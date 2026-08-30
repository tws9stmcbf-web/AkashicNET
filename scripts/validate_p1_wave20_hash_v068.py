#!/usr/bin/env python3
import json
from pathlib import Path

PATH = Path("references/community/drive-p1-wave20-hash-summary-v0.6.8.json")

def fail(msg):
    raise SystemExit(msg)

data = json.loads(PATH.read_text())
expected = {
    "version": "0.6.8",
    "stage": "P1_LOW_COST",
    "wave": "rows_31_50",
    "families": 20,
    "objects": 40,
    "bytes_hashed": 33504806,
    "byte_identical_verified_families": 15,
    "byte_mismatch_families": 5,
    "hash_failures": 0,
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
if "byte identity only" not in data.get("guardrail", "").lower():
    fail("guardrail must preserve byte-identity-only semantics")
print("P1 wave20 v0.6.8 aggregate validated")
