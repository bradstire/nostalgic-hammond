#!/usr/bin/env bash
# Re-creates public/images from the live site and verifies against MANIFEST.sha1 (run inside the unzipped source folder).
set -euo pipefail
grep ' public/' MANIFEST.sha1 | while read -r sha path; do
  mkdir -p "$(dirname "$path")"
  [ -f "$path" ] || curl -sS -o "$path" "https://www.nostalgichammond.com/${path#public/}"
done
sha1sum -c MANIFEST.sha1 --quiet && echo "ALL FILES VERIFIED"
