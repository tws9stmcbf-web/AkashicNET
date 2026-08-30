import copy
import importlib.util
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'scripts' / 'validate_retrieval_evidence_bridge_v078.py'
REF = ROOT / 'references' / 'community'

spec = importlib.util.spec_from_file_location('validate_retrieval_evidence_bridge_v078', SCRIPT)
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)


def load_inputs():
    schema = json.loads((REF / 'unified-retrieval-schema-v0.25.json').read_text(encoding='utf-8'))
    fixtures = json.loads((REF / 'retrieval-fixtures-v0.25.json').read_text(encoding='utf-8'))
    evidence = (ROOT / 'docs' / 'canonical-evidence-v01.md').read_text(encoding='utf-8')
    return schema, fixtures, evidence


def test_retrieval_evidence_bridge_accepts_repository_contract():
    schema, fixtures, evidence = load_inputs()
    result = validator.validate_retrieval_contract(schema, fixtures, evidence)
    assert result['truth_inference'] is False
    assert result['rights_promotion'] is False
    assert result['scientific_evidence_promotion'] is False


@pytest.mark.parametrize(
    'guard',
    [
        'truth_inference_allowed',
        'rights_promotion_allowed',
        'scientific_evidence_promotion_allowed',
        'ranking_changes_semantic_decision',
    ],
)
def test_rejects_forbidden_promotion_or_semantic_mutation(guard):
    schema, fixtures, evidence = load_inputs()
    mutated = copy.deepcopy(fixtures)
    mutated['invariants'][guard] = True
    with pytest.raises(AssertionError):
        validator.validate_retrieval_contract(schema, mutated, evidence)


@pytest.mark.parametrize(
    'guard',
    [
        'direct_metadata_lookup_is_not_semantic_acceptance',
        'hold_results_are_explicitly_addressable',
    ],
)
def test_rejects_loss_of_fail_closed_retrieval_guards(guard):
    schema, fixtures, evidence = load_inputs()
    mutated = copy.deepcopy(fixtures)
    mutated['invariants'][guard] = False
    with pytest.raises(AssertionError):
        validator.validate_retrieval_contract(schema, mutated, evidence)


def test_rejects_missing_per_result_truth_guard():
    schema, fixtures, evidence = load_inputs()
    mutated = copy.deepcopy(schema)
    required = mutated['properties']['results']['items']['properties']['contract_guards']['required']
    required.remove('not_truth_claim')
    with pytest.raises(AssertionError):
        validator.validate_retrieval_contract(mutated, fixtures, evidence)


def test_rejects_missing_hold_semantic_state():
    schema, fixtures, evidence = load_inputs()
    mutated = copy.deepcopy(schema)
    semantic_enum = mutated['properties']['results']['items']['properties']['semantic_decision']['enum']
    semantic_enum.remove('HOLD')
    with pytest.raises(AssertionError):
        validator.validate_retrieval_contract(mutated, fixtures, evidence)


def test_rejects_missing_evidence_boundary():
    schema, fixtures, evidence = load_inputs()
    mutated = evidence.replace('Provenance is not evidence', 'Provenance boundary removed')
    with pytest.raises(AssertionError):
        validator.validate_retrieval_contract(schema, fixtures, mutated)
