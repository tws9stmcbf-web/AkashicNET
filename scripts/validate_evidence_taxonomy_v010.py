#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REF = ROOT / 'references' / 'community'
TAXONOMY = REF / 'evidence-taxonomy-v0.10.json'
LEGACY_SCHEMA = ROOT / 'data' / 'evidence_claim_v01.schema.json'
HOME = ROOT / 'website' / 'app' / 'page.tsx'

CANONICAL = [
    'Established Evidence',
    'Interpretation',
    'Lived Experience/Testimony',
    'Hypothesis',
    'Speculation',
]
LEGACY_TIERS = {
    'EMPIRICAL_REFERENCE',
    'HISTORICAL',
    'CONTEMPLATIVE_PHILOSOPHICAL',
    'EXPERIENTIAL_ESOTERIC',
}


def main() -> None:
    tax = json.loads(TAXONOMY.read_text(encoding='utf-8'))
    legacy = json.loads(LEGACY_SCHEMA.read_text(encoding='utf-8'))
    home = HOME.read_text(encoding='utf-8')

    assert tax['version'] == '0.10.0-prealpha'
    assert tax['canonical_labels'] == CANONICAL
    assert set(tax['definitions']) == set(CANONICAL)

    legacy_enum = set(
        legacy['properties']['evidence_links']['items']['properties']['evidence_tier']['enum']
    )
    assert legacy_enum == LEGACY_TIERS

    boundary = tax['legacy_contract_boundary']
    assert boundary['legacy_evidence_tiers_are_source_support_types_not_public_certainty_labels'] is True
    for tier in LEGACY_TIERS:
        assert boundary[f'{tier}_does_not_auto_map_to_Established_Evidence'] is True

    guards = tax['promotion_guards']
    for key in [
        'retrieval_rank_may_not_upgrade_label',
        'reference_identity_may_not_upgrade_label',
        'graph_edge_state_may_not_upgrade_label',
        'hash_identity_may_not_upgrade_label',
        'archive_inclusion_may_not_upgrade_label',
        'Established_Evidence_requires_reviewed_support_and_provenance',
        'Lived_Experience_Testimony_may_not_be_universalised',
        'Hypothesis_may_not_be_presented_as_Established_Evidence',
        'Speculation_may_not_be_presented_as_Hypothesis_or_Established_Evidence',
    ]:
        assert guards[key] is True, f'missing taxonomy guard: {key}'
    assert guards['truth_inference_allowed'] is False
    assert guards['rights_promotion_allowed'] is False
    assert guards['scientific_evidence_promotion_allowed'] is False

    audit = tax['public_surface_audit']
    detected = [
        label for label in audit['homepage_current_labels'] if label in home
    ]
    assert detected == audit['homepage_current_labels']
    assert audit['homepage_missing_canonical_label'] == 'Hypothesis'
    assert 'Hypothesis' not in detected
    assert audit['homepage_exact_taxonomy_consistent'] is False
    assert audit['release_gate_passed'] is False
    assert tax['privacy_posture_changed'] is False
    assert tax['drive_access_performed'] is False

    print('AKASHICNET PRE-ALPHA v0.10 EVIDENCE TAXONOMY AUDIT PASS', {
        'canonical_labels': len(CANONICAL),
        'homepage_legacy_labels_detected': len(detected),
        'homepage_exact_taxonomy_consistent': False,
        'release_gate_passed': False,
        'privacy_posture_changed': False,
    })


if __name__ == '__main__':
    main()
