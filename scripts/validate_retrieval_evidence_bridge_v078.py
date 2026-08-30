#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REF = ROOT / 'references' / 'community'

REQUIRED_POLICY_GUARDS = {
    'truth_inference_allowed',
    'rights_promotion_allowed',
    'scientific_evidence_promotion_allowed',
    'ranking_changes_semantic_decision',
    'direct_metadata_lookup_is_not_semantic_acceptance',
}

REQUIRED_RESULT_GUARDS = {
    'ranking_changes_semantic_decision',
    'not_truth_claim',
    'not_scientific_evidence_claim',
    'not_rights_clearance_claim',
    'not_safety_or_efficacy_claim',
}

FALSE_INVARIANTS = {
    'truth_inference_allowed',
    'rights_promotion_allowed',
    'scientific_evidence_promotion_allowed',
    'ranking_changes_semantic_decision',
}

TRUE_INVARIANTS = {
    'direct_metadata_lookup_is_not_semantic_acceptance',
    'hold_results_are_explicitly_addressable',
}

EVIDENCE_BOUNDARIES = [
    'Provenance is not evidence',
    'Semantic connection is not scientific evidence',
    'Archive inclusion is not endorsement',
]


def validate_retrieval_contract(schema, fixtures, evidence_text):
    policy_required = set(schema['properties']['policy']['required'])
    missing_policy = REQUIRED_POLICY_GUARDS - policy_required
    assert not missing_policy, f'missing retrieval policy guards: {sorted(missing_policy)}'

    result_required = set(
        schema['properties']['results']['items']['properties']['contract_guards']['required']
    )
    missing_result = REQUIRED_RESULT_GUARDS - result_required
    assert not missing_result, f'missing per-result guards: {sorted(missing_result)}'

    invariants = fixtures['invariants']
    for key in FALSE_INVARIANTS:
        assert invariants.get(key) is False, f'{key} must remain false'
    for key in TRUE_INVARIANTS:
        assert invariants.get(key) is True, f'{key} must remain true'

    assert invariants.get('archive_mode') == 'metadata_and_links_only', (
        'retrieval archive mode must remain metadata_and_links_only'
    )
    assert invariants.get('result_order') == 'descending provenance_rank', (
        'retrieval result ordering contract changed'
    )

    evidence_lower = evidence_text.lower()
    for phrase in EVIDENCE_BOUNDARIES:
        assert phrase.lower() in evidence_lower, f'missing evidence boundary: {phrase}'

    tier_enum = schema['properties']['results']['items']['properties']['evidence_profile']['properties']['provenance_tier']['enum']
    assert 'P3_SHA256_IDENTITY_PROVENANCE' in tier_enum

    semantic_enum = schema['properties']['results']['items']['properties']['semantic_decision']['enum']
    assert 'HOLD' in semantic_enum, 'HOLD retrieval state must remain representable'
    assert 'DIRECT_METADATA_LOOKUP' in semantic_enum, (
        'direct metadata lookup must remain distinct from semantic acceptance'
    )

    return {
        'retrieval_schema_version': schema['properties']['api_version']['const'],
        'truth_inference': False,
        'rights_promotion': False,
        'scientific_evidence_promotion': False,
        'ranking_changes_semantic_decision': False,
        'provenance_is_evidence': False,
    }


def load_and_validate():
    schema = json.loads((REF / 'unified-retrieval-schema-v0.25.json').read_text(encoding='utf-8'))
    fixtures = json.loads((REF / 'retrieval-fixtures-v0.25.json').read_text(encoding='utf-8'))
    evidence = (ROOT / 'docs' / 'canonical-evidence-v01.md').read_text(encoding='utf-8')
    return validate_retrieval_contract(schema, fixtures, evidence)


if __name__ == '__main__':
    result = load_and_validate()
    print('AKASHICNET v0.7.8 RETRIEVAL EVIDENCE BRIDGE PASS', result)
