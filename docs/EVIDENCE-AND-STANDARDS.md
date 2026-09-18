# Evidence, vendor risk, and standards

This document records the authoritative evidence behind Vellitas marketing statements and the standards used to explain assessment findings. It is not a legal opinion, a certification, or a claim that the current product would have prevented every incident below.

## Defensible public statement

> Attackers have used misissued and stolen certificates, DNS hijacking, and actor-controlled infrastructure to impersonate trusted services and harvest credentials. Vellitas correlates certificate, DNS, network, geographic, and historical evidence to surface changes that warrant investigation.

A geographic, network, issuer, or configuration change is a risk signal—not proof of compromise. CDNs, cloud migrations, disaster recovery, acquisitions, and authorized service providers can create legitimate changes. Reports must show the observed evidence, corroborating context, confidence, and the validation required before remediation.

## Documented vendor pathways

### Target and Fazio Mechanical Services — 2013

A U.S. Senate staff analysis reported that attackers stole credentials from Fazio Mechanical Services, a small Pennsylvania HVAC contractor with remote access to Target for billing, contract submission, and project management. Attackers used vendor access as a foothold, and information associated with as many as 110 million Target customers was taken.

- Evidence: [U.S. Senate staff report](https://www.commerce.senate.gov/public/_cache/files/24d3c229-4f2f-405d-b8db-a3a67f183883/23E30AA955B5C00FE57CFD709621592C.2014-0325-target-kill-chain-analysis.pdf)
- Lesson: A small supplier can create a large attack path. Vendor MFA, least privilege, segmentation, access expiry, and continuous review should reflect the access granted.
- Product boundary: An outside-in assessment can evaluate the vendor's public exposure, but it cannot prove the security of private credentials, internal segmentation, or Target's access controls without additional authorization.

### Ticketmaster and Inbenta — 2018

The UK Information Commissioner's Office found that an attacker inserted malicious code into a chatbot hosted by Ticketmaster's vendor, Inbenta. Ticketmaster included the third-party JavaScript on payment pages, enabling the malicious code to collect names, card details, CVVs, usernames, and passwords entered by customers.

- Evidence: [UK ICO penalty notice](https://ico.org.uk/media/action-weve-taken/mpns/2618599/ticketmaster-uk-limited-mpn.pdf)
- Lesson: Third-party code loaded into a trusted customer workflow becomes part of that workflow's effective attack surface.
- Product boundary: Certificate and DNS monitoring can identify infrastructure and ownership changes around a third-party dependency, but detecting malicious JavaScript requires web-content integrity and dependency controls beyond the current certificate assessment.

### Kaseya VSA — 2021

Kaseya reported that attackers exploited zero-day vulnerabilities in its VSA product, bypassed authentication, and used standard management functionality to deploy ransomware. Fewer than 60 direct Kaseya customers were compromised, but many were managed service providers; Kaseya estimated that fewer than 1,500 downstream businesses were affected.

- Evidence: [Kaseya incident overview and technical details](https://helpdesk.kaseya.com/hc/en-gb/articles/4403584098961-Incident-Overview-Technical-Details)
- Corroboration: [U.S. Department of Justice case description](https://www.justice.gov/usao-ndtx/pr/ukrainian-arrested-and-charged-ransomware-attack-kaseya)
- Lesson: Privileged management software and MSP relationships can concentrate risk across many small organizations that do not contract directly with the original technology vendor.
- Product boundary: Outside-in evidence can identify exposed management services, certificates, networks, and changes, but it does not replace authenticated product vulnerability management.

### SolarWinds Orion — 2020

CISA documented that an advanced actor added malicious code to multiple SolarWinds Orion versions and used the supply-chain compromise for initial access to selected government, critical-infrastructure, and private-sector organizations. The actor established persistent access, compromised federated identity and Microsoft 365 environments, and exfiltrated sensitive data.

- Evidence: [CISA risk guidance](https://www.cisa.gov/sites/default/files/publications/CISA_Insights_SolarWinds-and-AD-M365-Compromise-Risk-Decisions-for-Leaders.pdf)
- Lesson: A trusted vendor, signed update, or previously approved service must still be monitored throughout its lifecycle.
- Product boundary: Public certificate observation is one layer of assurance; software provenance, build integrity, identity, endpoint detection, and incident response are separate controls.

## Documented certificate and TLS pathways

### Sea Turtle — 2017–2019

Cisco Talos documented DNS hijacking, CA-signed impersonation certificates, and stolen SSL certificates deployed on actor-controlled servers to harvest credentials. Talos identified at least 40 organizations across 13 countries. In one example, the same self-signed Cisco ASA certificate was observed on an actor-controlled IP address and an address associated with the victim.

- Evidence: [Cisco Talos investigation](https://blog.talosintelligence.com/seaturtle/)
- Relevant signals: certificate or public-key reuse, new IP/ASN/provider/country, DNS and nameserver changes, issuer changes, self-signed appliance certificates, and short-lived deployments.

### DigiNotar — 2011

A compromised certificate authority issued fraudulent certificates for Google and other services. ENISA reported that false certificates were used to eavesdrop on users in Iran. Approximately 300,000 Iranian OCSP requests were an indicator of possible affected users, not a definitive victim count.

- Evidence: [ENISA analysis](https://www.enisa.europa.eu/sites/default/files/all_files/Operation_Black_Tulip_v2.pdf)
- Relevant signals: unauthorized issuance, unexpected CA, geographic concentration, and infrastructure inconsistent with the legitimate operator.

### Equifax — 2017

A U.S. House investigation found that an internal certificate used to inspect encrypted traffic expired 19 months before the breach was discovered, restricting visibility into exfiltration affecting approximately 148 million people. The initial entry point was an unpatched Apache Struts vulnerability.

- Evidence: [U.S. House investigation](https://oversight.house.gov/wp-content/uploads/2018/12/Equifax-Report.pdf)
- Boundary: The failed certificate was internal. Vellitas must not suggest that its standard public-facing assessment would have discovered or prevented this monitoring failure.

### Canadian government Heartbleed breach — 2014

A Government of Canada review documented remote exploitation and data exfiltration through the OpenSSL Heartbleed flaw across 12 departments, including at least 900 taxpayer Social Insurance Numbers.

- Evidence: [Government of Canada review](https://www.canada.ca/content/dam/nsicop-cpsnr/documents/2022-cyber-attack-framework-report-en.pdf)
- Boundary: Certificate metadata alone cannot detect Heartbleed. Safe TLS implementation testing is an adjacent capability requiring explicit scope, technical safeguards, and product verification before it is marketed as available.

## Weak protocols and cipher language

Public breach reports rarely identify one cipher suite as the sole cause of a major incident. Vellitas should describe obsolete protocols and weak cipher suites as **known exploitable exposure**, not claim that each configuration has caused a named breach.

- [IETF RFC 8996](https://datatracker.ietf.org/doc/html/rfc8996) formally deprecates TLS 1.0 and TLS 1.1 because they lack support for current cryptographic mechanisms and increase downgrade and misconfiguration risk.
- [NIST SP 800-52 Rev. 2](https://csrc.nist.gov/pubs/sp/800/52/r2/final) requires modern TLS and approved cipher suites for federal systems and provides guidance for certificate and TLS configuration.

## Certificate Transparency operating requirement

[CISA's DNS infrastructure tampering guidance](https://www.cisa.gov/sites/default/files/publications/CISAInsights-Cyber-MitigateDNSInfrastructureTampering_S508C.pdf) recommends monitoring Certificate Transparency logs. Vellitas should treat continuous CT monitoring as a production capability only after the following are operating and verified:

1. Ingest and deduplicate current public CT entries from redundant sources.
2. Match exact domains, wildcard names, SANs, subsidiaries, approved brand variants, and reviewed name-similarity candidates.
3. Preserve issuer, serial number, validity, fingerprint, SPKI/public-key hash, log timestamp, first-seen time, and source-log evidence.
4. Correlate issuance with DNS, IP, ASN, provider, geolocation, current deployments, and customer policy.
5. Alert on an unexpected issuer, new key, unusual SAN expansion, short lifetime, suspicious name, or issuance inconsistent with approved infrastructure.
6. Score confidence and suppress known renewals, CDN changes, and other approved patterns.
7. Preserve the raw evidence needed to reproduce the finding and provide revocation or validation steps.

Until those controls are verified, public material should continue to label continuous, event-driven CT monitoring as roadmap work. Current assessments may use public CT evidence during analyst-led investigation without claiming continuous coverage.

## Vellitas correlation baseline

- Certificate fingerprint and public-key reuse across IP addresses.
- New countries, ASNs, cloud providers, or hosting networks.
- Certificate Transparency issuance and unexpected issuers.
- DNS A, AAAA, CNAME, MX, and NS changes.
- Short-lived certificate and DNS changes.
- New or unusual subject alternative names.
- Self-signed and temporary appliance certificates.
- Revocation, OCSP, and certificate-chain status.
- TLS versions, accepted cipher suites, and downgrade exposure.
- Historical first-seen, last-seen, and infrastructure movement.

## Standards and authoritative guidance map

| Area | Reference | How Vellitas should use it |
| --- | --- | --- |
| Obsolete TLS | [IETF RFC 8996](https://datatracker.ietf.org/doc/html/rfc8996) | Explain findings for TLS 1.0 and 1.1 support and downgrade exposure. |
| TLS configuration | [NIST SP 800-52 Rev. 2](https://csrc.nist.gov/pubs/sp/800/52/r2/final) | Reference modern protocol, approved cipher, certificate, and extension expectations where applicable. |
| Certificate Transparency | [CISA DNS tampering guidance](https://www.cisa.gov/sites/default/files/publications/CISAInsights-Cyber-MitigateDNSInfrastructureTampering_S508C.pdf) | Support CT monitoring, DNS-history correlation, and investigation of unauthorized issuance. |
| Supplier governance | [NIST CSF 2.0 C-SCRM Quick-Start Guide](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.1305.pdf) | Map vendor inventory, criticality, requirements, due diligence, continuous monitoring, and incident coordination to GV.SC outcomes. |
| Supply-chain program | [NIST SP 800-161 Rev. 1](https://csrc.nist.gov/pubs/sp/800/161/r1/upd1/final) | Place outside-in evidence within a broader product-and-service supply-chain risk program. |
| Managed services | [CISA/NSA/FBI and international MSP guidance](https://www.cisa.gov/news-events/news/cisa-nsa-fbi-and-international-cyber-authorities-issue-cybersecurity-advisory-protect-managed) | Support contractual security requirements, secure remote access, MFA, logging, monitoring, and shared incident responsibilities. |
| Payment service providers | [PCI SSC Requirement 12.8 guidance](https://www.pcisecuritystandards.org/faqs/1312/) | Where in scope, support third-party inventory, due diligence, agreements, responsibility mapping, and at-least-annual status monitoring. |

Standards references should be selected based on the customer's scope, industry, and contractual obligations. Reports should distinguish an observed technical result, a mapped control expectation, and any formal compliance conclusion. Vellitas does not state that a customer is certified or compliant unless a separately authorized qualified assessment supports that conclusion.
