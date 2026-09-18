#!/usr/bin/env python3
"""Minimal, dependency-free contact intake service for vellitas.com."""

from __future__ import annotations

import hashlib
import hmac
import json
import os
import re
import sqlite3
import threading
import time
import unicodedata
import uuid
from collections import defaultdict, deque
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any


EMAIL_RE = re.compile(r"^[^\s@]{1,64}@[A-Za-z0-9.-]{1,189}\.[A-Za-z]{2,63}$")
CONTROL_RE = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]")
ALLOWED_FIELDS = {"name", "email", "organization", "role", "message", "consent", "website", "startedAt"}
MAX_BODY_BYTES = 16_384
FIELD_LIMITS = {"name": 100, "email": 254, "organization": 160, "role": 120, "message": 3_000}


class ValidationError(ValueError):
    pass


@dataclass(frozen=True)
class Settings:
    host: str
    port: int
    database_path: Path
    allowed_origins: frozenset[str]
    public_host: str
    hmac_secret: bytes
    retention_days: int
    max_submissions_per_hour: int

    @classmethod
    def from_environment(cls) -> "Settings":
        secret = os.environ.get("CONTACT_HMAC_SECRET", "")
        if len(secret) < 32:
            raise RuntimeError("CONTACT_HMAC_SECRET must contain at least 32 characters")
        origins = frozenset(
            item.strip().rstrip("/")
            for item in os.environ.get("CONTACT_ALLOWED_ORIGINS", "https://vellitas.com").split(",")
            if item.strip()
        )
        return cls(
            host=os.environ.get("CONTACT_BIND", "127.0.0.1"),
            port=int(os.environ.get("CONTACT_PORT", "8787")),
            database_path=Path(os.environ.get("CONTACT_DATABASE", "/var/lib/vellitas-contact/submissions.sqlite3")),
            allowed_origins=origins,
            public_host=os.environ.get("CONTACT_PUBLIC_HOST", "vellitas.com"),
            hmac_secret=secret.encode("utf-8"),
            retention_days=int(os.environ.get("CONTACT_RETENTION_DAYS", "730")),
            max_submissions_per_hour=int(os.environ.get("CONTACT_MAX_PER_HOUR", "5")),
        )


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def normalize_text(value: Any, field: str) -> str:
    if not isinstance(value, str):
        raise ValidationError(f"{field} must be text")
    value = unicodedata.normalize("NFKC", value).strip()
    if CONTROL_RE.search(value):
        raise ValidationError(f"{field} contains unsupported characters")
    if len(value) > FIELD_LIMITS[field]:
        raise ValidationError(f"{field} is too long")
    return value


def validate_payload(payload: Any, now_ms: int | None = None) -> dict[str, Any]:
    if not isinstance(payload, dict):
        raise ValidationError("request body must be an object")
    unknown = set(payload) - ALLOWED_FIELDS
    if unknown:
        raise ValidationError("request contains unsupported fields")

    now_ms = now_ms if now_ms is not None else int(time.time() * 1000)
    try:
        started_at = int(payload.get("startedAt", 0))
    except (TypeError, ValueError) as exc:
        raise ValidationError("invalid form timing") from exc
    elapsed = now_ms - started_at
    if elapsed < 3_000 or elapsed > 7_200_000:
        raise ValidationError("invalid form timing")

    if payload.get("website") not in (None, ""):
        return {"honeypot": True}
    if payload.get("consent") is not True:
        raise ValidationError("consent is required")

    data = {field: normalize_text(payload.get(field, ""), field) for field in FIELD_LIMITS}
    if not data["name"] or not data["email"] or not data["organization"] or not data["message"]:
        raise ValidationError("name, email, organization, and message are required")
    if "\n" in data["email"] or "\r" in data["email"] or not EMAIL_RE.fullmatch(data["email"]):
        raise ValidationError("enter a valid work email")
    if len(data["message"]) < 20:
        raise ValidationError("tell us a little more about your needs")
    data["email"] = data["email"].lower()
    data["honeypot"] = False
    return data


