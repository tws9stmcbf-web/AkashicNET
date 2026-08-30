import copy
import importlib.util
import json
from pathlib import Path
import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "validate_v010_release_checkpoint.py"
spec = importlib.util.spec_from_file_location("release_checkpoint", SCRIPT)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

CHECKPOINT = json.loads((ROOT / "references" / "community" / "v010-release-checkpoint.json").read_text(encoding="utf-8"))
AUDIT = json.loads((ROOT / "references" / "community" / "v010-repository-release-audit.json").read_text(encoding="utf-8"))


def test_current_checkpoint_passes():
    assert mod.validate(CHECKPOINT, AUDIT)


@pytest.mark.parametrize("field,value", [
    ("release_ready", True),
    ("tag_and_release_created", True),
    ("integration_gate_present", False),
    ("repository_release_audit_passed", False),
    ("version_metadata_gate_complete", False),
])
def test_release_state_mutations_fail_closed(field, value):
    checkpoint = copy.deepcopy(CHECKPOINT)
    checkpoint[field] = value
    with pytest.raises(AssertionError):
        mod.validate(checkpoint, AUDIT)


def test_final_release_gate_cannot_disappear():
    checkpoint = copy.deepcopy(CHECKPOINT)
    checkpoint["remaining_release_gates"] = []
    with pytest.raises(AssertionError):
        mod.validate(checkpoint, AUDIT)


@pytest.mark.parametrize("field,value", [
    ("duplicate_review_denominator", 125),
    ("families_adjudicated", 82),
    ("families_unresolved", 44),
    ("next_mapping_required", "rows 87-91"),
    ("blocked_without_authoritative_private_mapping", False),
])
def test_canonicalisation_drift_fails_closed(field, value):
    checkpoint = copy.deepcopy(CHECKPOINT)
    checkpoint["canonicalisation"][field] = value
    with pytest.raises(AssertionError):
        mod.validate(checkpoint, AUDIT)


@pytest.mark.parametrize("key", [
    "truth_inference_allowed",
    "rights_promotion_allowed",
    "scientific_evidence_promotion_allowed",
    "ranking_changes_semantic_decision",
    "reference_identity_promotes_canonical_identity",
    "ambiguous_graph_edges_auto_promoted",
    "privacy_posture_changed",
])
def test_release_invariants_cannot_be_enabled(key):
    checkpoint = copy.deepcopy(CHECKPOINT)
    checkpoint["release_invariants"][key] = True
    with pytest.raises(AssertionError):
        mod.validate(checkpoint, AUDIT)


@pytest.mark.parametrize("field,value", [
    ("release_ready", True),
    ("remaining_release_gates", []),
    ("repository_release_audit_passed", False),
    ("current_version_metadata", "PUBLIC BETA"),
])
def test_audit_checkpoint_mismatch_fails_closed(field, value):
    audit = copy.deepcopy(AUDIT)
    audit[field] = value
    with pytest.raises(AssertionError):
        mod.validate(CHECKPOINT, audit)
