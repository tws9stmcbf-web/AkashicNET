#!/usr/bin/env python3
"""Audit readiness for the AkashicNET knowledge/data Beta candidate.

This is a readiness auditor, not a release promotion script. It exits non-zero only
when the readiness fixture is internally inconsistent or a supposedly completed
foundation is missing. A correctly detected BLOCKED state is a successful audit.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMMUNITY = ROOT / "references" / "community"
READINESS = COMMUNITY / "data-beta-readiness-v0.11.json"
V010 = COMMUNITY / "v010-release-checkpoint.json"
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

    readme_text = README.read_text(encoding="utf-8")
    denominator_risk = (
        "9,401 unique canonical Reddit URLs" in readme_text
        and not gates.get("historical_reddit_reconciliation_integrated")
    )

    summary = {
        "target_version": readiness["target_version"],
        "knowledge_data_beta_ready": derived_ready,
        "audit_state": "READY" if derived_ready else "BLOCKED",
        "completed_required_gates": sum(bool(v) for v in gates.values()),
        "required_gate_count": len(gates),
        "release_blockers": blockers,
        "critical_denominator_risk_detected": denominator_risk,
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
