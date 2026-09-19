# Patent-grounded product opportunities

This document translates public Vellitas patent records into product-planning opportunities. It is not a legal opinion, a claim-construction analysis, or a statement that every listed capability is currently available. Public-facing material should distinguish shipped features from roadmap items.

## Product status definitions

- **Available now**: delivered through the current Vellitas assessment and report workflow.
- **Near-term roadmap**: the next productization work after the real report is normalized into a repeatable evidence model.
- **Future roadmap**: a validated direction that still requires design, security review, and delivery planning.

The website status colors are blue for the Vellitas assessment, green for pass, yellow for caution, and red for immediate action. They communicate assessment outcome, not roadmap maturity.

## Available now

- Internet-visible certificate discovery from approved company names, domains, IP ranges, and other
  customer markers.
- Certificate and endpoint enrichment including IP address, country, issuer, serial number,
  signature algorithm, effective and expiration dates, validity duration, organization marker, key
  strength, and presented encryption protocol.
- DNS, reverse DNS, network, geospatial, configuration, and historical enrichment.
- Certificate-authority inventory and third-party versus self-signed classification.
- Expired, near-expiry, long-validity, weak-key, weak-signature, weak-protocol, weak-cipher,
  wildcard, and publicly exposed non-production certificate analysis.
- Unusual-location and name/domain-encroachment analysis with customer validation before a risk
  signal is treated as misuse or compromise.
- Evidence-based reporting with corrective work and an outside-in verification test.
- Consultant-led remediation or collaboration with the customer's security, IT, and technology providers.

These capabilities are demonstrated in the supplied December 2016 Global Risk and Vulnerability
Report and mapped in [Report capability mapping](REPORT-CAPABILITY-MAPPING.md). The report proves
the analytical capability, not that every legacy metric remains current or that the workflow is
already fully productized.

## Subscription operating model

Vellitas is a continuous service rather than a one-time report. The standard lifecycle is:

1. Confirm the customer's authorized scope and establish a baseline.
2. Deliver the initial assessment report and prioritized remediation plan.
3. Complete the corrective work through Vellitas consultants, the customer's team, or a shared delivery model.
4. Reobserve affected endpoints and record verified closure.
5. Continue monitoring the external security profile and notify the customer when a validated change requires action.

The standard planning cadence is a full onboarding baseline, daily review of changed or newly discovered endpoints, weekly portfolio reassessment, monthly reporting, quarterly scope confirmation, and on-demand retesting after remediation. Customer contracts define actual service levels and notification timing.

## Capabilities supported by the patent family

The public patent family describes internet-wide certificate discovery, combining certificate contents with external observations, querying for vulnerable certificates, comparing expected and observed information, preserving changes over time, and notifying customers or requesting corrective action.

### High-value metadata and analysis

1. **TLS and server posture**
   Protocol, cipher, key-strength, and signature analysis are current. Expand the normalized evidence
   model for chain completeness, compression, revocation signals, renegotiation behavior, and other
   externally observable handshake characteristics.
2. **Certificate identity and deployment graph**
   Serial number, issuer, IP, organization marker, and location correlation are current. Productize
   fingerprints, public-key hashes, subject and authority key identifiers, SANs, DNS, reverse DNS,
   network owner, and same-certificate or same-key deployment graphs.
3. **Historical observations**
   Preserve first-seen, last-seen, observation time, network and geolocation history, configuration changes, and renewal lineage. Show what changed, when it changed, and when Vellitas observed the change.
4. **Expected-versus-observed policy**
   Analyst-led comparison with expected issuers, locations, protocols, lifetimes, and environments is
   current. Productize tenant-configurable policy, approved networks and cloud regions, exceptions,
   and explainable deviation scoring.
5. **Certificate creep**
   Current naming analysis identifies development, test, QA, staging, internal, sample, default,
   and self-signed certificates exposed publicly. Expand correlation with location, ownership, and
   server context to reduce false positives.
6. **Name encroachment**
   Current name and domain encroachment analysis identifies organization names, domains, proximal
   names, and possible character substitutions. Expand similarity models, CT-driven notification,
   ownership evidence, and analyst disposition.
7. **Incident blast radius**
   Search by issuer, issuance window, fingerprint, public key, configuration weakness, or location to identify every affected public deployment after a CA, key, or protocol incident.
8. **Notification and remediation workflow**
   Notify customers when observations change, generate assignable remediation work, request revocation or removal when appropriate, retest the public endpoint, and preserve an audit trail through closure.

## Adjacent outside-in capabilities

