import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'scripts' / 'validate_evidence_taxonomy_v010.py'
spec = importlib.util.spec_from_file_location('evidence_taxonomy_v010', SCRIPT)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def test_evidence_taxonomy_audit_executes():
    mod.main()


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
