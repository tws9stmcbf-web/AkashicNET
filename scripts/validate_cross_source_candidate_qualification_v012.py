#!/usr/bin/env python3
"""Validate the fail-closed cross-source candidate qualification policy v0.1.2."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "references/community/cross-source-candidate-qualification-policy-v0.1.2.json"

DIRECT = {"EXPLICIT_IDENTIFIER", "EXACT_FULL_TITLE", "EXPLICIT_CITATION"}
CORROBORATING = {
    "DISTINCTIVE_NAMED_ENTITY",
    "DISTINCTIVE_MULTI_TOKEN_PHRASE",
    "EXPLICIT_FRAMEWORK_REFERENCE",
    "EXPLICIT_QUESTION_REFERENCE",
}
REQUIRED_GENERIC = {"sacred", "wisdom", "tradition", "symbolism", "consciousness", "meaning", "knowledge", "magic"}


def qualifies(policy: dict, anchors: list[dict]) -> bool:
    q = policy["qualification"]
    usable = [a for a in anchors if not a.get("graph_derived") and not a.get("representation_only")]
    direct = {a.get("type") for a in usable if a.get("type") in DIRECT}
    if len(direct) >= q["direct_anchor_minimum"]:
        return True
    corroborating = {
        (a.get("type"), a.get("normalized_value"))
        for a in usable
        if a.get("type") in CORROBORATING and a.get("normalized_value")
    }
    return len(corroborating) >= q["corroborating_anchor_minimum"]


def validate(policy: dict) -> list[str]:
    errors: list[str] = []
    if policy.get("policy_version") != "0.1.2":
        errors.append("policy_version must equal 0.1.2")
    defaults = policy.get("candidate_defaults", {})
    expected_defaults = {
        "assertion_class": "INFERRED_CANDIDATE",
        "review_state": "REVIEW_REQUIRED",
        "accepted_edge": False,
    }
    if defaults != expected_defaults:
        errors.append("candidate defaults must remain review-only and unaccepted")

    q = policy.get("qualification", {})
    if set(q.get("direct_anchor_types", [])) != DIRECT:
        errors.append("direct anchor types changed")
    if set(q.get("corroborating_anchor_types", [])) != CORROBORATING:
        errors.append("corroborating anchor types changed")
    if q.get("direct_anchor_minimum") != 1:
        errors.append("one direct anchor must be required")
    if q.get("corroborating_anchor_minimum") != 2:
        errors.append("two corroborating anchors must be required")
    for key in (
        "corroborating_anchors_must_be_distinct",
        "generic_terms_cannot_qualify_alone",
    ):
        if q.get(key) is not True:
            errors.append(f"{key} must remain true")
    for key in (
        "graph_derived_anchors_allowed",
        "representation_count_as_anchor_allowed",
        "reverse_edge_as_anchor_allowed",
    ):
        if q.get(key) is not False:
            errors.append(f"{key} must remain false")
    generic = q.get("generic_terms", [])
    if not REQUIRED_GENERIC.issubset(set(generic)):
        errors.append("generic-term denylist was weakened")
    if any(not re.fullmatch(r"[a-z]+", term) for term in generic):
        errors.append("generic terms must be normalized lowercase words")

    boundaries = policy.get("boundaries", {})
    required_false = (
        "private_drive_metadata_allowed",
        "automated_truth_inference_allowed",
        "automated_acceptance_allowed",
        "rights_promotion_allowed",
        "scientific_evidence_promotion_allowed",
        "canonical_identity_promotion_allowed",
        "circular_confidence_allowed",
    )
    for key in required_false:
        if boundaries.get(key) is not False:
            errors.append(f"boundary must remain false: {key}")

    generic_examples = [{"type": "GENERIC_TERM", "normalized_value": "sacred"}]
    if qualifies(policy, generic_examples):
        errors.append("generic single-token match qualified unexpectedly")
    return sorted(set(errors))


def main() -> int:
    policy = json.loads(POLICY.read_text(encoding="utf-8"))
    errors = validate(policy)
    print(json.dumps({
        "policy_version": policy.get("policy_version"),
        "direct_anchor_minimum": policy.get("qualification", {}).get("direct_anchor_minimum"),
        "corroborating_anchor_minimum": policy.get("qualification", {}).get("corroborating_anchor_minimum"),
        "automated_acceptance_allowed": False,
        "automated_truth_inference_allowed": False,
    }, sort_keys=True))
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("AKASHICNET CROSS-SOURCE CANDIDATE QUALIFICATION v0.1.2 PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
