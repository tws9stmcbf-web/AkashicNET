#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
READINESS = ROOT / "references/community/provenance-integrity-beta-readiness-v0.14.json"
INVENTORY = ROOT / "references/community/public-source-url-inventory-v0.14.json"
V013 = ROOT / "references/community/public-knowledge-beta-release-manifest-v0.13.json"

CRITERIA = [f"V014-C{i}" for i in range(1, 11)]
ALLOWED = {"PASS", "PARTIAL", "BLOCKED", "PENDING", "REVALIDATION_REQUIRED"}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--require-ready", action="store_true")
    args = parser.parse_args()

    readiness = json.loads(READINESS.read_text(encoding="utf-8"))
    inventory = json.loads(INVENTORY.read_text(encoding="utf-8"))
    v013 = json.loads(V013.read_text(encoding="utf-8"))

    assert readiness["target_version"] == "0.14.0-beta.1"
    assert readiness["target_name"] == "Provenance Integrity Beta"
    assert readiness["readiness_policy"] == "exact_commit_fail_closed"
    assert readiness["v014_declared"] is False
    assert readiness["status"] == "CANDIDATE_BLOCKED"

    assert v013["target_version"] == "0.13.0-beta.1"
    assert v013["state"] == "SEALED"
    assert v013["validated_release_commit"] == readiness["immutable_baseline"]["validated_release_commit"]
    assert readiness["immutable_baseline"]["retargetable"] is False

    keys = list(readiness["criteria"])
    assert [key.split("_", 1)[0] for key in keys] == CRITERIA, "v0.14 criterion set drift"
    assert all(value in ALLOWED for value in readiness["criteria"].values())

    inv = readiness["fixed_invariants"]
    assert all(value is False for value in inv.values()), "a fail-closed invariant was enabled"
    guards = inventory["guards"]
    assert guards["original_urls_preserved"] is True
    assert guards["unavailability_changes_truth_status"] is False
    assert guards["automatic_source_replacement"] is False
    assert guards["automatic_evidence_promotion"] is False

    entries = inventory["entries"]
    summary = inventory["summary"]
    assert summary["external_url_occurrences"] == len(entries)
    unique_ids = {entry["source_id"] for entry in entries}
    assert summary["unique_normalized_external_urls"] == len(unique_ids)
    for entry in entries:
        assert re.fullmatch(r"URL-[0-9a-f]{16}", entry["source_id"])
        assert entry["original_url"].startswith(("http://", "https://"))
        assert entry["truth_status_changed"] is False

    ready = (
        inventory["state"] == "ASSESSED"
        and entries
        and summary["unassessed_unique_urls"] == 0
        and all(value == "PASS" for value in readiness["criteria"].values())
        and readiness["release_blockers"] == []
        and readiness["v014_declared"] is True
    )
    if args.require_ready and not ready:
        raise SystemExit("BLOCKED: v0.14 readiness conditions are not all satisfied")
    print("VALID: v0.14 candidate contract is internally consistent")
    print(f"release_ready={ready} inventory_state={inventory['state']} blockers={len(readiness['release_blockers'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
