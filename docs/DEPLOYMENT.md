# Production deployment

The production website is a dependency-free static site. Nginx serves the files directly; PostgreSQL, Node.js, PHP, WordPress, and other application runtimes are not required.

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

## Current launch release

The current v1 revision was deployed as `/var/www/vellitas.com/releases/20260918T023044Z` on September 17, 2026. It includes the three-person leadership section, illustrative remediation report, privacy notice, structured organization data, Search Console verification, and updated sitemap.

Google Search Console ownership for the canonical URL-prefix property was verified with an HTML meta tag, and `sitemap.xml` was accepted successfully with three discovered pages.

## Production monitoring

Run the production check locally with:

```bash
./scripts/check-production.sh
```

The same check runs hourly and on demand through `.github/workflows/site-health.yml`. It verifies core content, the canonical redirect, security headers, public supporting files, and that the TLS certificate has at least 21 days remaining.
