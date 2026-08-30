#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REF = ROOT / "references" / "community"
CHECKPOINT = REF / "v010-release-checkpoint.json"
AUDIT = REF / "v010-repository-release-audit.json"

EXPECTED_COMPLETED = [
    "integration_gate_ci_green_and_merged",
    "evidence_taxonomy_consistency_audit",
    "repository_release_audit",
    "readme_changelog_version_metadata_update",
]


def main() -> int:
    checkpoint = json.loads(CHECKPOINT.read_text(encoding="utf-8"))
    audit = json.loads(AUDIT.read_text(encoding="utf-8"))

    assert checkpoint["version"] == "0.10.0-prealpha"
    assert checkpoint["release_name"] == "Evidence-Governed Knowledge Pipeline"
    assert checkpoint["release_ready"] is False
    assert checkpoint["integration_gate_present"] is True
    assert checkpoint["repository_release_audit_passed"] is True
    assert checkpoint["version_metadata_gate_complete"] is True
    assert checkpoint["tag_and_release_created"] is False
    assert checkpoint["completed_release_gates"] == EXPECTED_COMPLETED
    assert checkpoint["remaining_release_gates"] == ["tag_and_release_creation"]

    canonical = checkpoint["canonicalisation"]
    assert canonical["duplicate_review_denominator"] == 126
    assert canonical["families_adjudicated"] == 81
    assert canonical["families_unresolved"] == 45
    assert canonical["families_adjudicated"] + canonical["families_unresolved"] == canonical["duplicate_review_denominator"]
    assert canonical["next_mapping_required"] == "rows 82-86"
    assert canonical["blocked_without_authoritative_private_mapping"] is True

    invariants = checkpoint["release_invariants"]
    assert all(value is False for value in invariants.values())

    assert audit["repository_release_audit_passed"] is True
    assert audit["release_ready"] is False
    assert audit["remaining_release_gates"] == ["tag_and_release_creation"]
    assert audit["current_version_metadata"] == "PRE-ALPHA v0.10"

    print("AKASHICNET PRE-ALPHA v0.10 RELEASE CHECKPOINT PASS", {
        "completed_gates": len(EXPECTED_COMPLETED),
        "remaining_gate": "tag_and_release_creation",
        "release_ready": False,
        "canonical_review": "81/126",
        "unresolved": 45,
    })
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
