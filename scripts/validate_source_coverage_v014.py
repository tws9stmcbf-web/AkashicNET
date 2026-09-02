#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "references/community/source-coverage-v0.14.json"
ALLOWED = {"AVAILABLE", "REDIRECTED", "UNAVAILABLE", "RATE_LIMITED", "UNCHECKED"}


def fail(msg):
    raise SystemExit(f"FAIL: {msg}")

if not MANIFEST.is_file():
    fail("missing v0.14 source coverage manifest")

m = json.loads(MANIFEST.read_text())
if m.get("target_version") != "0.14.0-beta.1":
    fail("wrong target version")
if m.get("status") != "PARTIAL_FAIL_CLOSED":
    fail("coverage manifest must remain PARTIAL_FAIL_CLOSED until denominator is proven")
if m.get("coverage_complete") is not False:
    fail("coverage must not be declared complete yet")
if m.get("release_ready") is not False:
    fail("source coverage must not declare release readiness")

records = m.get("records")
if not isinstance(records, list) or not records:
    fail("source coverage records missing")

seen_ids = set()
seen_urls = set()
for rec in records:
    sid = rec.get("source_id")
    url = rec.get("original_url")
    status = rec.get("status")
    review = rec.get("review_record")
    if not sid or sid in seen_ids:
        fail(f"missing or duplicate source_id: {sid}")
    if not isinstance(url, str) or not url.startswith(("http://", "https://")):
        fail(f"invalid original_url for {sid}")
    if url in seen_urls:
        fail(f"duplicate original_url without explicit provenance linkage: {url}")
    if status not in ALLOWED:
        fail(f"invalid status for {sid}: {status}")
    if not review or not (ROOT / review).is_file():
        fail(f"missing review record for {sid}: {review}")
    review_obj = json.loads((ROOT / review).read_text())
    source = review_obj.get("source", {})
    if source.get("source_id") != sid:
        fail(f"source_id mismatch in {review}")
    if source.get("original_url") != url:
        fail(f"original URL mismatch in {review}")
    if source.get("live_status") != status:
        fail(f"status mismatch in {review}")
    seen_ids.add(sid)
    seen_urls.add(url)

if set(m.get("allowed_statuses", [])) != ALLOWED:
    fail("allowed source statuses changed")

inv = m.get("invariants", {})
required_true = ["original_url_preserved"]
required_false = [
    "silent_replacement",
    "unavailable_or_changed_means_false",
    "truth_inference",
    "scientific_evidence_promotion",
    "rights_promotion",
    "private_drive_promotion",
]
for key in required_true:
    if inv.get(key) is not True:
        fail(f"invariant must be true: {key}")
for key in required_false:
    if inv.get(key) is not False:
        fail(f"invariant must be false: {key}")

print(f"PASS: v0.14 source coverage contract validates {len(records)} reviewed source records and remains fail-closed")
