#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REF = ROOT / "references" / "community"
AUDIT = REF / "v010-repository-release-audit.json"
DRIVE = REF / "drive-p1-small-batch5-hash-summary-v0.6.15.json"
WIKI = REF / "wikispine-checkpoint-v0.7.4.json"
TOPICS = REF / "topic-census-checkpoint-v0.7.5.json"
TAXONOMY = REF / "evidence-taxonomy-v0.10.json"
BATCH3 = REF / "canonical-adjudication-batch3-v0.7.3.json"
README = ROOT / "README.md"


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    audit = load(AUDIT)
    drive = load(DRIVE)
    wiki = load(WIKI)
    topics = load(TOPICS)
    taxonomy = load(TAXONOMY)
    batch3 = load(BATCH3)
    readme = README.read_text(encoding="utf-8")

    assert audit["version"] == "0.10.0-prealpha"
    assert audit["repository_release_audit_passed"] is True
    assert audit["release_ready"] is False

    state = audit["verified_state"]
    assert drive["authoritative_unique_families_after"] == state["canonical_families_adjudicated"] == 81
    assert drive["unresolved_after"] == state["canonical_families_unresolved"] == 45
    assert state["canonical_duplicate_review_denominator"] == 126
    assert 81 + 45 == 126
    assert state["canonical_mapping_blocked_fail_closed"] is True

    assert wiki["unique_seeds"] == state["wikispine_unique_seeds"] == 53
    assert wiki["resolved_high_precision"] == state["wikispine_resolved_high_precision"] == 50
    assert wiki["pending"] == state["wikispine_pending"] == 3
    assert 50 + 3 == 53

    assert topics["audited_unique_topics"] == state["audited_public_metadata_topics"] == 68
    assert topics["interpretation"]["broader_300_plus_claim_status"] == state["broader_300_plus_topic_claim"]

    assert len(taxonomy["canonical_labels"]) == state["public_epistemic_labels"] == 5
    assert taxonomy["public_surface_audit"]["homepage_exact_taxonomy_consistent"] is True
    assert taxonomy["public_surface_audit"]["release_gate_passed"] is True

    assert batch3["supersedes_checkpoint"] == "canonical-adjudication-public-bibliography-v0.10.1.json"
    assert {r["decision"] for r in batch3["records"]} == {"ACCEPT"}
    for record in batch3["records"]:
        assert record["relationship"] == "REPRESENTS_WORK"
        assert record["rights_promoted"] is False
        assert record["public_release_promoted"] is False
        assert record["scientific_evidence_promoted"] is False
        assert record["safety_or_efficacy_promoted"] is False

    assert "PRE-ALPHA v0.9" in readme
    assert audit["current_public_version_metadata"] == "PRE-ALPHA v0.9"
    assert audit["remaining_release_gates"] == [
        "readme_changelog_version_metadata_update",
        "tag_and_release_creation",
    ]

    invariants = audit["release_invariants"]
    for key, value in invariants.items():
        assert value is False, f"release invariant must remain false: {key}"
    assert audit["drive_access_performed"] is False

    print("AKASHICNET PRE-ALPHA v0.10 REPOSITORY RELEASE AUDIT PASS: metadata/tag gates remain")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
