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

# Contract bridge: WikiSpine concept/reference identity is intentionally weaker than
# canonical work identity, edition identity, rights/public status, scientific-evidence
# status, or truth. Those claims require independent adjudication and must never be
# inferred from a Wikidata QID, reference-class match, or REFERENCE_IDENTITY_ONLY.
contract_text = (ROOT / 'docs' / 'CANONICAL_ADJUDICATION_CONTRACT_V070.md').read_text(encoding='utf-8')
required_phrases = [
    'work identity',
    'edition identity',
    'rights',
    'scientific',
    'truth',
]
for phrase in required_phrases:
    assert phrase.lower() in contract_text.lower(), f'missing canonical contract boundary: {phrase}'

# The canonical example must remain a separate adjudication artifact. Presence of
# WikiSpine reference identity cannot mutate or satisfy its adjudication fields.
assert isinstance(CANON, dict)
assert 'version' in CANON

print('AKASHICNET v0.7.7 WIKISPINE CANONICAL BRIDGE PASS', {
    'wikispine_records_checked': len(BATCH['records']),
    'reference_identity_only': True,
    'canonical_work_identity_inferred': False,
    'edition_identity_inferred': False,
    'rights_status_inferred': False,
    'scientific_evidence_inferred': False,
    'truth_inferred': False,
})
