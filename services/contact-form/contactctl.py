#!/usr/bin/env python3
"""Read and update locally stored contact submissions from an administrator shell."""

from __future__ import annotations

import argparse
import os
import sqlite3
import textwrap
from pathlib import Path


def database_path() -> Path:
    return Path(os.environ.get("CONTACT_DATABASE", "/var/lib/vellitas-contact/submissions.sqlite3"))


def list_submissions(status: str, limit: int) -> None:
    with sqlite3.connect(database_path()) as db:
        rows = db.execute(
            """SELECT id, created_at, name, email, organization, role, message, status
               FROM submissions WHERE (? = 'all' OR status = ?) ORDER BY created_at DESC LIMIT ?""",
            (status, status, limit),
        ).fetchall()
    if not rows:
        print("No matching submissions.")
        return
    for row in rows:
        submission_id, created_at, name, email, organization, role, message, current_status = row
        print(f"{created_at}  {current_status.upper()}  {submission_id}")
        print(f"{name} <{email}> — {organization}" + (f" — {role}" if role else ""))
        print(textwrap.fill(message, width=96, initial_indent="  ", subsequent_indent="  "))
        print()


def set_status(submission_id: str, status: str) -> None:
    if status not in {"new", "reviewed", "closed"}:
        raise SystemExit("Status must be new, reviewed, or closed.")
    with sqlite3.connect(database_path()) as db:
        cursor = db.execute("UPDATE submissions SET status = ? WHERE id = ?", (status, submission_id))
    if cursor.rowcount != 1:
        raise SystemExit("Submission not found.")
    print(f"Updated {submission_id} to {status}.")


def main() -> None:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)
    list_parser = subparsers.add_parser("list")
    list_parser.add_argument("--status", choices=["new", "reviewed", "closed", "all"], default="new")
    list_parser.add_argument("--limit", type=int, default=20)
    status_parser = subparsers.add_parser("status")
    status_parser.add_argument("submission_id")
    status_parser.add_argument("value")
    args = parser.parse_args()
    if args.command == "list":
        list_submissions(args.status, max(1, min(args.limit, 100)))
    else:
        set_status(args.submission_id, args.value)


if __name__ == "__main__":
    main()
