# Website email

The public website uses `contact@vellitas.com`. It is a Google Workspace alternate email address for the existing company user, so messages to the alias arrive in the same inbox without an additional Workspace license.

The personal mailbox address is not present in the checked-in website source.

## Replying from the alias

Receiving through an alias does not automatically make it the outgoing sender. In Gmail, add `contact@vellitas.com` under **Settings → Accounts and Import → Send mail as**, make it the default for website correspondence if desired, and enable replying from the address to which a message was sent.

## Spam and address harvesting

Any email address published in HTML can be collected by automated crawlers. Using the role alias limits exposure of the primary mailbox and makes the public address easier to filter or replace, but it does not prevent spam.

If spam becomes significant, replace direct `mailto:` actions with a server-side contact form protected by rate limiting, bot detection, validation, and logging. Do not place mail provider credentials in client-side JavaScript.

## Domain authentication

Before using the alias for outbound mail, verify Google Workspace email authentication in DNS:

- SPF authorizes Google to send mail for `vellitas.com`.
- DKIM cryptographically signs outbound mail.
- DMARC defines handling and reporting for messages that fail alignment.

Roll DMARC out gradually, beginning with monitoring, after SPF and DKIM are verified. Website DNS records and email DNS records are independent; do not remove Google MX records when changing the website.
