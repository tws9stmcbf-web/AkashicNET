import copy
import importlib.util
from pathlib import Path
import json
import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'scripts' / 'validate_retrieval_api_compat_v026.py'
spec = importlib.util.spec_from_file_location('compat', SCRIPT)
compat = importlib.util.module_from_spec(spec)
spec.loader.exec_module(compat)

POLICY = (ROOT / 'references' / 'community' / 'retrieval-api-compatibility-policy-v0.26.md').read_text(encoding='utf-8')
SCHEMA = json.loads((ROOT / 'references' / 'community' / 'unified-retrieval-schema-v0.25.json').read_text(encoding='utf-8'))
FIXTURES = json.loads((ROOT / 'references' / 'community' / 'retrieval-fixtures-v0.25.json').read_text(encoding='utf-8'))


def test_current_contract_passes():
    assert compat.validate(POLICY, SCHEMA, FIXTURES)


@pytest.mark.parametrize('field', ['api', 'api_version', 'schema_id', 'request', 'policy', 'summary', 'results', 'compatibility'])
def test_required_top_level_fields_fail_closed(field):
    schema = copy.deepcopy(SCHEMA)
    schema['required'].remove(field)
    with pytest.raises(AssertionError):
        compat.validate(POLICY, schema, FIXTURES)


@pytest.mark.parametrize('key,value', [
    ('truth_inference_allowed', True),
    ('rights_promotion_allowed', True),
    ('scientific_evidence_promotion_allowed', True),
    ('ranking_changes_semantic_decision', True),
    ('direct_metadata_lookup_is_not_semantic_acceptance', False),
    ('hold_results_are_explicitly_addressable', False),
])
def test_epistemic_and_semantic_mutations_fail_closed(key, value):
    fixtures = copy.deepcopy(FIXTURES)
    fixtures['invariants'][key] = value
    with pytest.raises(AssertionError):
        compat.validate(POLICY, SCHEMA, fixtures)


@pytest.mark.parametrize('decision', ['HOLD', 'DIRECT_METADATA_LOOKUP'])
def test_boundary_decisions_cannot_disappear(decision):
    schema = copy.deepcopy(SCHEMA)
    schema['properties']['results']['items']['properties']['semantic_decision']['enum'].remove(decision)
    with pytest.raises(AssertionError):
        compat.validate(POLICY, schema, FIXTURES)


def test_policy_boundary_cannot_be_silently_removed():
    policy = POLICY.replace('`DIRECT_METADATA_LOOKUP is not semantic acceptance`.', '')
    with pytest.raises(AssertionError):
        compat.validate(policy, SCHEMA, FIXTURES)
