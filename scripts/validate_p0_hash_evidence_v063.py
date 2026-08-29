#!/usr/bin/env python3
import csv
import json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REF = ROOT / 'references' / 'community'
RESULTS = REF / 'drive-p0-hash-results-v0.6.3.csv'
SUMMARY = REF / 'drive-p0-hash-summary-v0.6.3.json'
EXPECTED_FAMILIES = 6
EXPECTED_OBJECTS = 18
EXPECTED_BYTES = 14838834

with RESULTS.open(newline='', encoding='utf-8') as f:
    rows = list(csv.DictReader(f))
summary = json.loads(SUMMARY.read_text(encoding='utf-8'))

assert len(rows) == EXPECTED_OBJECTS, f'expected {EXPECTED_OBJECTS} rows, got {len(rows)}'
assert len({r['drive_id'] for r in rows}) == EXPECTED_OBJECTS, 'duplicate Drive IDs in P0 evidence'
assert sum(int(r['downloaded_size_bytes']) for r in rows) == EXPECTED_BYTES
assert all(r['expected_size_bytes'] == r['downloaded_size_bytes'] for r in rows), 'size mismatch'
assert all(r['hash_status'] == 'HASHED' for r in rows), 'unhashed P0 object'
assert all(r['acquisition_route'] == 'CONNECTED_GOOGLE_DRIVE_RAW_DOWNLOAD' for r in rows)
assert all(r['canonical_promotion_status'] == 'HOLD_PENDING_WORK_ADJUDICATION' for r in rows)
assert all(r['rights_state'] == 'UNKNOWN_UNVERIFIED' for r in rows)
assert all(r['scientific_evidence_state'] == 'NOT_EVALUATED' for r in rows)

families = defaultdict(list)
for row in rows:
    digest = row['sha256']
    assert len(digest) == 64
    bytes.fromhex(digest)
    families[row['candidate_family_id']].append(row)

assert len(families) == EXPECTED_FAMILIES
for fid, group in families.items():
    assert len(group) == 3, f'{fid}: expected three objects'
    assert len({r['sha256'] for r in group}) == 1, f'{fid}: hash mismatch'
    assert len({r['name'] for r in group}) == 1, f'{fid}: name mismatch'
    assert len({r['expected_size_bytes'] for r in group}) == 1, f'{fid}: expected-size mismatch'
    assert all(r['family_byte_identity_status'] == 'BYTE_IDENTICAL_VERIFIED' for r in group)

assert summary['p0_families'] == EXPECTED_FAMILIES
assert summary['p0_objects'] == EXPECTED_OBJECTS
assert summary['bytes_hashed'] == EXPECTED_BYTES
assert summary['hash_failures'] == 0
assert summary['family_results'] == {'BYTE_IDENTICAL_VERIFIED': EXPECTED_FAMILIES}
assert summary['byte_identical_verified_families'] == sorted(families)
assert summary['work_ids_promoted'] == 0
assert summary['edition_ids_promoted'] == 0
assert summary['rights_promoted'] == 0
assert summary['scientific_evidence_promoted'] == 0

print('P0 hash evidence v0.6.3 validation PASS')
print(f'families={len(families)} objects={len(rows)} bytes={EXPECTED_BYTES}')
