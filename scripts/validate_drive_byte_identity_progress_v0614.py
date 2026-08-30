#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECKPOINT = ROOT / "references/community/drive-byte-identity-progress-checkpoint-v0.6.14.json"

with CHECKPOINT.open(encoding="utf-8") as f:
    c = json.load(f)

assert c["review_family_denominator"] == 126
assert c["authoritative_unique_families_adjudicated"] == 76
assert c["unresolved_families"] == 50
assert c["authoritative_unique_families_adjudicated"] + c["unresolved_families"] == c["review_family_denominator"]
assert c["authoritative_objects_hashed"] == 158
assert c["authoritative_bytes_hashed"] == 156990596
assert c["family_results"] == {"BYTE_IDENTICAL_VERIFIED": 76, "BYTE_MISMATCH": 0}
assert c["hash_failures"] == 0
assert c["overlap_reconciliation"]["pr_40_authoritative"] is True
assert c["overlap_reconciliation"]["pr_44_incremental_families"] == 0
assert c["latest_queue_window"] == "overall_rows_72_76"

expected_sources = [
    "references/community/drive-p0-hash-summary-v0.6.3.json",
    "references/community/drive-p1-cumulative-hash-checkpoint-v0.6.8.json",
    "references/community/drive-p1-wave20-reconciliation-v0.6.9.json",
    "references/community/drive-p1-small-batch5-hash-summary-v0.6.10.json",
    "references/community/drive-p1-small-batch5-hash-summary-v0.6.11.json",
    "references/community/drive-p1-small-batch5-hash-summary-v0.6.12.json",
    "references/community/drive-p1-small-batch5-hash-summary-v0.6.13.json",
    "references/community/drive-p1-small-batch5-hash-summary-v0.6.14.json",
]
assert c["source_summaries"] == expected_sources
for rel in expected_sources:
    assert (ROOT / rel).exists(), rel

privacy = c["privacy_boundary"]
for key in ("drive_ids_public", "filenames_public", "paths_public", "per_object_sha256_public"):
    assert privacy[key] is False

promotions = c["promotions"]
assert set(promotions) == {"work_identity", "edition_identity", "rights", "public_release", "scientific_evidence", "truth"}
assert all(value == 0 for value in promotions.values())

rule = c["execution_rule"]
assert "hash immediately" in rule
assert "persist digest privately" in rule

guardrail = c["guardrail"].lower()
for phrase in ("byte identity only", "work identity", "edition identity", "rights", "truth", "scientific-evidence"):
    assert phrase in guardrail

print("drive byte-identity progress checkpoint v0.6.14: OK")
