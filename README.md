# Vellitas website

A dependency-free static website for `vellitas.com`. It can be hosted directly on Surf or any static hosting service without WordPress, a CMS, or a build step.

## Repository contents

- `index.html`, `styles.css`, `theme.js`, and `script.js`: the production website
- `assets/`: original website artwork and identity assets
- `deploy/nginx/vellitas.com.conf`: the production Nginx virtual host and contact-form proxy
- `services/contact-form/`: the dependency-free, same-origin briefing-form service
- `docs/DEPLOYMENT.md`: DNS, HTTPS, release, and rollback procedures
- `docs/EMAIL.md`: the public contact alias and email-security notes
- `docs/PROJECT-HISTORY.md`: product narrative and implementation record
- `docs/PRODUCT-ROADMAP.md`: patent-grounded product opportunities and website priorities
- `docs/CUSTOMER-PORTAL.md`: tenant isolation, scope onboarding, search, and remediation controls
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
Nginx serves the site directly and proxies only `/api/contact` to a small local Python service.
PostgreSQL, Node.js, PHP, WordPress, and a build step are not required.

- Release directory: `/var/www/vellitas.com/releases/20260918T054258Z`
- Active release: `/var/www/vellitas.com/current`
- Nginx site: `/etc/nginx/sites-available/vellitas.com`
- Enabled site: `/etc/nginx/sites-enabled/vellitas.com`
- Access log: `/var/log/nginx/vellitas.access.log`
- Error log: `/var/log/nginx/vellitas.error.log`
- Contact-service release: `/opt/vellitas-contact/releases/20260918T041542Z`

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

## Contact form

All primary calls to action lead to a same-origin briefing form. The service validates an exact
field allowlist, normalizes and bounds input, applies origin, host, timing, honeypot, duplicate,
and rate-limit controls, and writes parameterized records to a private SQLite database. Raw source
IP addresses are not retained in the form database.

Surf does not currently have a configured mail transport. Administrators review stored requests
with the private `contactctl.py` command documented in `services/contact-form/README.md` until a
transactional notification provider or Google Workspace relay is configured.

SPF, DKIM, and monitoring-mode DMARC are published in Route 53. Gmail still needs the one-time **Send mail as** setup before replies can originate from the public alias.

## Patent links

The patent section links to public records for U.S. Patent Nos. 10,771,260; 11,444,786; 11,831,785; and 12,250,327.

## Artwork

The globe, patent illustration, and social preview were generated specifically for Vellitas. The
logo family was rebuilt as transparent vector artwork from the highest-resolution owner-supplied
source and includes full-logo light/dark variants plus blue, green, yellow, and red report shields.
No third-party stock artwork or external font service is used.

The site follows the visitor's operating-system color preference by default. The header control
cycles through system, light, and dark modes and stores the choice locally in the browser. It does
not add tracking or send the preference to Vellitas.
