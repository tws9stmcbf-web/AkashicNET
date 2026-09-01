#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
READINESS = ROOT / "references" / "community" / "public-knowledge-beta-readiness-v0.13.json"
V012 = ROOT / "references" / "community" / "integration-beta-readiness-v0.12.json"
MANIFEST = ROOT / "references" / "community" / "public-knowledge-beta-release-manifest-v0.13.json"

REQUIRED = [
    "v012_integration_beta_readiness_preserved",
    "no_release_critical_public_privacy_or_provenance_defect",
    "knowledge_graph_asserted_vs_candidate_separation",
    "big_questions_architecture_supports_multiple_products",
    "public_evidence_and_provenance_synchronized",
    "automated_public_source_link_integrity_gate",
    "reproducible_public_knowledge_release_manifest",
    "deterministic_public_route_responsive_accessibility_gate",
    "support_funding_separated_from_evidence_conclusions",
    "end_to_end_public_knowledge_beta_release_gate",
]

SHA40 = re.compile(r"^[0-9a-f]{40}$")


def main() -> int:
    readiness = json.loads(READINESS.read_text(encoding="utf-8"))
    v012 = json.loads(V012.read_text(encoding="utf-8"))
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))

    assert readiness["target_version"] == "0.13.0-beta.1"
    assert readiness["readiness_policy"] == "fail_closed"
    audit = readiness["audit"]
    assert list(audit) == REQUIRED, "v0.13 gate set drift"
    assert all(audit[k] == "PASS" for k in REQUIRED), audit
    assert readiness["release_blockers"] == []
    assert readiness["public_knowledge_beta_declared"] is True

    assert v012["integration_beta_declared"] is True
    assert v012["release_blockers"] == []
    assert all(v is True for v in v012["required_gates"].values())

    assert manifest["target_version"] == "0.13.0-beta.1"
    assert manifest["release_policy"] == "exact_commit_fail_closed"
    state = manifest.get("state", "CANDIDATE")
    validated = manifest["validated_release_commit"]
    if state == "CANDIDATE":
        assert validated is None, "candidate manifest must not pre-populate validated release commit"
    elif state == "SEALED":
        assert isinstance(validated, str) and SHA40.fullmatch(validated), (
            "sealed manifest must preserve an exact lowercase 40-character validated commit SHA"
        )
        assert "does not retarget" in manifest["seal_rule"], (
            "sealed metadata must state that the later seal commit does not retarget the release"
        )
    else:
        raise AssertionError(f"unsupported manifest state: {state}")

    assert manifest["privacy"]["private_drive_identifiers_public"] is False
    assert manifest["privacy"]["private_drive_paths_public"] is False
    assert manifest["privacy"]["private_drive_timestamps_public"] is False
    assert manifest["privacy"]["file_linked_private_hashes_public"] is False

    inv = readiness["invariants"]
    assert inv["truth_inference_allowed"] is False
    assert inv["rights_promotion_allowed"] is False
    assert inv["scientific_evidence_promotion_allowed"] is False
    assert inv["private_drive_promotion_allowed"] is False
    assert inv["api_unverified_reddit_may_be_labelled_api_verified"] is False
    assert inv["cross_source_candidate_links_are_truth_claims"] is False
    assert inv["public_visual_design_is_evidence"] is False

    print("PUBLIC KNOWLEDGE BETA v0.13 READY: 10/10 deterministic gates PASS")
    print(f"manifest_state={state} validated_release_commit={validated}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
