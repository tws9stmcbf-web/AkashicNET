#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REVIEWS = [
    ROOT / "references/source-integrity-batch12-review-v0.1.json",
    ROOT / "references/source-integrity-batch13-review-v0.1.json",
]
APPLICATION = ROOT / "references/source-integrity-batch13-repair-application-v0.1.json"
ALLOWED = {"AVAILABLE", "REDIRECTED", "UNAVAILABLE", "RATE_LIMITED", "UNCHECKED"}


def fail(msg):
    raise SystemExit(f"FAIL: {msg}")

for path in REVIEWS:
    if not path.is_file():
        fail(f"missing source-integrity review: {path.relative_to(ROOT)}")
    obj = json.loads(path.read_text())
    source = obj.get("source", {})
    url = source.get("original_url")
    status = source.get("live_status")
    guards = obj.get("guards", {})
    if not isinstance(url, str) or not url.startswith(("http://", "https://")):
        fail(f"invalid original URL in {path.name}")
    if status not in ALLOWED:
        fail(f"invalid live status in {path.name}: {status}")
    if guards.get("preserve_original_url") is not True:
        fail(f"original URL preservation not asserted in {path.name}")
    if guards.get("no_silent_replacement") is not True:
        fail(f"no-silent-replacement guard missing in {path.name}")
    if guards.get("unavailable_or_changed_does_not_mean_false") is not True:
        fail(f"availability/falsity separation missing in {path.name}")
    for key in ["truth_inference", "scientific_evidence_promotion", "rights_promotion", "website_promotion"]:
        if guards.get(key) is not False:
            fail(f"guard {key} must remain false in {path.name}")

if not APPLICATION.is_file():
    fail("missing batch13 repair application")
app = json.loads(APPLICATION.read_text())
guards = app.get("guards", {})
if guards.get("original_url_preserved") is not True:
    fail("batch13 application did not preserve original URL")
for key in ["silent_source_replacement", "truth_inference", "scientific_evidence_promotion", "rights_promotion", "website_promotion", "unavailable_source_treated_as_false"]:
    if guards.get(key) is not False:
        fail(f"batch13 application guard {key} must remain false")
if not app.get("source", {}).get("original_url"):
    fail("batch13 application source URL missing")

print("PASS: v0.14 source-integrity release guards preserve provenance and do not infer falsity from availability")
