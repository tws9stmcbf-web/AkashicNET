import copy
import importlib.util
import json
from pathlib import Path
import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'scripts' / 'validate_ontology_boundary_v079.py'
spec = importlib.util.spec_from_file_location('ontology_boundary_v079', SCRIPT)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

DATA = json.loads((ROOT / 'references' / 'community' / 'ontology-boundary-fixtures-v0.7.9.json').read_text(encoding='utf-8'))
GRAPH = (ROOT / 'references' / 'community' / 'knowledge-graph-schema-v0.1.md').read_text(encoding='utf-8')
CANON = (ROOT / 'docs' / 'CANONICAL_ADJUDICATION_CONTRACT_V070.md').read_text(encoding='utf-8')
EVIDENCE = (ROOT / 'docs' / 'canonical-evidence-v01.md').read_text(encoding='utf-8')


def base_edge():
    return {
        'relationship': 'WORK_RELATED_TO_WORK',
        'basis': 'content_evidence',
        'review_state': 'accepted',
        'promotes_work_identity': False,
        'promotes_edition_identity': False,
        'promotes_rights': False,
        'promotes_scientific_evidence': False,
        'promotes_truth': False,
    }


def test_current_contract_passes():
    assert mod.validate(DATA, GRAPH, CANON, EVIDENCE)


def test_non_promoting_edge_is_safe():
    assert mod.edge_is_safe(base_edge()) is True


def test_hash_cannot_promote_work_identity():
    e = base_edge()
    e['basis'] = 'hash'
    e['promotes_work_identity'] = True
    assert mod.edge_is_safe(e) is False


def test_collection_alignment_cannot_promote_edition_identity():
    e = base_edge()
    e['basis'] = 'collection_alignment'
    e['promotes_edition_identity'] = True
    assert mod.edge_is_safe(e) is False


def test_title_normalisation_cannot_promote_rights():
    e = base_edge()
    e['basis'] = 'title_normalisation'
    e['promotes_rights'] = True
    assert mod.edge_is_safe(e) is False


def test_weak_provenance_cannot_promote_scientific_evidence():
    e = base_edge()
    e['basis'] = 'exact_metadata'
    e['promotes_scientific_evidence'] = True
    assert mod.edge_is_safe(e) is False


def test_unresolved_edge_cannot_promote_truth():
    e = base_edge()
    e['review_state'] = 'unresolved'
    e['promotes_truth'] = True
    assert mod.edge_is_safe(e) is False


@pytest.mark.parametrize('key,value', [
    ('ambiguous_edges_default_unresolved', False),
    ('hash_is_byte_identity_signal_only', False),
    ('rights_independent_of_canonical_identity', False),
    ('scientific_evidence_independent_of_provenance', False),
    ('truth_inference_allowed', True),
    ('drive_access_performed', True),
    ('privacy_posture_changed', True),
])
def test_guardrail_mutations_fail_closed(key, value):
    data = copy.deepcopy(DATA)
    data['guardrails'][key] = value
    with pytest.raises(AssertionError):
        mod.validate(data, GRAPH, CANON, EVIDENCE)


@pytest.mark.parametrize('promotion_key', sorted(mod.PROMOTION_KEYS))
def test_even_accepted_content_edge_cannot_auto_promote(promotion_key):
    edge = base_edge()
    edge[promotion_key] = True
    assert mod.edge_is_safe(edge) is False


@pytest.mark.parametrize('doc_name,phrase', [
    ('graph', 'ambiguous relationships remain explicit `unresolved` edges'),
    ('canon', 'work identity'),
    ('evidence', 'provenance is not evidence'),
])
def test_boundary_language_cannot_disappear(doc_name, phrase):
    graph, canon, evidence = GRAPH.lower(), CANON.lower(), EVIDENCE.lower()
    if doc_name == 'graph':
        assert phrase in graph
        graph = graph.replace(phrase, 'removed boundary', 1)
    elif doc_name == 'canon':
        assert phrase in canon
        canon = canon.replace(phrase, 'removed boundary', 1)
    else:
        assert phrase in evidence
        evidence = evidence.replace(phrase, 'removed boundary', 1)
    with pytest.raises(AssertionError):
        mod.validate(DATA, graph, canon, evidence)
