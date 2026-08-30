import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REF = ROOT / 'references' / 'community'


def test_wikispine_reference_identity_is_fail_closed():
    batch = json.loads((REF / 'wikispine-batch-f-v0.7.4.json').read_text(encoding='utf-8'))
    checkpoint = json.loads((REF / 'wikispine-checkpoint-v0.7.4.json').read_text(encoding='utf-8'))

    assert checkpoint['candidate_edges_default'] == 'HOLD'
    assert checkpoint['truth_inference_allowed'] is False
    assert checkpoint['rights_promotion_allowed'] is False
    assert checkpoint['scientific_evidence_promotion_allowed'] is False

    for record in batch['records']:
        assert record['semantic_decision'] == 'REFERENCE_IDENTITY_ONLY'
        assert record['truth_inference'] is False
        assert record['scientific_evidence'] is False


def test_canonical_contract_keeps_stronger_claims_separate():
    text = (ROOT / 'docs' / 'CANONICAL_ADJUDICATION_CONTRACT_V070.md').read_text(encoding='utf-8').lower()
    for phrase in ('work identity', 'edition identity', 'rights', 'scientific', 'truth'):
        assert phrase in text
