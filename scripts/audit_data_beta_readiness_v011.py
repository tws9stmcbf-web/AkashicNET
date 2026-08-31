#!/usr/bin/env python3
"""Audit readiness for the AkashicNET knowledge/data Beta candidate.

This is a readiness auditor, not a release promotion script. It fails closed when a
completed readiness gate cannot be independently reconstructed from repository state.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMMUNITY = ROOT / "references" / "community"
READINESS = COMMUNITY / "data-beta-readiness-v0.11.json"
V010 = COMMUNITY / "v010-release-checkpoint.json"
REDDIT_CHECKPOINT = COMMUNITY / "reddit-corpus-structural-checkpoint-v0.2.json"
README = ROOT / "README.md"

FOUNDATION_PATHS = {
    "public_beta_integration_gate_present": ROOT / "scripts" / "validate_public_beta_integration_gate.py",
    "public_data_boundary_present": ROOT / "scripts" / "check_public_data_boundary.py",
    "evidence_taxonomy_present": COMMUNITY / "evidence-taxonomy-v0.10.json",
    "ontology_boundary_present": COMMUNITY / "ontology-boundary-fixtures-v0.7.9.json",
    "topic_census_present": COMMUNITY / "topic-census-checkpoint-v0.7.5.json",
    "stable_provenance_contract_present": COMMUNITY / "evidence-provenance-scoring-v0.1.md",
}


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def audit() -> tuple[list[str], dict]:
    errors: list[str] = []
    readiness = load_json(READINESS)
    v010 = load_json(V010)
    checkpoint = load_json(REDDIT_CHECKPOINT)
    gates = readiness["required_gates"]

    if readiness.get("target_version") != "0.11.0-beta.1":
        errors.append("target_version must remain 0.11.0-beta.1 for this gate")
    if readiness.get("current_public_phase") != "PUBLIC BETA":
        errors.append("public experience phase must remain PUBLIC BETA")
    if readiness.get("sealed_engineering_baseline") != v010.get("version"):
        errors.append("sealed engineering baseline does not match v0.10 checkpoint")
    if not v010.get("release_ready") or not v010.get("release_verification", {}).get("verified_by_readback"):
        errors.append("sealed v0.10 release is not verified")
    if not gates.get("sealed_v010_release_verified"):
        errors.append("readiness fixture incorrectly marks sealed v0.10 incomplete")

    for gate, path in FOUNDATION_PATHS.items():
        exists = path.is_file()
        if gates.get(gate) is not exists:
            errors.append(f"{gate} fixture={gates.get(gate)!r} but file_present={exists!r}: {path.relative_to(ROOT)}")

    for invariant, value in readiness.get("invariants", {}).items():
        if value is not False:
            errors.append(f"fail-closed invariant must remain false: {invariant}")

    readme_text = README.read_text(encoding="utf-8")
    denominator_markers = (
        f"**{checkpoint['source_rows']:,} source rows**",
        f"**{checkpoint['unique_post_ids_all_subreddits']:,} unique Reddit post IDs / canonical post URLs across all archived subreddits**",
        f"**{checkpoint['unique_post_ids_by_subreddit']['NeuronsToNirvana']:,} unique r/NeuronsToNirvana post IDs**",
        "not Reddit API verification",
    )
    denominator_documented = all(marker in readme_text for marker in denominator_markers)
    if gates.get("historical_reddit_denominator_documented") is not denominator_documented:
        errors.append(
            "historical_reddit_denominator_documented does not match README/checkpoint evidence; "
            f"fixture={gates.get('historical_reddit_denominator_documented')!r} reconstructed={denominator_documented!r}"
        )

    boundary = checkpoint.get("evidence_boundary", {})
    if checkpoint.get("network_access_performed") is not False or checkpoint.get("reddit_api_verification_performed") is not False:
        errors.append("Reddit structural checkpoint must remain explicitly offline/API-unverified")
    if any(boundary.get(key) is not False for key in (
        "structurally_valid_means_api_verified",
        "annotation_rows_are_independent_posts",
        "source_row_count_may_be_presented_as_unique_post_count",
    )):
        errors.append("Reddit structural checkpoint evidence boundary was weakened")

    blockers = readiness.get("release_blockers", [])
    for blocker in blockers:
        if blocker not in gates:
            errors.append(f"release blocker is not a required gate: {blocker}")
        elif gates[blocker] is not False:
            errors.append(f"release blocker should be false until resolved: {blocker}")

    derived_ready = all(bool(value) for value in gates.values()) and not blockers
    declared = bool(readiness.get("knowledge_data_beta_declared"))
    if declared != derived_ready:
        errors.append(
            "knowledge_data_beta_declared must equal derived readiness; "
            f"declared={declared} derived={derived_ready}"
        )

    denominator_risk = not denominator_documented or "9,401 unique canonical Reddit URLs" in readme_text

    summary = {
        "target_version": readiness["target_version"],
        "knowledge_data_beta_ready": derived_ready,
        "audit_state": "READY" if derived_ready else "BLOCKED",
        "completed_required_gates": sum(bool(v) for v in gates.values()),
        "required_gate_count": len(gates),
        "release_blockers": blockers,
        "critical_denominator_risk_detected": denominator_risk,
        "reddit_source_rows": checkpoint["source_rows"],
        "reddit_structural_unique_posts": checkpoint["unique_post_ids_all_subreddits"],
        "reddit_api_verified": checkpoint["reddit_api_verification_performed"],
        "sealed_engineering_baseline": v010["version"],
        "public_experience_phase": readiness["current_public_phase"],
    }
    return errors, summary


def main() -> int:
    try:
        errors, summary = audit()
    except (OSError, json.JSONDecodeError, KeyError, TypeError) as exc:
        print(f"DATA BETA READINESS AUDIT FAILED: {exc}")
        return 1

    print(json.dumps(summary, indent=2))
    if errors:
        print("DATA BETA READINESS AUDIT FAILED")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"DATA BETA READINESS AUDIT PASS: correctly classified {summary['audit_state']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
