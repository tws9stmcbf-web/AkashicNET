#!/usr/bin/env python3
"""Run the current public-safe AkashicNET integration gates as one fail-closed check.

This gate composes existing validators. It does not alter the sealed PRE-ALPHA v0.10
fixture or infer canonical identity, rights, truth, scientific evidence, safety, or efficacy.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

CHECKS = [
    ("sealed v0.10 integration", ("scripts/validate_v010_integration_gate.py",)),
    ("Public Beta status", ("tools/validate_public_beta_status.py",)),
    ("public data boundary", ("scripts/check_public_data_boundary.py",)),
    (
        "canonical adjudication contract",
        (
            "scripts/validate_canonical_adjudication_v070.py",
            "references/community/canonical-adjudication-example-v0.7.0.json",
        ),
    ),
    ("evidence/provenance scoring contract", ("scripts/validate_evidence_provenance_contract_v05.py",)),
    ("current WikiSpine v0.7.18", ("scripts/validate_wikispine_v0718.py",)),
    ("ontology boundary", ("scripts/validate_ontology_boundary_v079.py",)),
    ("Wikipedia pilot integrity/privacy", ("tools/validate_wikipedia_pilot.py",)),
    ("retrieval/evidence bridge", ("scripts/validate_retrieval_evidence_bridge_v078.py",)),
    (
        "BQ001 public synthesis",
        (
            "scripts/validate_bq001_public_synthesis_v01.py",
            "references/big-questions/BQ001/public-synthesis-v0.1.json",
        ),
    ),
    ("BQ001 public status boundary", ("scripts/validate_bq001_public_status_boundary.py",)),
]


def main() -> int:
    failures: list[str] = []
    for label, command in CHECKS:
        relative, *args = command
        path = ROOT / relative
        if not path.is_file():
            failures.append(f"{label}: missing validator {relative}")
            continue
        result = subprocess.run(
            [sys.executable, str(path), *args],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        if result.returncode != 0:
            detail = (result.stderr or result.stdout).strip()
            failures.append(f"{label}: exit {result.returncode}: {detail}")

    if failures:
        print("PUBLIC BETA INTEGRATION GATE FAILED")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print(
        "PUBLIC BETA INTEGRATION GATE PASS",
        {
            "checks": len(CHECKS),
            "live_governance_checks": 6,
            "privacy_posture_changed": False,
        },
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
