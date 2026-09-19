import tempfile
import time
import unittest
from pathlib import Path

from server import ContactStore, Settings, ValidationError, validate_payload


def valid_payload():
    return {
        "name": "Ada Lovelace",
        "email": "ada@example.com",
        "organization": "Example Company",
        "role": "Security lead",
        "message": "We would like to assess our public certificate inventory.",
        "consent": True,
        "website": "",
        "startedAt": int(time.time() * 1000) - 5_000,
    }


class ValidationTests(unittest.TestCase):
    def test_valid_payload_is_normalized(self):
        data = validate_payload(valid_payload())
        self.assertEqual(data["email"], "ada@example.com")
        self.assertFalse(data["honeypot"])

    def test_honeypot_is_silently_identified(self):
        payload = valid_payload()
        payload["website"] = "https://spam.invalid"
        self.assertTrue(validate_payload(payload)["honeypot"])

    def test_too_fast_is_rejected(self):
        payload = valid_payload()
        payload["startedAt"] = int(time.time() * 1000)
        with self.assertRaises(ValidationError):
            validate_payload(payload)

    def test_unknown_field_is_rejected(self):
        payload = valid_payload()
        payload["admin"] = True
        with self.assertRaises(ValidationError):
            validate_payload(payload)

    def test_header_injection_email_is_rejected(self):
        payload = valid_payload()
        payload["email"] = "ada@example.com\nBcc: victim@example.com"
        with self.assertRaises(ValidationError):
            validate_payload(payload)


class StoreTests(unittest.TestCase):
    def test_parameterized_storage_and_duplicate_detection(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            settings = Settings(
                host="127.0.0.1",
                port=0,
                database_path=Path(temp_dir) / "submissions.sqlite3",
                allowed_origins=frozenset({"https://vellitas.com"}),
                public_host="vellitas.com",
                hmac_secret=b"x" * 32,
                retention_days=730,
                max_submissions_per_hour=5,
            )
            store = ContactStore(settings)
            data = validate_payload(valid_payload())
            first_id, first_duplicate = store.save(data, "192.0.2.1")
            second_id, second_duplicate = store.save(data, "192.0.2.1")
            self.assertFalse(first_duplicate)
            self.assertTrue(second_duplicate)
            self.assertEqual(first_id, second_id)


if __name__ == "__main__":
    unittest.main()
