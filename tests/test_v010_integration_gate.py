import copy
import importlib.util
import json
from pathlib import Path
import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'scripts' / 'validate_v010_integration_gate.py'
spec = importlib.util.spec_from_file_location('v010_gate', SCRIPT)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def fixture():
    return json.loads((ROOT / 'references' / 'community' / 'v010-integration-fixture.json').read_text(encoding='utf-8'))


def test_release_flow_is_fail_closed():
    mod.validate_flow(fixture())
    mod.validate_contract_chain()


def test_retrieval_rank_cannot_promote_hold():
    data = copy.deepcopy(fixture())
    data['stages'][3]['semantic_state'] = 'ACCEPT'
    with pytest.raises(AssertionError):
        mod.validate_flow(data)


def test_reference_identity_cannot_promote_hold():
    data = copy.deepcopy(fixture())
    data['stages'][2]['semantic_state'] = 'ACCEPT'
    with pytest.raises(AssertionError):
        mod.validate_flow(data)


def test_graph_candidate_cannot_promote_edge():
    data = copy.deepcopy(fixture())
    data['stages'][4]['edge_state'] = 'accepted'
    with pytest.raises(AssertionError):
        mod.validate_flow(data)


def test_rights_cannot_be_inferred_downstream():
    data = copy.deepcopy(fixture())
    data['stages'][5]['rights_state'] = 'PUBLIC'
    with pytest.raises(AssertionError):
        mod.validate_flow(data)


def test_evidence_classification_does_not_promote_semantics():
    data = copy.deepcopy(fixture())
    data['stages'][5]['semantic_state'] = 'ACCEPT'
    with pytest.raises(AssertionError):
        mod.validate_flow(data)
