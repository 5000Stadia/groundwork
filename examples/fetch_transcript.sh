#!/usr/bin/env bash
# Fetches the real test transcript: Mixergy's 2015 interview with Brady Lewis
# (Allmoxy), a cabinet-shop operator walking through his shop's operations —
# faxes retyped into Excel, bad debt, no invoicing discipline. Official public
# transcript, published by Mixergy. Not committed to this repo (copyright);
# run this script to reproduce the example.
set -euo pipefail
cd "$(dirname "$0")"

URL="https://mixergy.com/interviews/brady-lewis-allmoxy/"
OUT="transcript.txt"
TMP="$(mktemp)"
trap 'rm -f "$TMP"' EXIT

curl -sL "$URL" -o "$TMP"

python3 - "$TMP" "$OUT" <<'PY'
import sys, re, html

raw = open(sys.argv[1], encoding="utf-8", errors="replace").read()

# The full transcript sits in <article class="transcript-view">...</article>.
m = re.search(r'<article class="transcript-view">(.*?)</article>', raw, flags=re.S)
if not m:
    sys.exit("transcript-view article not found — page layout changed?")
body = m.group(1)

# One paragraph per <p>; speaker names are in nested spans — strip tags inline.
paragraphs = re.findall(r"<p>(.*?)</p>", body, flags=re.S)
lines = []
for p in paragraphs:
    text = re.sub(r"<[^>]+>", "", p)
    text = html.unescape(text)
    text = re.sub(r"\s+", " ", text).strip()
    if text:
        lines.append(text)

out = "\n\n".join(lines)
open(sys.argv[2], "w", encoding="utf-8").write(out)
print(f"wrote {sys.argv[2]} ({len(out.split())} words)")
PY
