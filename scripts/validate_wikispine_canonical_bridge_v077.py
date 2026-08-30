#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REF = ROOT / 'references' / 'community'

BATCH = json.loads((REF / 'wikispine-batch-f-v0.7.4.json').read_text(encoding='utf-8'))
CHECK = json.loads((REF / 'wikispine-checkpoint-v0.7.4.json').read_text(encoding='utf-8'))
CANON = json.loads((REF / 'canonical-adjudication-example-v0.7.0.json').read_text(encoding='utf-8'))

assert CHECK['reference_class'] == 'REFERENCE_ENCYCLOPEDIA'
assert CHECK['candidate_edges_default'] == 'HOLD'
assert CHECK['truth_inference_allowed'] is False
assert CHECK['rights_promotion_allowed'] is False
assert CHECK['scientific_evidence_promotion_allowed'] is False

for record in BATCH['records']:
    assert record['semantic_decision'] == 'REFERENCE_IDENTITY_ONLY'
    assert record['reference_class'] == 'REFERENCE_ENCYCLOPEDIA'
    assert record['truth_inference'] is False
    assert record['scientific_evidence'] is False

contract_text = (ROOT / 'docs' / 'CANONICAL_ADJUDICATION_CONTRACT_V070.md').read_text(encoding='utf-8')
required_phrases = ['work identity', 'edition identity', 'rights', 'scientific', 'truth']
for phrase in required_phrases:
    assert phrase.lower() in contract_text.lower(), f'missing canonical contract boundary: {phrase}'

assert isinstance(CANON, dict)
assert CANON.get('contract_version') == '0.7.0'
assert isinstance(CANON.get('records'), list) and CANON['records']
for record in CANON['records']:
    assert record['rights_promoted'] is False
    assert record['public_release_promoted'] is False
    assert record['scientific_evidence_promoted'] is False
    assert record['safety_or_efficacy_promoted'] is False

print('AKASHICNET v0.7.7 WIKISPINE CANONICAL BRIDGE PASS', {
    'wikispine_records_checked': len(BATCH['records']),
    'reference_identity_only': True,
    'canonical_work_identity_inferred': False,
    'edition_identity_inferred': False,
    'rights_status_inferred': False,
    'scientific_evidence_inferred': False,
    'truth_inferred': False,
})
