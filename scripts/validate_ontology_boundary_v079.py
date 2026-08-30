#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / 'references' / 'community' / 'ontology-boundary-fixtures-v0.7.9.json'
SCHEMA_DOC = ROOT / 'references' / 'community' / 'knowledge-graph-schema-v0.1.md'
CANON_DOC = ROOT / 'docs' / 'CANONICAL_ADJUDICATION_CONTRACT_V070.md'
EVIDENCE_DOC = ROOT / 'docs' / 'canonical-evidence-v01.md'

WEAK_BASES = {'hash', 'title_normalisation', 'collection_alignment', 'exact_metadata'}
PROMOTION_KEYS = {
    'promotes_work_identity',
    'promotes_edition_identity',
    'promotes_rights',
    'promotes_scientific_evidence',
    'promotes_truth',
}


def edge_is_safe(edge: dict) -> bool:
    promoted = {k for k in PROMOTION_KEYS if edge.get(k) is True}
    if not promoted:
        return True
    if edge.get('basis') in WEAK_BASES:
        return False
    if edge.get('review_state') in {'unresolved', 'provisional'}:
        return False
    return False


def main() -> None:
    data = json.loads(FIXTURES.read_text(encoding='utf-8'))
    assert data['version'] == '0.7.9'
    guards = data['guardrails']
    assert guards['ambiguous_edges_default_unresolved'] is True
    assert guards['hash_is_byte_identity_signal_only'] is True
    assert guards['rights_independent_of_canonical_identity'] is True
    assert guards['scientific_evidence_independent_of_provenance'] is True
    assert guards['truth_inference_allowed'] is False
    assert guards['drive_access_performed'] is False
    assert guards['privacy_posture_changed'] is False

    for edge in data['allowed_examples']:
        assert edge_is_safe(edge), f"allowed edge rejected: {edge['id']}"
    for edge in data['forbidden_examples']:
        assert not edge_is_safe(edge), f"forbidden promotion accepted: {edge['id']}"

    graph = SCHEMA_DOC.read_text(encoding='utf-8').lower()
    canon = CANON_DOC.read_text(encoding='utf-8').lower()
    evidence = EVIDENCE_DOC.read_text(encoding='utf-8').lower()

    for phrase in ['ambiguous relationships remain explicit `unresolved` edges', 'rights state is independent', 'scientific evidence']:
        assert phrase in graph, f'missing ontology boundary phrase: {phrase}'
    for phrase in ['work identity', 'edition identity', 'rights', 'truth', 'scientific']:
        assert phrase in canon, f'missing canonical boundary phrase: {phrase}'
    for phrase in ['provenance is not evidence', 'semantic connection is not scientific evidence']:
        assert phrase in evidence, f'missing evidence boundary phrase: {phrase}'

    print('AKASHICNET v0.7.9 ONTOLOGY BOUNDARY PASS', {
        'allowed_examples': len(data['allowed_examples']),
        'forbidden_examples': len(data['forbidden_examples']),
        'truth_inference_allowed': False,
        'rights_promotion_from_weak_basis_allowed': False,
        'scientific_evidence_promotion_from_weak_basis_allowed': False,
    })


if __name__ == '__main__':
    main()
