#!/usr/bin/env python3
"""Validate provenance-linked adjudication for cross-source batch v0.1.1."""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.validate_cross_source_edge_provenance_v01 import validate as validate_contract

DATA = ROOT / "references/community/cross-source-review-adjudication-v0.1.1.json"
LEDGER = ROOT / "references/community/cross-source-review-adjudication-v0.1.1.md"
LEDGER_ID = "artifact:cross-source-review-ledger:0.1.1"


def validate_adjudication(data: dict) -> list[str]:
    errors = list(validate_contract(data))
    artifacts = {a.get("artifact_id"): a for a in data.get("artifacts", []) if isinstance(a, dict)}
    ledger = artifacts.get(LEDGER_ID, {})
    if ledger.get("sha256") != hashlib.sha256(LEDGER.read_bytes()).hexdigest():
        errors.append("review-ledger digest mismatch")
    if ledger.get("independence_key") != "review:cross-source-batch-v0.1.1":
        errors.append("review ledger must use its fixed independence key")

    edges = {e.get("edge_id"): e for e in data.get("edges", []) if isinstance(e, dict)}
    candidates = [e for e in edges.values() if e.get("assertion_class") == "INFERRED_CANDIDATE"]
    decisions = [e for e in edges.values() if e.get("assertion_class") == "REJECTED_HOLD"]
    if len(candidates) != 3 or len(decisions) != 3 or len(edges) != 6:
        errors.append("adjudication must preserve 3 candidates and add exactly 3 decisions")
    if any(e.get("accepted_edge") is True for e in edges.values()):
        errors.append("adjudication must accept zero edges")

    ledger_text = LEDGER.read_text(encoding="utf-8")
    for number in range(1, 4):
        candidate_id = f"edge:review-batch-{number:04d}"
        decision_id = f"edge:review-decision-{number:04d}"
        record_id = f"decision:review-batch-{number:04d}"
        candidate = edges.get(candidate_id, {})
        decision = edges.get(decision_id, {})
        if decision.get("parent_edge_ids") != [candidate_id]:
            errors.append(f"{decision_id}: must cite exactly its candidate parent")
        if decision.get("source") != candidate.get("source") or decision.get("target") != candidate.get("target"):
            errors.append(f"{decision_id}: endpoints drifted from candidate")
        if decision.get("relationship") != candidate.get("relationship"):
            errors.append(f"{decision_id}: relationship drifted from candidate")
        required = {
            "assertion_class": "REJECTED_HOLD",
            "review_state": "REJECTED",
            "accepted_edge": False,
            "confidence_source_artifact_ids": [LEDGER_ID],
            "adjudication_ref": {"artifact_id": LEDGER_ID, "record_id": record_id},
            "not_truth_claim": True,
            "not_scientific_evidence": True,
            "not_rights_clearance": True,
        }
        for key, expected in required.items():
            if decision.get(key) != expected:
                errors.append(f"{decision_id}: {key} must be {expected!r}")
        if record_id not in ledger_text:
            errors.append(f"{decision_id}: decision record missing from ledger")

    policy = data.get("policy", {})
    if any(policy.get(key) is not False for key in (
        "truth_inference_allowed",
        "rights_promotion_allowed",
        "scientific_evidence_promotion_allowed",
        "confidence_from_representation_count_allowed",
        "circular_confidence_allowed",
    )):
        errors.append("all non-promotion policy switches must remain false")
    return sorted(set(errors))


def main() -> int:
    data = json.loads(DATA.read_text(encoding="utf-8"))
    errors = validate_adjudication(data)
    print(json.dumps({
        "candidate_count": 3,
        "decision_counts": {"REJECTED": 3, "HOLD": 0, "ACCEPTED": 0},
        "accepted_edge_count": 0,
        "truth_inference_allowed": False,
        "circular_confidence_allowed": False,
    }, sort_keys=True))
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("AKASHICNET CROSS-SOURCE REVIEW ADJUDICATION v0.1.1 PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
