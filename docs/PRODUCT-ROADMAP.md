# Patent-grounded product opportunities

This document translates public Vellitas patent records into product-planning opportunities. It is not a legal opinion, a claim-construction analysis, or a statement that every listed capability is currently available. Public-facing material should distinguish shipped features from roadmap items.

## Capabilities supported by the patent family

The public patent family describes internet-wide certificate discovery, combining certificate contents with external observations, querying for vulnerable certificates, comparing expected and observed information, preserving changes over time, and notifying customers or requesting corrective action.

### High-value metadata and analysis

1. **TLS and server posture**
   Capture supported protocol versions, cipher suites, chain completeness, key and signature strength, compression, revocation signals, renegotiation behavior, and other externally observable handshake characteristics.
2. **Certificate identity and deployment graph**
   Link fingerprints, public-key hashes, serial numbers, subject and authority key identifiers, issuer, SANs, DNS, reverse DNS, IP addresses, network owner, and observed locations. Use the graph to identify the same certificate or key across multiple hosts or regions.
3. **Historical observations**
   Preserve first-seen, last-seen, observation time, network and geolocation history, configuration changes, and renewal lineage. Show what changed, when it changed, and when Vellitas observed the change.
4. **Expected-versus-observed policy**
   Let customers define approved issuers, locations, networks, cloud regions, protocol versions, certificate lifetimes, and environments. Flag deviations from those expectations.
5. **Certificate creep**
   Identify development, test, QA, staging, internal, sample, default, and self-signed certificates exposed publicly. Combine naming signals with location and server context to reduce false positives.
6. **Name encroachment**
   Detect lookalike company and domain names, character substitution, suspicious prefixes or suffixes, and certificates issued for names that could mislead customers.
7. **Incident blast radius**
   Search by issuer, issuance window, fingerprint, public key, configuration weakness, or location to identify every affected public deployment after a CA, key, or protocol incident.
8. **Notification and remediation workflow**
   Notify customers when observations change, generate assignable remediation work, request revocation or removal when appropriate, retest the public endpoint, and preserve an audit trail through closure.

## Adjacent outside-in capabilities

- Certificate Transparency monitoring for early warning when a related certificate is issued.
- An attack-surface graph connecting certificates, domains, DNS, IP addresses, autonomous systems, cloud providers, ports, and externally visible services.
- Domain and DNS posture checks covering CAA, DNSSEC, SPF, DKIM, DMARC, dangling records, and takeover indicators.
- Web-edge posture including HTTPS redirects, HSTS, security headers, exposed administrative interfaces, and obsolete protocols.
- Vendor and subsidiary exposure views that separate first-party assets from hosted, acquired, or third-party infrastructure.
- API, webhook, SIEM, and ticketing integrations with ownership, due dates, retest status, and evidence attachments.
- Exposure trends and an executive score based on observed evidence, severity, duration, recurrence, and remediation progress.

## Recommended sequence

### First

- Normalize the real assessment report into an evidence model.
- Add historical observations and same-certificate or same-key deployment detection.
- Add customer-defined expected locations, networks, issuers, and protocol policies.
- Produce remediation instructions and an outside-in verification result for every finding.

### Next

- Add Certificate Transparency and name-encroachment monitoring.
- Add alerting, ticket creation, ownership, retest, and audit history.
- Add an attack-surface graph and vendor attribution.

### Later

- Add approved automated actions, including revocation or removal requests, only with strong authorization controls and human review.
- Expand into broader DNS and web-edge posture after the certificate workflow is reliable and explainable.

## Website assessment

The website's weakest area is product proof. The visual presentation and outside-in message are strong, but a buyer cannot yet inspect a real deliverable, understand the exact assessment scope, or see how findings move from observation to verified closure.

The strongest improvements are:

1. Replace the illustrative report with a carefully redacted real report and retain a short sample finding on the page.
2. Add a methodology section that states what Vellitas observes, how often it observes it, what it does not access, and how confidence is assigned.
3. Label current capabilities and planned capabilities separately.
4. Replace the email-only call to action with a protected qualification form connected to a sales workflow while retaining the role alias.
5. Add data-handling, retention, and responsible-scanning information for security buyers.
6. Add customer, partner, or independently verifiable evidence when permission is available.

## Public patent records

- [US 10,771,260](https://patents.google.com/patent/US10771260B2/en)
- [US 11,444,786](https://patents.google.com/patent/US11444786B2/en)
- [US 11,831,785](https://patents.google.com/patent/US11831785B2/en)
- [US 12,250,327](https://patents.google.com/patent/US12250327B2/en)
