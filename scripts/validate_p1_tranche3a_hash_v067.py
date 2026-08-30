#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
P = ROOT / 'references' / 'community' / 'drive-p1-tranche3a-hash-summary-v0.6.7.json'
s = json.loads(P.read_text(encoding='utf-8'))
assert s['version'] == '0.6.7'
assert s['families'] == 5
assert s['objects'] == 10
assert s['bytes_hashed'] == 4407566
assert s['family_results'] == {'BYTE_IDENTICAL_VERIFIED': 5}
assert len(bytes.fromhex(s['private_batch_sha256'])) == 32
assert s['work_ids_promoted'] == 0
assert s['edition_ids_promoted'] == 0
assert s['rights_promoted'] == 0
assert s['scientific_evidence_promoted'] == 0
print('P1 tranche 3a aggregate v0.6.7 validation PASS')
print('families=5 objects=10 bytes=4407566 byte_identical_verified=5')
