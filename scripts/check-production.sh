#!/usr/bin/env bash

set -euo pipefail

site_url="https://vellitas.com/"
www_url="https://www.vellitas.com/"
body_file=$(mktemp)
headers_file=$(mktemp)
trap 'rm -f "$body_file" "$headers_file"' EXIT

status_code=$(curl --fail --silent --show-error --max-time 25 \
  --output "$body_file" --dump-header "$headers_file" --write-out '%{http_code}' "$site_url")

if [[ "$status_code" != "200" ]]; then
  echo "Expected HTTP 200 from $site_url; received $status_code" >&2
  exit 1
fi

grep -Fq '<title>Vellitas | Outside-In Digital Certificate Intelligence</title>' "$body_file"
grep -Fq 'contact@vellitas.com' "$body_file"
grep -Fq 'Spencer Shearer' "$body_file"
grep -Fq 'Seth Shearer' "$body_file"
grep -Fq 'Fraser Mackenzie' "$body_file"
grep -Fq 'id="contact-form"' "$body_file"
grep -Fq 'id="methodology"' "$body_file"

for header in \
  'Strict-Transport-Security:' \
  'X-Content-Type-Options:' \
  'Content-Security-Policy:' \
  'Referrer-Policy:'; do
  if ! grep -Fiq "$header" "$headers_file"; then
    echo "Missing expected response header: $header" >&2
    exit 1
  fi
done

effective_url=$(curl --fail --silent --show-error --location --max-time 25 \
  --output /dev/null --write-out '%{url_effective}' "$www_url")

if [[ "$effective_url" != "$site_url" ]]; then
  echo "Expected $www_url to resolve to $site_url; received $effective_url" >&2
  exit 1
fi

for page in sample-report.html privacy.html data-practices.html robots.txt sitemap.xml assets/vellitas-shield-blue.svg; do
  curl --fail --silent --show-error --max-time 25 --output /dev/null "https://vellitas.com/$page"
done

if ! printf '' | openssl s_client -connect vellitas.com:443 -servername vellitas.com 2>/dev/null \
  | openssl x509 -checkend 1814400 -noout; then
  echo 'TLS certificate expires in fewer than 21 days.' >&2
  exit 1
fi

echo 'Vellitas production checks passed.'
