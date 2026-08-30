#!/usr/bin/env python3
import json
from pathlib import Path

PATH = Path("references/community/drive-p1-wave20-hash-summary-v0.6.8.json")

def fail(msg):
    raise SystemExit(msg)

data = json.loads(PATH.read_text())
expected = {
    "version": "0.6.9-reconciliation",
    "stage": "P1_LOW_COST",
    "wave": "rows_31_50",
    "families": 20,
    "objects": 40,
    "bytes_hashed": 33041612,
    "byte_identical_verified_families": 20,
    "byte_mismatch_families": 0,
    "hash_failures": 0,
    "status": "SUPERSEDED_OVERLAP_RECONCILED",
    "incremental_families_added": 0,
    "disputed_families_reverified": 5,
    "immediate_hash_recheck": "ALL_5_MATCHED_EXPECTED_SIZE_AND_SHA256_WITHIN_PAIR",
    "work_id_promotions": 0,
    "edition_id_promotions": 0,
    "rights_promotions": 0,
    "scientific_evidence_promotions": 0,
}
for key, value in expected.items():
    if data.get(key) != value:
        fail(f"{key}: expected {value!r}, got {data.get(key)!r}")
if data["byte_identical_verified_families"] + data["byte_mismatch_families"] != data["families"]:
    fail("family outcome counts must sum to total families")
if data.get("authoritative_source") != "references/community/drive-p1-large-wave20-hash-summary-v0.6.8.json":
    fail("authoritative overlap source must be explicit")
if "hash each fetched object immediately" not in data.get("guardrail", "").lower():
    fail("guardrail must require immediate hashing")
print("P1 wave20 overlap reconciliation v0.6.9 validated")
