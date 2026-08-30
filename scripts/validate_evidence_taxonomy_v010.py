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
LEGACY_HOMEPAGE_LABELS = [
    'Supported evidence',
    'Interpretive framework',
    'Lived experience',
    'Speculative possibility',
]


def validate(tax: dict, legacy: dict, home: str) -> bool:
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
    assert audit['homepage_current_labels'] == CANONICAL
    assert audit['homepage_missing_canonical_label'] is None
    assert audit['homepage_exact_taxonomy_consistent'] is True
    assert audit['release_gate_passed'] is True
    assert audit['remediation'] is None

    for label in CANONICAL:
        assert f'<h3>{label}</h3>' in home, f'missing canonical homepage label: {label}'
    for label in LEGACY_HOMEPAGE_LABELS:
        assert f'<h3>{label}</h3>' not in home, f'legacy homepage label still present: {label}'

    assert tax['privacy_posture_changed'] is False
    assert tax['drive_access_performed'] is False
    return True


def main() -> None:
    tax = json.loads(TAXONOMY.read_text(encoding='utf-8'))
    legacy = json.loads(LEGACY_SCHEMA.read_text(encoding='utf-8'))
    home = HOME.read_text(encoding='utf-8')
    validate(tax, legacy, home)

    print('AKASHICNET PRE-ALPHA v0.10 EVIDENCE TAXONOMY PASS', {
        'canonical_labels': len(CANONICAL),
        'homepage_exact_taxonomy_consistent': True,
        'release_gate_passed': True,
        'privacy_posture_changed': False,
    })


if __name__ == '__main__':
    main()
