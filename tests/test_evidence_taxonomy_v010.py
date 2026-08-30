import copy
import importlib.util
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'scripts' / 'validate_evidence_taxonomy_v010.py'
spec = importlib.util.spec_from_file_location('evidence_taxonomy_v010', SCRIPT)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

TAXONOMY = json.loads((ROOT / 'references' / 'community' / 'evidence-taxonomy-v0.10.json').read_text(encoding='utf-8'))
LEGACY = json.loads((ROOT / 'data' / 'evidence_claim_v01.schema.json').read_text(encoding='utf-8'))
HOME = (ROOT / 'website' / 'app' / 'page.tsx').read_text(encoding='utf-8')


def test_evidence_taxonomy_audit_executes():
    assert mod.validate(TAXONOMY, LEGACY, HOME)


def test_canonical_public_taxonomy_has_five_distinct_labels():
    assert mod.CANONICAL == [
        'Established Evidence',
        'Interpretation',
        'Lived Experience/Testimony',
        'Hypothesis',
        'Speculation',
    ]
    assert len(set(mod.CANONICAL)) == 5


def test_legacy_tiers_are_not_public_certainty_labels():
    assert 'EMPIRICAL_REFERENCE' in mod.LEGACY_TIERS
    assert 'Established Evidence' not in mod.LEGACY_TIERS


@pytest.mark.parametrize('field', [
    'truth_inference_allowed',
    'rights_promotion_allowed',
    'scientific_evidence_promotion_allowed',
])
def test_epistemic_promotion_flags_fail_closed(field):
    tax = copy.deepcopy(TAXONOMY)
    tax['promotion_guards'][field] = True
    with pytest.raises(AssertionError):
        mod.validate(tax, LEGACY, HOME)


@pytest.mark.parametrize('field', [
    'retrieval_rank_may_not_upgrade_label',
    'reference_identity_may_not_upgrade_label',
    'graph_edge_state_may_not_upgrade_label',
    'hash_identity_may_not_upgrade_label',
    'archive_inclusion_may_not_upgrade_label',
    'Established_Evidence_requires_reviewed_support_and_provenance',
    'Lived_Experience_Testimony_may_not_be_universalised',
    'Hypothesis_may_not_be_presented_as_Established_Evidence',
    'Speculation_may_not_be_presented_as_Hypothesis_or_Established_Evidence',
])
def test_required_promotion_guards_cannot_be_disabled(field):
    tax = copy.deepcopy(TAXONOMY)
    tax['promotion_guards'][field] = False
    with pytest.raises(AssertionError):
        mod.validate(tax, LEGACY, HOME)


def test_legacy_source_support_tier_cannot_auto_map_to_established_evidence():
    tax = copy.deepcopy(TAXONOMY)
    tax['legacy_contract_boundary']['EMPIRICAL_REFERENCE_does_not_auto_map_to_Established_Evidence'] = False
    with pytest.raises(AssertionError):
        mod.validate(tax, LEGACY, HOME)


def test_legacy_schema_cannot_gain_public_certainty_label():
    legacy = copy.deepcopy(LEGACY)
    enum = legacy['properties']['evidence_links']['items']['properties']['evidence_tier']['enum']
    enum.append('Established Evidence')
    with pytest.raises(AssertionError):
        mod.validate(TAXONOMY, legacy, HOME)


def test_canonical_label_order_and_membership_cannot_drift():
    tax = copy.deepcopy(TAXONOMY)
    tax['canonical_labels'][0] = 'Confirmed Truth'
    with pytest.raises(AssertionError):
        mod.validate(tax, LEGACY, HOME)


def test_public_surface_cannot_drop_canonical_label():
    home = HOME.replace('<h3>Speculation</h3>', '<h3>Possibility</h3>', 1)
    assert home != HOME
    with pytest.raises(AssertionError):
        mod.validate(TAXONOMY, LEGACY, home)


def test_public_surface_cannot_restore_legacy_certainty_label():
    home = HOME + '\n<h3>Supported evidence</h3>\n'
    with pytest.raises(AssertionError):
        mod.validate(TAXONOMY, LEGACY, home)


@pytest.mark.parametrize(('field', 'value'), [
    ('homepage_exact_taxonomy_consistent', False),
    ('release_gate_passed', False),
    ('homepage_missing_canonical_label', 'Speculation'),
])
def test_public_surface_audit_cannot_claim_inconsistent_state(field, value):
    tax = copy.deepcopy(TAXONOMY)
    tax['public_surface_audit'][field] = value
    with pytest.raises(AssertionError):
        mod.validate(tax, LEGACY, HOME)


@pytest.mark.parametrize('field', ['privacy_posture_changed', 'drive_access_performed'])
def test_privacy_or_drive_boundary_change_fails_closed(field):
    tax = copy.deepcopy(TAXONOMY)
    tax[field] = True
    with pytest.raises(AssertionError):
        mod.validate(tax, LEGACY, HOME)
