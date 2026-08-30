#!/usr/bin/env python3

from __future__ import annotations

import json
import sys
from pathlib import Path

ALLOWED_LABELS = {
    "Established Evidence",
    "Interpretation",
    "Lived Experience/Testimony",
    "Hypothesis",
    "Speculation",
}
FORBIDDEN_OVERCLAIM_PHRASES = {
    "proves consciousness after death",
    "proves survival after death",
    "proves brain-independent consciousness",
    "proves consciousness cannot survive death",
    "proves non-survival",
}


def fail(message: str) -> None:
    raise ValueError(message)


def validate(payload: dict) -> None:
    if payload.get("batch_id") != "BQ001-BATCH1-SCIENTIFIC-BASELINE":
        fail("unexpected batch_id")
    if payload.get("question_id") != "BQ001":
        fail("question_id must be BQ001")
    if payload.get("question_status") != "UNRESOLVED":
        fail("BQ001 must remain UNRESOLVED")

    sources = payload.get("sources")
    if not isinstance(sources, list) or len(sources) < 4:
        fail("Batch 1 requires at least four source records")
    source_map = {}
    for source in sources:
        sid = source.get("source_id")
        if not sid or sid in source_map:
            fail("source IDs must be non-empty and unique")
        source_map[sid] = source
        if not source.get("url") or not source.get("doi"):
            fail(f"{sid}: reproducible URL and DOI required")
        if not isinstance(source.get("limitations"), list) or not source["limitations"]:
            fail(f"{sid}: source limitations required")

    claims = payload.get("claims")
    if not isinstance(claims, list) or len(claims) < 5:
        fail("Batch 1 requires at least five scoped claims")
    claim_ids = set()
    for claim in claims:
        cid = claim.get("claim_id")
        if not cid or cid in claim_ids:
            fail("claim IDs must be non-empty and unique")
        claim_ids.add(cid)
        if claim.get("evidence_label") not in ALLOWED_LABELS:
            fail(f"{cid}: invalid evidence label")
        if claim.get("claim_type") == "INTERPRETATION" and claim.get("evidence_label") == "Established Evidence":
            fail(f"{cid}: interpretation may not be labelled Established Evidence")
        source_ids = claim.get("source_ids")
        if not isinstance(source_ids, list) or not source_ids:
            fail(f"{cid}: at least one source required")
        for sid in source_ids:
            if sid not in source_map:
                fail(f"{cid}: unknown source {sid}")
        if not isinstance(claim.get("limitations"), list) or not claim["limitations"]:
            fail(f"{cid}: explicit limitations required")
        if not isinstance(claim.get("uncertainty"), str) or not claim["uncertainty"].strip():
            fail(f"{cid}: explicit uncertainty required")
        text = claim.get("text", "").lower()
        for phrase in FORBIDDEN_OVERCLAIM_PHRASES:
            if phrase in text:
                fail(f"{cid}: forbidden overclaim: {phrase}")

    conclusion = payload.get("batch_conclusion", {})
    if conclusion.get("status") != "UNRESOLVED":
        fail("batch conclusion must remain UNRESOLVED")

    guards = payload.get("promotion_guards", {})
    required_false = {
        "model_support_edges_upgrade_evidence",
        "cardiac_arrest_equals_irreversible_death",
        "reported_recall_proves_brain_independent_consciousness",
        "brain_dependence_under_tested_conditions_proves_non_survival",
        "review_article_counts_as_primary_experiment",
    }
    for key in required_false:
        if guards.get(key) is not False:
            fail(f"promotion guard must remain false: {key}")


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: validate_bq001_batch1_v01.py <batch.json>", file=sys.stderr)
        return 2
    try:
        payload = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
        validate(payload)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"BQ001 BATCH1 FAIL: {exc}", file=sys.stderr)
        return 1
    print("BQ001 BATCH1 PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
