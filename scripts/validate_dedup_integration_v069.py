#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REF = ROOT / 'references' / 'community'
SRC = REF / 'drive-p1-cumulative-hash-checkpoint-v0.6.8.json'
OUT = REF / 'dedup-integration-checkpoint-v0.6.9.json'

src = json.loads(SRC.read_text(encoding='utf-8'))
out = json.loads(OUT.read_text(encoding='utf-8'))

assert src['version'] == '0.6.8'
assert out['version'] == '0.6.9'
assert out['source_checkpoint'].endswith('drive-p1-cumulative-hash-checkpoint-v0.6.8.json')

assert src['families'] == out['verified_duplicate_families'] == 25
assert src['objects'] == out['verified_physical_objects'] == 50
assert src['family_results']['BYTE_IDENTICAL_VERIFIED'] == 25
assert out['dedup_logical_slots'] == 25
assert out['potential_redundant_physical_copies'] == 25
assert out['verified_physical_objects'] - out['dedup_logical_slots'] == out['potential_redundant_physical_copies']

assert out['collapse_basis'] == 'BYTE_IDENTICAL_VERIFIED_SHA256'
assert out['integration_mode'] == 'AGGREGATE_CAPACITY_ONLY'
assert out['object_level_mapping_available_publicly'] is False
assert out['object_level_collapse_performed'] is False
assert out['private_mapping_required_for_object_level_collapse'] is True
assert out['existing_v0_17_dedup_semantics_preserved'] is True

assert out['drive_access_performed'] is False
assert out['new_hashes_computed'] is False
assert out['work_identity_promoted'] is False
assert out['edition_identity_promoted'] is False
assert out['rights_promoted'] is False
assert out['scientific_evidence_promoted'] is False
assert out['truth_inference'] is False

# The cumulative public checkpoint itself must remain conservative.
assert src['drive_access_performed'] is False
assert src['new_hashes_computed'] is False
assert src['work_ids_promoted'] == 0
assert src['edition_ids_promoted'] == 0
assert src['rights_promoted'] == 0
assert src['scientific_evidence_promoted'] == 0

print('AKASHICNET v0.6.9 DEDUP INTEGRATION PASS', {
    'verified_duplicate_families': 25,
    'verified_physical_objects': 50,
    'dedup_logical_slots': 25,
    'potential_redundant_physical_copies': 25,
    'integration_mode': 'AGGREGATE_CAPACITY_ONLY',
    'object_level_collapse_performed': False,
    'drive_access_performed': False,
    'new_hashes_computed': False,
    'rights_promoted': False,
    'scientific_evidence_promoted': False,
})
