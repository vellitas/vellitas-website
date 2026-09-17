# Vellitas website

A dependency-free static website for `vellitas.com`. It can be hosted directly on Surf or any static hosting service without WordPress, a CMS, or a build step.

## Repository contents

- `index.html`, `styles.css`, and `script.js`: the production website
- `assets/`: original website artwork and identity assets
- `deploy/nginx/vellitas.com.conf`: the production Nginx virtual host
- `docs/DEPLOYMENT.md`: DNS, HTTPS, release, and rollback procedures
- `docs/EMAIL.md`: the public contact alias and email-security notes
- `docs/PROJECT-HISTORY.md`: product narrative and implementation record
- `scripts/check-production.sh`: production availability, redirect, header, and TLS checks
- `.github/workflows/site-health.yml`: hourly production monitoring through GitHub Actions

## Preview locally

From this folder, run:

```bash
python3 -m http.server 4173
```

Then open `http://localhost:4173`.

## Production deployment

The production host is the Ubuntu server reached with `ssh surf` at `135.148.44.243`.
Nginx serves the site directly; PostgreSQL and an application runtime are not required.

- Release directory: `/var/www/vellitas.com/releases/20260917T070434Z`
- Active release: `/var/www/vellitas.com/current`
- Nginx site: `/etc/nginx/sites-available/vellitas.com`
- Enabled site: `/etc/nginx/sites-enabled/vellitas.com`
- Access log: `/var/log/nginx/vellitas.access.log`
- Error log: `/var/log/nginx/vellitas.error.log`

To publish a later revision, upload it to a new timestamped release directory, validate it,
move the `current` symlink to that release, run `sudo nginx -t`, and reload Nginx. Keeping each
release in its own directory makes rollback a single symlink change.

## Route 53 and HTTPS

The intended records in the Route 53 hosted zone for `vellitas.com` are:

- Apex `A`: `135.148.44.243`
- `www` `CNAME`: `vellitas.com`

The apex is the canonical hostname. Nginx redirects `www.vellitas.com` to
`https://vellitas.com`. Certbot manages the Let's Encrypt certificate and renewal for both
hostnames. The initial ECDSA certificate expires December 16, 2026; an immediate Certbot
renewal simulation completed successfully after installation.

## Contact action

All primary calls to action open a pre-addressed email to `contact@vellitas.com`, a Google Workspace alias routed to the company inbox.

SPF, DKIM, and monitoring-mode DMARC are published in Route 53. Gmail still needs the one-time **Send mail as** setup before replies can originate from the public alias.

## Patent links

The patent section links to public records for U.S. Patent Nos. 10,771,260; 11,444,786; 11,831,785; and 12,250,327.

## Artwork

The globe, patent illustration, and social preview were generated specifically for Vellitas. No third-party stock artwork or external font service is used.
