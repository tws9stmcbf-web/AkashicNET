#!/usr/bin/env python3
import json
from pathlib import Path

p = Path('references/community/wikispine-batch-g-people-v0.7.7a.json')
d = json.loads(p.read_text(encoding='utf-8'))
assert d['version'] == '0.7.7a'
assert len(d['records']) == 2
assert {r['entity_type'] for r in d['records']} == {'PERSON'}
assert {r['wikidata_qid'] for r in d['records']} == {'Q125249', 'Q41532'}
assert len({r['wikidata_qid'] for r in d['records']}) == 2
for r in d['records']:
    assert r['resolution_state'] == 'RESOLVED_HIGH_PRECISION'
    assert r['reference_class'] == 'REFERENCE_ENCYCLOPEDIA'
    assert r['semantic_decision'] == 'REFERENCE_IDENTITY_ONLY'
    assert r['truth_inference'] is False
    assert r['scientific_evidence'] is False
for key in ('rights_promotion_allowed','scientific_evidence_promotion_allowed','truth_inference_allowed','drive_access_performed'):
    assert d['guardrails'][key] is False
assert d['guardrails']['candidate_edges_default'] == 'HOLD'
print('AKASHICNET v0.7.7a WIKISPINE PEOPLE PASS', [r['label'] for r in d['records']])
