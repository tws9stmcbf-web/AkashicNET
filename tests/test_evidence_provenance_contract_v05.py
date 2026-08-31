import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "validate_evidence_provenance_contract_v05.py"
spec = importlib.util.spec_from_file_location("provenance_contract", SCRIPT)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

SPEC_TEXT = (ROOT / "references/community/evidence-provenance-scoring-v0.1.md").read_text(encoding="utf-8")
OVERLAY_TEXT = (ROOT / "scripts/overlay_evidence_provenance_v05.py").read_text(encoding="utf-8")


def test_current_contract_passes():
    assert mod.validate(SPEC_TEXT, OVERLAY_TEXT) == []


def test_unresolved_cap_cannot_be_removed():
    broken = OVERLAY_TEXT.replace(
        "if r['reconciled_status']=='UNRESOLVED_PROVENANCE': cap=45",
        "if r['reconciled_status']=='UNRESOLVED_PROVENANCE': cap=100",
    )
    assert mod.validate(SPEC_TEXT, broken)


def test_review_required_cap_cannot_be_removed():
    broken = OVERLAY_TEXT.replace(
        "if r['reconciled_status']=='REVIEW_REQUIRED': cap=55",
        "if r['reconciled_status']=='REVIEW_REQUIRED': cap=100",
    )
    assert mod.validate(SPEC_TEXT, broken)


def test_scientific_evidence_promotion_cannot_be_enabled():
    broken = OVERLAY_TEXT.replace(
        "'scientific_evidence_promotion_allowed':False",
        "'scientific_evidence_promotion_allowed':True",
    )
    assert mod.validate(SPEC_TEXT, broken)


def test_rights_and_truth_guards_cannot_disappear():
    broken = OVERLAY_TEXT.replace("'not_truth_score':True", "'not_truth_score':False")
    broken = broken.replace("'not_rights_score':True", "'not_rights_score':False")
    assert mod.validate(SPEC_TEXT, broken)


def test_spec_must_retain_scientific_evidence_boundary():
    broken = SPEC_TEXT.replace(
        "Scientific-evidence status is never promoted from provenance or canonical-confidence scoring alone.",
        "",
    )
    assert mod.validate(broken, OVERLAY_TEXT)
