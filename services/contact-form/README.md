# Contact intake service

This dependency-free Python service accepts the public briefing form through an exact same-origin endpoint. It stores only the submitted lead fields and an HMAC of the source IP; the raw IP address is not retained in the form database.

Security controls include an exact field allowlist, strict length and type validation, Unicode normalization, body-size limits, origin and host validation, a timing heuristic, a honeypot, duplicate suppression, an in-process hourly limit, Nginx request limiting, parameterized SQLite statements, and a systemd sandbox. The service does not execute submitted text or interpolate it into SQL, HTML, headers, or shell commands.

Submissions are stored at `/var/lib/vellitas-contact/submissions.sqlite3`. Administrators can review them on Surf with:

```bash
sudo -u vellitas-contact CONTACT_DATABASE=/var/lib/vellitas-contact/submissions.sqlite3 \
  python3 /opt/vellitas-contact/current/contactctl.py list --status new
```

An email notification transport is intentionally not embedded. Surf has no configured mail transport, and adding an SMTP credential to browser code or source control would be unsafe. A production notification integration should use a transactional provider or Google Workspace relay with secrets stored only in `/etc/vellitas/contact-form.env` or an external secret manager.
