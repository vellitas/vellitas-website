# Project record

## Purpose

The site presents Vellitas as an outside-in certificate intelligence and security assessment platform. Its core distinction is that organizations commonly harden and test systems from the inside, while Vellitas observes public-facing certificate evidence from the external perspective an attacker or third party can see.

The product narrative is:

1. Discover public-facing services and associated digital certificates.
2. Enrich certificate evidence with DNS, network, geospatial, configuration, and historical context.
3. Detect defects such as expired or self-signed certificates, weak configurations, unusual locations, forgotten assets, and name encroachment.
4. Deliver a prioritized remediation report that explains the work required to fix and retest each defect.

The report is intended to be actionable by corporate security, internal IT, or a company's third-party technology provider.

## Inputs

The content and information architecture were developed from the supplied Vellitas problem/solution, patent-description, and key-selling-points presentations. Those source presentations are not copied into this public repository.

## Implementation decisions

- Built as real, semantic HTML pages with CSS and a small amount of JavaScript—not as screenshots or a WordPress theme.
- Uses no external font, tracking, analytics, or JavaScript dependency.
- Uses original generated artwork stored locally under `assets/`.
- Includes responsive navigation, keyboard-visible focus states, reduced-motion support, and a custom 404 page.
- References the public Vellitas patent records from the site.
- Uses a corrected intrinsic aspect ratio for the hero globe so it remains spherical across desktop viewport sizes.
- Sends all calls to action to the role alias `contact@vellitas.com`.

## Production record

The launch site was configured on the Surf Ubuntu host with Nginx, HTTPS, security headers, versioned releases, and a reversible `current` symlink. Amazon Route 53 directs both the apex and `www` hostnames to production. Full operational details are in [`DEPLOYMENT.md`](DEPLOYMENT.md).