- Continuous Certificate Transparency ingestion for early warning when a related certificate is
  issued. Correlate issuer, serial number, fingerprint, public-key hash, SANs, log timestamp,
  DNS, IP, ASN, provider, geolocation, current deployments, and customer-approved policy. Suppress
  known renewals and approved CDN or cloud patterns before notification.
- An attack-surface graph connecting certificates, domains, DNS, IP addresses, autonomous systems, cloud providers, ports, and externally visible services.
- Domain and DNS posture checks covering CAA, DNSSEC, SPF, DKIM, DMARC, dangling records, and takeover indicators.
- Web-edge posture including HTTPS redirects, HSTS, security headers, exposed administrative interfaces, and obsolete protocols.
- Vendor and subsidiary exposure views that separate first-party assets from hosted, acquired, or
  third-party infrastructure. Maintain the customer-to-vendor relationship, the business service,
  access level, authorized assessment scope, criticality, required baseline, exceptions, and most
  recent verification result.
- API, webhook, SIEM, and ticketing integrations with ownership, due dates, retest status, and evidence attachments.
- Exposure trends and an executive score based on observed evidence, severity, duration, recurrence, and remediation progress.

## Customer portal and scope control

The proposed portal is a roadmap capability. It must not expose a global certificate search to customers. Every asset, observation, finding, report, remediation artifact, script, and query must be bound to a tenant identifier and enforced with deny-by-default authorization at the data layer.

Onboarding begins with customer-provided seed domains, brands, subsidiaries, acquisitions, approved networks, and cloud accounts. Vellitas then uses public certificate, SAN, Certificate Transparency, DNS, reverse-DNS, RDAP, ASN, redirect, and shared-infrastructure signals to propose related assets. A candidate remains in a review queue until ownership or assessment authority is confirmed, ideally with DNS TXT proof and otherwise through documented manual approval. Quarterly scope confirmation and ownership-change checks reduce stale authorization.

Once approved, the customer can search and filter only its tenant-scoped portfolio—for example, self-signed certificates, a specific business unit, issuer, region, or remediation state. Narrowing and expanding a query changes only filters within the approved portfolio; it never expands authorization. See [Customer portal architecture](CUSTOMER-PORTAL.md).

## Vendor assurance model

Vendor assurance is a continuous use case rather than a one-time procurement questionnaire. A
customer should identify vendors whose software, code, identity, remote access, hosted service, or
network connection could affect its operations or data. Vellitas can then apply a customer-approved
outside-in baseline proportionate to that relationship.

The initial baseline should include certificate validity and chain health, unexpected issuers,
certificate and public-key reuse, supported TLS versions and cipher suites, DNS and nameserver
posture, observed IP/ASN/provider/geography, exposed administrative or appliance interfaces within
scope, and historical change. Continuous checks should identify material drift and attach the
observed evidence, confidence, customer policy, responsible party, and retest requirement.

Passive public sources such as Certificate Transparency and DNS history may identify a candidate
vendor exposure. Active assessment must remain within written authorization. A vendor anomaly does
not establish compromise and must be validated against legitimate CDN, cloud, disaster-recovery,
acquisition, and subcontractor patterns.

The evidence and standards supporting this model are maintained in
[Evidence, vendor risk, and standards](EVIDENCE-AND-STANDARDS.md).

## Remediation automation safeguards

Generated remediation scripts are a roadmap capability and must be treated as controlled change artifacts, not autonomous fixes. Every script should be versioned, tied to a specific finding and target, reviewed by Vellitas and the customer, support a dry-run or preview where the platform permits it, require explicit approval, preserve output and rollback guidance, and be verified from the outside after execution. Automatic execution is off by default.

## Recommended sequence

### First

- Normalize the real assessment report into an evidence model.
- Add historical observations and same-certificate or same-key deployment detection.
- Add customer-defined expected locations, networks, issuers, and protocol policies.
- Produce remediation instructions and an outside-in verification result for every finding.
- Apply the public data-retention and responsible-scanning baseline and support contract-specific overrides.

### Next

- Add continuous Certificate Transparency and name-encroachment change monitoring.
- Add alerting, ticket creation, ownership, retest, and audit history.
- Add an attack-surface graph and vendor attribution.
- Launch tenant-scoped portfolio search with candidate-scope review, RBAC, SSO/MFA, and audit logging.
- Generate reviewed, versioned remediation scripts with dry-run, approval, and rollback controls.

### Later

- Add approved automated actions, including revocation or removal requests, only with strong authorization controls and human review.
- Expand into broader DNS and web-edge posture after the certificate workflow is reliable and explainable.
- Add per-tenant workflow integrations, customer-configured policy, and executive exposure trends.

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
