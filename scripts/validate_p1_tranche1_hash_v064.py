#!/usr/bin/env python3
import csv
import json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REF = ROOT / 'references' / 'community'
CSV_PATH = REF / 'drive-p1-tranche1-hash-results-v0.6.4.csv'
SUMMARY_PATH = REF / 'drive-p1-tranche1-hash-summary-v0.6.4.json'

with CSV_PATH.open(newline='', encoding='utf-8') as f:
    rows = list(csv.DictReader(f))
summary = json.loads(SUMMARY_PATH.read_text(encoding='utf-8'))

assert len(rows) == 20, f'expected 20 object rows, got {len(rows)}'
assert summary['families'] == 10
assert summary['objects'] == 20
assert summary['bytes_hashed'] == 2522992
assert summary['family_results'] == {'BYTE_IDENTICAL_VERIFIED': 10}
assert summary['work_ids_promoted'] == 0
assert summary['edition_ids_promoted'] == 0
assert summary['rights_promoted'] == 0
assert summary['scientific_evidence_promoted'] == 0

families = defaultdict(list)
for r in rows:
    assert r['priority'] == 'P1_LOW_COST'
    assert r['family_result'] == 'BYTE_IDENTICAL_VERIFIED'
    assert r['acquisition_route'] == 'CONNECTED_GOOGLE_DRIVE_RAW_DOWNLOAD'
    assert r['work_identity_status'] == 'HOLD_PENDING_WORK_ADJUDICATION'
    assert not r['edition_id_promoted']
    assert r['rights_state'] == 'UNKNOWN_UNVERIFIED'
    assert r['scientific_evidence_state'] == 'NOT_EVALUATED'
    assert len(bytes.fromhex(r['sha256'])) == 32
    families[r['candidate_family_id']].append(r)

assert len(families) == 10, f'expected 10 families, got {len(families)}'
assert len({r['drive_id'] for r in rows}) == 20, 'duplicate Drive IDs in tranche'
assert sum(int(r['size_bytes']) for r in rows) == summary['bytes_hashed']

for fid, group in families.items():
    assert len(group) == 2, f'{fid}: expected 2 objects'
    assert len({r['name'] for r in group}) == 1, f'{fid}: names differ'
    assert len({r['size_bytes'] for r in group}) == 1, f'{fid}: sizes differ'
    assert len({r['sha256'] for r in group}) == 1, f'{fid}: hashes differ'

print('P1 tranche 1 hash evidence v0.6.4 validation PASS')
print('families=10 objects=20 bytes=2522992 byte_identical_verified=10')
