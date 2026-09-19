# Report capability mapping

This document maps a private historical enterprise assessment to the Vellitas product-status model.
The private source is treated as evidence of analytical capability, not as permission to reproduce
customer-specific data or proof that every capability is already implemented as a self-service
product. Public examples use syntheticized data and deliberately omit source-identifying details.

## Capabilities demonstrated by the report

| Capability | Evidence in the supplied report | Product status |
| --- | --- | --- |
| Internet-visible discovery | Search across customer names, domains, IP ranges, and associated identifiers at enterprise scale | Available now |
| Geospatial enrichment | Country-level distribution and review of locations outside the expected operating pattern | Available now |
| Name and domain encroachment | Similar and proximal names, possible character substitution, and third-party domain examples | Available now |
| Certificate authority inventory | Multiple public, private, and self-signed trust patterns cataloged | Available now |
| Self-signed detection | Material self-signed populations identified with remediation guidance | Available now |
| Expiration analysis | Expired and next-90-day counts with renew-or-decommission guidance | Available now |
| Validity-duration analysis | Certificate lifetime distribution and long-validity review | Available now; legacy counts require reconciliation |
| Key-strength analysis | Certificates below the report's 2048-bit threshold | Available now |
| Signature-algorithm analysis | SHA-1 and weaker signing-algorithm population | Available now |
| Protocol and cipher analysis | SSL/TLS protocol evidence, weak-protocol host count, cipher components, and weak-cipher percentage | Available now |
| Non-production detection | Naming-based flag for test, development, QA, and related exposed services | Available now |
| Wildcard analysis | Wildcard count, largest wildcard domain, expired wildcard count, and operational-risk discussion | Available now |
| Certificate-level evidence | IP, country, serial, signature, authority, effective and expiration date, validity, company marker, key strength, and protocol | Available now |
| Corrective guidance | Portfolio recommendations and example remediation priorities | Available now; consultant-led workflow |

## Capabilities not demonstrated as continuous product functions

- Continuous Certificate Transparency ingestion and event-driven issuance alerting.
- DNS A, AAAA, CNAME, MX, and NS change monitoring.
- Fingerprint and public-key reuse graphs across IPs, networks, providers, vendors, and locations.
- Normalized first-seen, last-seen, and infrastructure-movement history.
- Customer-configurable policy, exception, and confidence-scoring engines.
- Tenant-scoped customer search, RBAC, SSO/MFA, and audit logging.
- Vendor relationship and assurance portfolios.
- Ticketing, SIEM, API, and webhook workflows.
- Generated remediation scripts with dry-run, approval, rollback, and outside-in verification.

## Source-data caution

The private source contained internally inconsistent nested validity-duration counts. The public
sample replaces those values with internally consistent syntheticized buckets while preserving the
lesson: production reporting must recalculate derived totals from raw observations and prevent
contradictory values from entering executive decisioning.

The supplied report is customer-specific and should not be published without appropriate
permission and transformation. The redesigned current-capability report is a real-world-informed
synthetic dataset: names, domains, IP addresses, dates, geographic distributions, counts, and
evidence rows are altered or synthesized. It retains realistic finding relationships and analytical
meaning without describing or fingerprinting the source customer. It is not a fresh customer
assessment.
