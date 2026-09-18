# Production deployment

The production website is a dependency-free static site. Nginx serves the files directly and proxies the exact `/api/contact` path to a small Python standard-library service bound to loopback. PostgreSQL, Node.js, PHP, WordPress, and a build step are not required.

## Infrastructure

- Canonical URL: `https://vellitas.com`
- Production host: Surf (`135.148.44.243`)
- Operating system: Ubuntu 24.04 LTS
- Web server: Nginx
- TLS: Let's Encrypt, managed by Certbot
- DNS: Amazon Route 53
- Web root symlink: `/var/www/vellitas.com/current`
- Release root: `/var/www/vellitas.com/releases`
- Nginx configuration: `/etc/nginx/sites-available/vellitas.com`
- Contact service code: `/opt/vellitas-contact/current`
- Contact database: `/var/lib/vellitas-contact/submissions.sqlite3`
- Contact environment: `/etc/vellitas/contact-form.env`

The checked-in Nginx configuration is at [`deploy/nginx/vellitas.com.conf`](../deploy/nginx/vellitas.com.conf).

## DNS records

The Route 53 hosted zone uses these website records:

| Name | Type | Value |
| --- | --- | --- |
| `vellitas.com` | `A` | `135.148.44.243` |
| `www.vellitas.com` | `CNAME` | `vellitas.com` |

`vellitas.com` is canonical. Nginx redirects both HTTP hostnames and the HTTPS `www` hostname to `https://vellitas.com`.

## Release procedure

Create a fresh release for every deployment. Do not edit the active release in place.

```bash
release_id=$(date -u +%Y%m%dT%H%M%SZ)
release_path="/var/www/vellitas.com/releases/$release_id"

ssh surf "sudo install -d -o svshearer -g svshearer -m 0755 '$release_path'"
rsync -az --delete --exclude README.md --exclude ASSET-NOTES.md ./ "surf:$release_path/"
ssh surf "sudo ln -sfn '$release_path' /var/www/vellitas.com/current && sudo nginx -t"
```

After activation, verify the canonical response, the redirect, and the main security headers:

```bash
curl -fsSI https://vellitas.com/
curl -fsSI https://www.vellitas.com/
```

The HTML is served with `Cache-Control: no-cache`. Static assets are cached for 30 days, so change their query-string version in `index.html` whenever a CSS or JavaScript file changes.

## Contact service deployment

The service runs as the unprivileged `vellitas-contact` user under a hardened systemd unit. Its environment file must be owned by root, readable only by root and the service group, and contain a random `CONTACT_HMAC_SECRET` of at least 32 characters. Never commit the live secret.

Copy `services/contact-form/` to a timestamped directory under `/opt/vellitas-contact/releases`, point `/opt/vellitas-contact/current` to it, install `vellitas-contact.service`, then run:

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now vellitas-contact.service
sudo systemctl restart vellitas-contact.service
curl --fail http://127.0.0.1:8787/healthz
sudo nginx -t
sudo systemctl reload nginx
```

The Nginx layer limits body size and request rate. The application separately validates host and origin, input types and lengths, form timing, a honeypot, duplicates, and an hourly source limit. SQLite writes use bound parameters, and raw source IP addresses are not stored.

Review new submissions with:

```bash
sudo -u vellitas-contact CONTACT_DATABASE=/var/lib/vellitas-contact/submissions.sqlite3 \
  python3 /opt/vellitas-contact/current/contactctl.py list --status new
```

Surf does not currently have an active mail transport. Add a transactional notification provider or a properly authorized Google Workspace relay before expecting submission emails; keep any credential in the root-owned environment file or an external secret manager.

## Rollback

List the available releases, select the last known-good absolute path, and repoint the symlink:

```bash
ssh surf 'ls -1dt /var/www/vellitas.com/releases/*'
ssh surf "sudo ln -sfn '/var/www/vellitas.com/releases/RELEASE_ID' /var/www/vellitas.com/current && sudo nginx -t"
```

## TLS maintenance

Certbot installed the certificate for `vellitas.com` and `www.vellitas.com` and manages renewal. Periodically verify renewal with:

```bash
ssh surf 'sudo certbot renew --dry-run'
```

## Current production release

Website commit `da298f3` was deployed as `/var/www/vellitas.com/releases/20260918T135048Z`
on September 18, 2026. The immediately preceding rollback release is
`/var/www/vellitas.com/releases/20260918T055703Z`. The contact service remains at
`/opt/vellitas-contact/releases/20260918T041542Z`.

The current website includes the corrected blue-shield header logo, matching report and favicon
vectors, the established dark presentation, protected external-link behavior, refreshed social
preview, the three-person leadership section, methodology and product-status sections, the
subscription and remediation lifecycle, the protected briefing form, illustrative report, privacy
and data-practices notices, sourced vendor and certificate incident evidence, standards mapping,
Certificate Transparency roadmap requirements, structured organization data, Search Console
verification, and sitemap.

Google Search Console ownership for the canonical URL-prefix property was verified with an HTML meta tag, and `sitemap.xml` was accepted successfully with three discovered pages.

## Production monitoring

Run the production check locally with:

```bash
./scripts/check-production.sh
```

The same check runs hourly and on demand through `.github/workflows/site-health.yml`. It verifies core content, the canonical redirect, security headers, public supporting files, and that the TLS certificate has at least 21 days remaining.
