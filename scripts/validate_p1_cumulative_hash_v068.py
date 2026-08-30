#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'references' / 'community' / 'drive-p1-cumulative-hash-checkpoint-v0.6.8.json'
summary = json.loads(OUT.read_text(encoding='utf-8'))

assert summary['version'] == '0.6.8'
assert summary['milestone'] == 'CUMULATIVE_P1_VERIFIED_DEDUP_CHECKPOINT'
assert summary['drive_access_performed'] is False
assert summary['new_hashes_computed'] is False
assert summary['public_private_rows_tracked'] is False
assert summary['object_overlap_check'] == 'NOT_POSSIBLE_FROM_PUBLIC_AGGREGATES'

sources = []
for rel in summary['source_summaries']:
    p = ROOT / rel
    assert p.exists(), rel
    s = json.loads(p.read_text(encoding='utf-8'))
    sources.append(s)

assert len(sources) == 4
tranche_names = [s['tranche'] for s in sources]
batch_hashes = [s['private_batch_sha256'] for s in sources]
assert len(set(tranche_names)) == len(tranche_names)
assert len(set(batch_hashes)) == len(batch_hashes)
assert all(len(bytes.fromhex(h)) == 32 for h in batch_hashes)

families = sum(s['families'] for s in sources)
objects = sum(s['objects'] for s in sources)
bytes_hashed = sum(s['bytes_hashed'] for s in sources)
verified = sum(s['family_results'].get('BYTE_IDENTICAL_VERIFIED', 0) for s in sources)

assert families == summary['families'] == 25
assert objects == summary['objects'] == 50
assert bytes_hashed == summary['bytes_hashed'] == 13520744
assert verified == summary['family_results']['BYTE_IDENTICAL_VERIFIED'] == 25
assert summary['unique_private_batch_sha256'] == len(set(batch_hashes)) == 4

for key in ('work_ids_promoted', 'edition_ids_promoted', 'rights_promoted', 'scientific_evidence_promoted'):
    assert summary[key] == 0
    assert all(s[key] == 0 for s in sources)

print('AKASHICNET v0.6.8 CUMULATIVE P1 HASH PASS', {
    'tranches': len(sources),
    'families': families,
    'objects': objects,
    'bytes_hashed': bytes_hashed,
    'byte_identical_verified': verified,
    'unique_private_batches': len(set(batch_hashes)),
    'drive_access_performed': False,
    'new_hashes_computed': False,
    'rights_promoted': 0,
    'scientific_evidence_promoted': 0,
})
