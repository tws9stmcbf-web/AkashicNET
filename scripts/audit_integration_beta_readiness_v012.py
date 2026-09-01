#!/usr/bin/env python3
"""Fail-closed readiness audit for AkashicNET v0.12 Integration Beta."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMMUNITY = ROOT / "references" / "community"
READINESS = COMMUNITY / "integration-beta-readiness-v0.12.json"
DATA_BETA = COMMUNITY / "data-beta-readiness-v0.11.json"
BQ = ROOT / "references" / "big-questions" / "BQ001" / "public-synthesis-v0.1.json"
BQ_PAGE = ROOT / "website" / "app" / "big-questions" / "bq001" / "page.tsx"
CROSS_SOURCE = ROOT / "scripts" / "build_cross_source_graph_v07.py"

PATH_GATES = {
    "public_beta_integration_gate_present": ROOT / "scripts" / "validate_public_beta_integration_gate.py",
    "immutable_actions_gate_present": ROOT / "scripts" / "validate_actions_immutable_refs.py",
    "public_data_boundary_present": ROOT / "scripts" / "check_public_data_boundary.py",
    "evidence_taxonomy_present": COMMUNITY / "evidence-taxonomy-v0.10.json",
    "stable_provenance_contract_present": COMMUNITY / "evidence-provenance-scoring-v0.1.md",
    "integration_beta_ci_gate_present": ROOT / ".github" / "workflows" / "validate-integration-beta-readiness-v012.yml",
}


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def audit() -> tuple[list[str], dict]:
    errors: list[str] = []
    readiness = load_json(READINESS)
    data_beta = load_json(DATA_BETA)
    bq = load_json(BQ)
    page = BQ_PAGE.read_text(encoding="utf-8")
    cross_source = CROSS_SOURCE.read_text(encoding="utf-8")
    gates = readiness["required_gates"]

    if readiness.get("target_version") != "0.12.0-beta.1":
        errors.append("target_version must remain 0.12.0-beta.1")
    if readiness.get("current_public_phase") != "PUBLIC BETA":
        errors.append("current_public_phase must remain PUBLIC BETA")

    reconstructed: dict[str, bool] = {}
    reconstructed["data_beta_readiness_preserved"] = bool(data_beta.get("knowledge_data_beta_declared")) and not data_beta.get("release_blockers")
    for gate, path in PATH_GATES.items():
        reconstructed[gate] = path.is_file()

    reconstructed["bq001_canonical_status_unresolved"] = (
        bq.get("status") == "UNRESOLVED"
        and bq.get("conclusion", {}).get("status") == "UNRESOLVED"
    )
    reconstructed["bq001_website_status_unresolved"] = (
        "CURRENT STATUS · UNRESOLVED" in page
        and "CURRENT CONCLUSION · UNRESOLVED" in page
    )

    canonical_version = str(bq.get("version", ""))
    displayed_versions = re.findall(r"Public synthesis v([0-9]+(?:\.[0-9]+)*)", page)
    reconstructed["bq001_website_provenance_version_synchronized"] = (
        len(displayed_versions) == 1 and displayed_versions[0] == canonical_version
    )

    reconstructed["knowledge_graph_non_truth_crosslink_policy_present"] = all(marker in cross_source for marker in (
        "'review_state':'provisional'",
        "'not_truth_claim':True",
        "graph['policy']['cross_source_links_are_not_truth_claims']=True",
        "'cross_link_policy':'explicit canonical label mention in curated title/summary only; provisional until reviewed'",
    ))

    for gate, actual in reconstructed.items():
        declared = gates.get(gate)
        if declared is not actual:
            errors.append(f"{gate} fixture={declared!r} reconstructed={actual!r}")

    for invariant, value in readiness.get("invariants", {}).items():
        if value is not False:
            errors.append(f"fail-closed invariant must remain false: {invariant}")

    blockers = readiness.get("release_blockers", [])
    for blocker in blockers:
        if blocker not in gates:
            errors.append(f"release blocker is not a required gate: {blocker}")
        elif gates[blocker] is not False:
            errors.append(f"release blocker must remain false until resolved: {blocker}")

    derived_ready = all(bool(v) for v in gates.values()) and not blockers
    declared_ready = bool(readiness.get("integration_beta_declared"))
    if declared_ready != derived_ready:
        errors.append(f"integration_beta_declared={declared_ready} derived={derived_ready}")

    summary = {
        "target_version": readiness["target_version"],
        "audit_state": "READY" if derived_ready else "BLOCKED",
        "integration_beta_ready": derived_ready,
        "completed_required_gates": sum(bool(v) for v in gates.values()),
        "required_gate_count": len(gates),
        "release_blockers": blockers,
        "bq001_canonical_version": canonical_version,
        "bq001_website_displayed_versions": displayed_versions,
        "bq001_status": bq.get("status"),
        "truth_inference_allowed": readiness["invariants"]["truth_inference_allowed"],
        "rights_promotion_allowed": readiness["invariants"]["rights_promotion_allowed"],
        "scientific_evidence_promotion_allowed": readiness["invariants"]["scientific_evidence_promotion_allowed"],
    }
    return errors, summary


def main() -> int:
    try:
        errors, summary = audit()
    except (OSError, json.JSONDecodeError, KeyError, TypeError) as exc:
        print(f"INTEGRATION BETA READINESS AUDIT FAILED: {exc}")
        return 1

    print(json.dumps(summary, indent=2))
    if errors:
        print("INTEGRATION BETA READINESS AUDIT FAILED")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"INTEGRATION BETA READINESS AUDIT PASS: correctly classified {summary['audit_state']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
