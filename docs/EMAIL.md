# Website email

The public website uses `contact@vellitas.com`. It is a Google Workspace alternate email address for the existing company user, so messages to the alias arrive in the same inbox without an additional Workspace license.

The personal mailbox address is not present in the checked-in website source.

## Replying from the alias

Receiving through an alias does not automatically make it the outgoing sender. The Workspace alias is active, but Gmail's one-time **Settings → Accounts and Import → Send mail as** setup is still required before replies can originate from `contact@vellitas.com`. Make it the default for website correspondence if desired and enable replying from the address to which a message was sent.

## Spam and address harvesting

Any email address published in HTML can be collected by automated crawlers. Using the role alias limits exposure of the primary mailbox and makes the public address easier to filter or replace, but it does not prevent spam.

If spam becomes significant, replace direct `mailto:` actions with a server-side contact form protected by rate limiting, bot detection, validation, and logging. Do not place mail provider credentials in client-side JavaScript.

## Domain authentication

The following Google Workspace authentication records were published in Route 53 on September 17, 2026:

- Apex SPF: `v=spf1 include:_spf.google.com ~all`
- Google DKIM: 2048-bit key using selector `google`; Workspace authentication was started after public DNS verification.
- DMARC: monitoring mode (`p=none`) with aggregate reports delivered to a private reporting alias.

Keep DMARC in monitoring mode while collecting reports. After legitimate senders are inventoried and SPF/DKIM alignment is stable, move deliberately to `quarantine` and then `reject`. Website DNS records and email DNS records are independent; do not remove Google MX records when changing the website.

Do not check the private reporting alias, DKIM key material, administrator URLs, or test recipients into the public repository.
