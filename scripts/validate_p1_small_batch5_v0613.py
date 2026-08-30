#!/usr/bin/env python3
import json
from pathlib import Path

P = Path('references/community/drive-p1-small-batch5-hash-summary-v0.6.13.json')
d = json.loads(P.read_text(encoding='utf-8'))

expected = {
    'version': '0.6.13',
    'stage': 'P1_LOW_COST',
    'queue_window': 'overall_rows_67_71',
    'families': 5,
    'objects': 10,
    'bytes_hashed': 23503894,
    'byte_identical_verified_families': 5,
    'byte_mismatch_families': 0,
    'hash_failures': 0,
    'unresolved_families_before': 60,
    'unresolved_families_after': 55,
    'work_id_promotions': 0,
    'edition_id_promotions': 0,
    'rights_promotions': 0,
    'public_release_promotions': 0,
    'scientific_evidence_promotions': 0,
}
for k,v in expected.items():
    assert d.get(k) == v, f'{k}: expected {v!r}, got {d.get(k)!r}'
assert d['byte_identical_verified_families'] + d['byte_mismatch_families'] == d['families']
assert len(d['private_batch_sha256']) == 64
int(d['private_batch_sha256'], 16)
for forbidden in ('drive_id','filename','parent_path','sha256s'):
    assert forbidden not in d, f'forbidden object-level field: {forbidden}'
assert 'hash immediately' in d['execution_rule'].lower()
assert 'physical byte identity only' in d['guardrail'].lower()
assert 'canonical work identity' in d['guardrail'].lower()
print('P1 small batch5 aggregate v0.6.13 validation PASS')
print('families=5 objects=10 bytes=23503894 verified=5 unresolved=55')
