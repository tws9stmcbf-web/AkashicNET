#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SUMMARY = ROOT / 'references' / 'community' / 'drive-p1-large-wave20-hash-summary-v0.6.8.json'

s = json.loads(SUMMARY.read_text(encoding='utf-8'))
assert s['version'] == '0.6.8'
assert s['tranche'] == 'P1_LARGE_WAVE_20_FAMILIES'
assert s['families'] == 20
assert s['objects'] == 40
assert s['bytes_hashed'] == 33041612
assert s['family_results'] == {'BYTE_IDENTICAL_VERIFIED': 20}
assert len(s['private_batch_sha256']) == 64
int(s['private_batch_sha256'], 16)
assert s['work_ids_promoted'] == 0
assert s['edition_ids_promoted'] == 0
assert s['rights_promoted'] == 0
assert s['scientific_evidence_promoted'] == 0
assert 'byte identity' in s['guardrail'].lower()
assert 'canonical work identity' in s['guardrail'].lower()
print('P1 large wave20 aggregate v0.6.8 validation PASS')
print('families=20 objects=40 bytes=33041612 byte_identical_verified=20')
