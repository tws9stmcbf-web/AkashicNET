#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REF = ROOT / 'references' / 'community'
FIXTURE = REF / 'v010-integration-fixture.json'

EXPECTED_STAGES = [
    'ingestion',
    'canonical_resolution',
    'reference_resolution',
    'retrieval',
    'graph_candidate',
    'evidence_classification',
]


def validate_flow(data: dict) -> None:
    assert data['synthetic_public_safe'] is True
    stages = data['stages']
    assert [s['stage'] for s in stages] == EXPECTED_STAGES
    assert all(s['provenance_present'] is True for s in stages)

    # Once conservative canonical review places this record on HOLD, downstream
    # reference, retrieval, graph and evidence stages must not silently promote it.
    downstream = stages[1:]
    assert all(s['semantic_state'] == 'HOLD' for s in downstream)
    assert stages[2]['reference_identity_only'] is True
    assert stages[3]['retrieval_rank'] == 1
    assert stages[3]['semantic_state'] == 'HOLD'
    assert stages[4]['edge_state'] == 'unresolved'
    assert stages[5]['edge_state'] == 'unresolved'
    assert stages[5]['evidence_state'] == 'HYPOTHESIS'
    assert all(s['rights_state'] == 'UNRESOLVED' for s in stages)

    guards = data['release_guards']
    for key in [
        'hold_may_not_auto_promote',
        'ranking_may_not_change_semantic_state',
        'reference_identity_may_not_create_work_identity',
        'graph_candidate_may_not_create_truth',
        'provenance_may_not_create_scientific_evidence',
        'rights_may_not_be_inferred',
    ]:
        assert guards[key] is True, f'missing release guard: {key}'
    assert guards['privacy_posture_changed'] is False
    assert guards['drive_access_performed'] is False


def validate_contract_chain() -> None:
    required = [
        ROOT / 'docs' / 'CANONICAL_ADJUDICATION_CONTRACT_V070.md',
        REF / 'wikispine-canonical-bridge-checkpoint-v0.7.7.json',
        REF / 'unified-retrieval-schema-v0.25.json',
        REF / 'retrieval-fixtures-v0.25.json',
        REF / 'ontology-boundary-fixtures-v0.7.9.json',
        ROOT / 'docs' / 'canonical-evidence-v01.md',
        ROOT / 'docs' / 'DATA_SECURITY_BOUNDARY.md',
    ]
    for path in required:
        assert path.exists(), f'missing integration contract: {path.relative_to(ROOT)}'

    wiki = json.loads((REF / 'wikispine-canonical-bridge-checkpoint-v0.7.7.json').read_text(encoding='utf-8'))
    assert wiki['reference_identity_only'] is True
    assert wiki['canonical_work_identity_inferred'] is False
    assert wiki['edition_identity_inferred'] is False
    assert wiki['rights_status_inferred'] is False
    assert wiki['scientific_evidence_inferred'] is False
    assert wiki['truth_inferred'] is False

    retrieval = json.loads((REF / 'retrieval-fixtures-v0.25.json').read_text(encoding='utf-8'))['invariants']
    assert retrieval['truth_inference_allowed'] is False
    assert retrieval['rights_promotion_allowed'] is False
    assert retrieval['scientific_evidence_promotion_allowed'] is False
    assert retrieval['ranking_changes_semantic_decision'] is False

    ontology = json.loads((REF / 'ontology-boundary-fixtures-v0.7.9.json').read_text(encoding='utf-8'))['guardrails']
    assert ontology['ambiguous_edges_default_unresolved'] is True
    assert ontology['rights_independent_of_canonical_identity'] is True
    assert ontology['scientific_evidence_independent_of_provenance'] is True
    assert ontology['truth_inference_allowed'] is False


if __name__ == '__main__':
    data = json.loads(FIXTURE.read_text(encoding='utf-8'))
    assert data['version'] == '0.10.0-prealpha'
    validate_flow(data)
    validate_contract_chain()
    print('AKASHICNET PRE-ALPHA v0.10 INTEGRATION GATE PASS', {
        'stages': len(data['stages']),
        'semantic_state_after_canonical_review': 'HOLD',
        'final_evidence_state': 'HYPOTHESIS',
        'rights_state': 'UNRESOLVED',
        'privacy_posture_changed': False,
    })
