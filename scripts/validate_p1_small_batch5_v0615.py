#!/usr/bin/env python3
import json
from pathlib import Path

P = Path('references/community/drive-p1-small-batch5-hash-summary-v0.6.15.json')

def fail(msg):
    raise SystemExit(f'FAIL: {msg}')

if not P.exists(): fail('summary missing')
d = json.loads(P.read_text())
expected = {
    'version':'0.6.15',
    'tranche':'P1_SMALL_BATCH5_OVERALL_ROWS_77_81',
    'families':5,
    'objects':10,
    'bytes_hashed':38013254,
    'hash_failures':0,
    'private_rows_tracked_in_public_repo':False,
    'authoritative_unique_families_before':76,
    'authoritative_unique_families_after':81,
    'unresolved_before':50,
    'unresolved_after':45,
    'work_ids_promoted':0,
    'edition_ids_promoted':0,
    'rights_promoted':0,
    'scientific_evidence_promoted':0,
}
for k,v in expected.items():
    if d.get(k) != v: fail(f'{k}: expected {v!r}, got {d.get(k)!r}')
fr=d.get('family_results',{})
if fr.get('BYTE_IDENTICAL_VERIFIED') != 5 or fr.get('NOT_BYTE_IDENTICAL') != 0:
    fail('family result counts incorrect')
if len(d.get('private_batch_sha256','')) != 64:
    fail('private batch digest malformed')
if d['authoritative_unique_families_after'] + d['unresolved_after'] != 126:
    fail('denominator arithmetic does not equal 126')
if 'physical byte identity only' not in d.get('guardrail',''):
    fail('guardrail missing')
print('PASS: P1 small batch5 v0.6.15 aggregate is valid')
