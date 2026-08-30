#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SUMMARY = ROOT / 'references' / 'community' / 'drive-p1-tranche2b-hash-summary-v0.6.6.json'
s = json.loads(SUMMARY.read_text(encoding='utf-8'))
assert s['version'] == '0.6.6'
assert s['families'] == 5
assert s['objects'] == 10
assert s['bytes_hashed'] == 3645354
assert s['family_results'] == {'BYTE_IDENTICAL_VERIFIED': 5}
assert s['work_ids_promoted'] == 0
assert s['edition_ids_promoted'] == 0
assert s['rights_promoted'] == 0
assert s['scientific_evidence_promoted'] == 0
assert len(bytes.fromhex(s['private_batch_sha256'])) == 32
assert s['guardrail'].startswith('SHA-256 equality proves byte identity')
print('P1 tranche 2b aggregate v0.6.6 validation PASS')
print('families=5 objects=10 bytes=3645354 verified=5')
