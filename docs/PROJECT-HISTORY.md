# Project record

## Purpose

The site presents Vellitas as an outside-in certificate intelligence and security assessment platform. Its core distinction is that organizations commonly harden and test systems from the inside, while Vellitas observes public-facing certificate evidence from the external perspective an attacker or third party can see.

The product narrative is:

1. Discover public-facing services and associated digital certificates.
2. Enrich certificate evidence with DNS, network, geospatial, configuration, and historical context.
3. Detect defects such as expired or self-signed certificates, weak configurations, unusual locations, forgotten assets, and name encroachment.
4. Deliver a prioritized remediation report that explains the work required to fix and retest each defect.
5. Plan and complete remediation through Vellitas consultants, the customer's team, or a shared model.
6. Verify closure and continue monitoring the customer's external security profile under a subscription.

The report is intended to be actionable by corporate security, internal IT, or a company's third-party technology provider.

The public evidence section documents how vendor credentials, embedded third-party code, managed
service software, trusted updates, stolen certificates, fraudulent issuance, and TLS defects have
created real attack paths. Large incidents and downstream small-business impacts are presented with
authoritative sources and explicit product boundaries. The site maps relevant observations to IETF,
NIST, CISA, and PCI guidance without claiming certification. Continuous Certificate Transparency
ingestion remains a documented roadmap capability until production operation is verified.

## Inputs

The content and information architecture were developed from the supplied Vellitas problem/solution, patent-description, and key-selling-points presentations. Those source presentations are not copied into this public repository.

## Implementation decisions

- Built as real, semantic HTML pages with CSS and a small amount of JavaScript—not as screenshots or a WordPress theme.
- Uses no external font, tracking, analytics, or JavaScript dependency.
- Uses original generated artwork stored locally under `assets/`.
- Includes responsive navigation, keyboard-visible focus states, reduced-motion support, and a custom 404 page.
- References the public Vellitas patent records from the site.
- Uses a corrected intrinsic aspect ratio for the hero globe so it remains spherical across desktop viewport sizes.
- Sends all calls to action to a protected same-origin form backed by a private, parameterized SQLite service.
- Keeps Vellitas's Wyoming legal domicile in legal material rather than using it as leadership positioning.
- Introduces cofounders Spencer Shearer and Seth Shearer using biographies derived from their public LinkedIn profiles.
- Introduces Fraser Mackenzie as Chief Product & Technology Officer, reflecting his product vision, enterprise architecture, metadata, digital transformation, and AI experience.
- Includes a clearly labeled illustrative remediation report, a privacy notice, and organization structured data.
- Monitors the production pages, redirect behavior, security headers, and TLS certificate lifetime through an hourly GitHub Actions workflow.
- Distinguishes available capabilities from roadmap features and documents the customer portal, tenant isolation, responsible-scanning, retention, remediation automation, and continuous subscription model.
- Includes transparent vector shield assets for the blue Vellitas mark, green pass, yellow caution, and red immediate-action states.
- Rebuilds the complete logo family from the highest-resolution owner-supplied artwork, including a blue-shield header wordmark, shield-only report marks, and a matching favicon.
- Uses the established dark presentation consistently; the experimental light mode and its selector were removed after visual review.
- Opens external patent, LinkedIn, and public-roadmap links in a separate tab with `noopener noreferrer` protection and an assistive-technology announcement.
- Refreshes the 1200×630 social-sharing image and organization logo metadata to match the production identity.

## Production record

The launch site was configured on the Surf Ubuntu host with Nginx, HTTPS, security headers, versioned releases, and a reversible `current` symlink. Amazon Route 53 directs both the apex and `www` hostnames to production. Full operational details are in [`DEPLOYMENT.md`](DEPLOYMENT.md).
