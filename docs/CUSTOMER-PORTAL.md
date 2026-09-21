# Customer portal architecture

This document defines the security boundary for a possible Vellitas customer front end. It is a roadmap design, not a statement that the portal is currently available.

## Core rule

A customer may search, filter, export, and remediate only assets in that customer's approved scope. The user interface is not the security boundary. Authorization must be enforced in every database query, object-store key, search index, report export, background job, and API request.

## Scope onboarding

1. **Collect seeds**: legal names, brands, domains, subsidiaries, acquisitions, known certificate names, ASNs, approved networks, cloud accounts, and important third parties.
2. **Prove or document authority**: prefer DNS TXT proof for root domains. Allow documented manual approval when corporate structure, contracts, or a security contact establish authority and DNS proof is impractical.
3. **Discover candidates**: correlate certificate SANs and subjects, Certificate Transparency, DNS and reverse DNS, RDAP/WHOIS, ASN and network ownership, redirects, shared public keys, hosting relationships, and naming similarity.
4. **Review candidates**: place related assets in a proposed-scope queue. Show the evidence for association and a confidence rating. Do not expose another customer's finding or confidential annotation while a candidate is under review.
5. **Approve or reject**: an authorized customer scope owner and, for ambiguous assets, a Vellitas reviewer approve the association. Record who approved it, why, and when.
6. **Recertify**: review scope quarterly and when ownership, acquisitions, divestitures, DNS control, or registration information changes.

## Tenant isolation

- Attach an immutable `tenant_id` to every asset, observation, finding, policy, report, script, job, export, and audit event.
- Enforce tenant predicates with PostgreSQL row-level security or an equivalent data-layer control; deny access when tenant context is absent.
- Use service roles with least privilege and separate read, remediation-authoring, approval, and administration permissions.
- Require SSO and MFA for customer access, with role-based access for viewers, analysts, approvers, and tenant administrators.
- Partition search indexes and object-store paths by tenant, use short-lived signed download links, and prevent predictable identifiers from becoming authorization controls.
- Log sign-in, search, export, scope, policy, script, approval, and administrative events.
- Test cross-tenant access as a release-blocking security requirement.

## Search and reporting

The portal opens on the approved tenant portfolio. A customer can narrow or broaden filters within that set by hostname, domain, subsidiary, issuer, validity, cipher or protocol, region, network, finding type, severity, confidence, owner, or remediation state. Clearing a filter returns to the tenant portfolio—not the global Vellitas corpus.

Search results can be converted into a remediation report or a controlled batch of remediation artifacts. Exports inherit the same tenant and role checks as the interactive view.

## Remediation scripts

Scripts are generated for a specific finding, target, technology, and observed configuration. Before release they require template allowlisting, parameter validation, secrets exclusion, static checks, Vellitas review, customer approval, a dry-run or plan, rollback guidance, integrity signing, and a recorded execution result. The default product delivers the script for controlled execution; it does not run changes automatically.

## Suggested implementation sequence

1. Evidence and scope data model, including proposed and approved assets.
2. Administrator-only scope review and tenant-isolation tests.
3. Read-only customer portfolio, search, and report export.
4. SSO/MFA, customer roles, policies, notification settings, and audit views.
5. Remediation work tracking and script generation.
6. Explicitly approved integrations and, only after operational maturity, narrowly scoped execution.
