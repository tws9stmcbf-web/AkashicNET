#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "references" / "community" / "orchestration-task-uniqueness-v0.1.json"

EXPECTED_CLASSES = ["NEW", "EXTENDS", "SUPERSEDES", "DUPLICATE"]
REQUIRED_SUBSYSTEMS = {
    "drive_hashing",
    "canonicalisation",
    "wikispine",
    "retrieval",
    "ontology",
    "evidence",
    "bounded_questions",
    "release",
    "website_metrics",
    "privacy_security",
}


def main() -> int:
    payload = json.loads(CONTRACT.read_text(encoding="utf-8"))
    assert payload["version"] == "0.1.0"
    assert payload["classifications"] == EXPECTED_CLASSES

    rules = payload["rules"]
    for key in (
        "inspect_open_prs_before_new_pr",
        "inspect_recent_merged_prs_before_new_pr",
        "inspect_open_issues_before_new_pr",
        "one_active_implementation_per_subsystem",
        "superseding_work_must_name_predecessor",
        "extending_work_must_name_canonical_path",
    ):
        assert rules[key] is True, key
    assert rules["duplicate_work_may_open_pr"] is False

    assert REQUIRED_SUBSYSTEMS <= set(payload["subsystems"])

    overlaps = {entry["scope"]: entry for entry in payload["known_reconciled_overlap"]}
    assert "drive_hashing" in overlaps
    assert "bounded_questions" in overlaps
    assert "PR-44" in overlaps["drive_hashing"]["records"]
    assert "zero incremental families" in overlaps["drive_hashing"]["resolution"]
    assert "PR-83" in overlaps["bounded_questions"]["records"]
    assert "legacy/read-only" in overlaps["bounded_questions"]["resolution"]

    template = payload["pre_pr_decision_template"]
    assert template["classification"] == "NEW|EXTENDS|SUPERSEDES|DUPLICATE"
    assert template["safe_to_open_pr"] == "BOOLEAN"

    invariants = payload["release_invariants"]
    assert all(value is False for value in invariants.values())

    print("ORCHESTRATION TASK UNIQUENESS v0.1 PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
