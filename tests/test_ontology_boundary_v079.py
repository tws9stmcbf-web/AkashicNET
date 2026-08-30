import importlib.util
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / 'scripts' / 'validate_ontology_boundary_v079.py'
spec = importlib.util.spec_from_file_location('ontology_boundary_v079', SCRIPT)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


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