class ContactStore:
    def __init__(self, settings: Settings):
        self.settings = settings
        settings.database_path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize()

    def connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.settings.database_path, timeout=10)
        connection.execute("PRAGMA foreign_keys = ON")
        connection.execute("PRAGMA journal_mode = WAL")
        connection.execute("PRAGMA busy_timeout = 5000")
        return connection

    def _initialize(self) -> None:
        with self.connect() as db:
            db.execute(
                """
                CREATE TABLE IF NOT EXISTS submissions (
                    id TEXT PRIMARY KEY,
                    created_at TEXT NOT NULL,
                    name TEXT NOT NULL,
                    email TEXT NOT NULL,
                    organization TEXT NOT NULL,
                    role TEXT NOT NULL,
                    message TEXT NOT NULL,
                    source_ip_hash TEXT NOT NULL,
                    content_hash TEXT NOT NULL,
                    status TEXT NOT NULL DEFAULT 'new'
                )
                """
            )
            db.execute("CREATE INDEX IF NOT EXISTS idx_submissions_created ON submissions(created_at)")
            db.execute("CREATE INDEX IF NOT EXISTS idx_submissions_content ON submissions(content_hash)")

    def _digest(self, value: str) -> str:
        return hmac.new(self.settings.hmac_secret, value.encode("utf-8"), hashlib.sha256).hexdigest()

    def save(self, data: dict[str, Any], remote_ip: str) -> tuple[str, bool]:
        created_at = utc_now().isoformat(timespec="seconds")
        content = "\x1f".join(data[field] for field in ("email", "organization", "message"))
        content_hash = self._digest(content)
        duplicate_since = (utc_now() - timedelta(hours=24)).isoformat(timespec="seconds")
        with self.connect() as db:
            duplicate = db.execute(
                "SELECT id FROM submissions WHERE content_hash = ? AND created_at >= ? LIMIT 1",
                (content_hash, duplicate_since),
            ).fetchone()
            if duplicate:
                return duplicate[0], True
            submission_id = str(uuid.uuid4())
            db.execute(
                """
                INSERT INTO submissions
                    (id, created_at, name, email, organization, role, message, source_ip_hash, content_hash)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    submission_id,
                    created_at,
                    data["name"],
                    data["email"],
                    data["organization"],
                    data["role"],
                    data["message"],
                    self._digest(remote_ip),
                    content_hash,
                ),
            )
        return submission_id, False

    def purge_expired(self) -> int:
        cutoff = (utc_now() - timedelta(days=self.settings.retention_days)).isoformat(timespec="seconds")
        with self.connect() as db:
            cursor = db.execute("DELETE FROM submissions WHERE created_at < ?", (cutoff,))
            return cursor.rowcount


class HourlyRateLimiter:
    def __init__(self, maximum: int):
        self.maximum = maximum
        self.events: dict[str, deque[float]] = defaultdict(deque)
        self.lock = threading.Lock()

    def allow(self, key: str) -> bool:
        now = time.monotonic()
        cutoff = now - 3_600
        with self.lock:
            events = self.events[key]
            while events and events[0] < cutoff:
                events.popleft()
            if len(events) >= self.maximum:
                return False
            events.append(now)
            return True


class ContactHandler(BaseHTTPRequestHandler):
    server_version = "VellitasContact"

    @property
    def app(self) -> "ContactServer":
        return self.server  # type: ignore[return-value]

    def log_message(self, format_string: str, *args: Any) -> None:
        message = format_string % args
        print(json.dumps({"time": utc_now().isoformat(), "remote": self.client_address[0], "message": message}), flush=True)

    def _json(self, status: HTTPStatus, payload: dict[str, Any]) -> None:
        body = json.dumps(payload, separators=(",", ":")).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:
        if self.path == "/healthz":
            self._json(HTTPStatus.OK, {"status": "ok"})
        else:
            self._json(HTTPStatus.NOT_FOUND, {"error": "not found"})

    def do_POST(self) -> None:
        if self.path != "/api/contact":
            self._json(HTTPStatus.NOT_FOUND, {"error": "not found"})
            return

        settings = self.app.settings
        host = self.headers.get("Host", "").split(":", 1)[0].lower()
        origin = self.headers.get("Origin", "").rstrip("/")
        if host != settings.public_host or origin not in settings.allowed_origins:
            self._json(HTTPStatus.FORBIDDEN, {"error": "request origin was not accepted"})
            return
        if self.headers.get_content_type() != "application/json":
            self._json(HTTPStatus.UNSUPPORTED_MEDIA_TYPE, {"error": "send JSON"})
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            length = 0
        if length < 2 or length > MAX_BODY_BYTES:
            self._json(HTTPStatus.REQUEST_ENTITY_TOO_LARGE, {"error": "request size was not accepted"})
            return

        remote_ip = self.headers.get("X-Real-IP", self.client_address[0]).strip()
        rate_key = hmac.new(settings.hmac_secret, remote_ip.encode("utf-8"), hashlib.sha256).hexdigest()
        if not self.app.rate_limiter.allow(rate_key):
            self._json(HTTPStatus.TOO_MANY_REQUESTS, {"error": "please wait before trying again"})
            return

        try:
            payload = json.loads(self.rfile.read(length))
            data = validate_payload(payload)
        except (json.JSONDecodeError, UnicodeDecodeError, ValidationError) as exc:
            self._json(HTTPStatus.BAD_REQUEST, {"error": str(exc)})
            return

        if data.get("honeypot"):
            self._json(HTTPStatus.ACCEPTED, {"status": "received"})
            return

        self.app.store.save(data, remote_ip)
        if self.app.request_count % 25 == 0:
            self.app.store.purge_expired()
        self.app.request_count += 1
        self._json(HTTPStatus.CREATED, {"status": "received"})


class ContactServer(ThreadingHTTPServer):
    daemon_threads = True

    def __init__(self, settings: Settings):
        self.settings = settings
        self.store = ContactStore(settings)
        self.rate_limiter = HourlyRateLimiter(settings.max_submissions_per_hour)
        self.request_count = 1
        super().__init__((settings.host, settings.port), ContactHandler)


def main() -> None:
    settings = Settings.from_environment()
    server = ContactServer(settings)
    print(json.dumps({"status": "listening", "address": settings.host, "port": settings.port}), flush=True)
    try:
        server.serve_forever(poll_interval=0.5)
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
