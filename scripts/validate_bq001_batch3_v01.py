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
REQUIRED_GUARDS_FALSE = {
    "case_match_proves_reincarnation",
    "retrospective_case_equals_prospective_controlled_test",
    "cultural_belief_proves_or_disproves_reincarnation",
    "failure_of_psychological_explanation_proves_reincarnation",
    "psychological_correlates_disprove_reincarnation",
    "field_investigator_review_counts_as_independent_replication",
    "model_support_edges_upgrade_evidence",
}


def fail(msg: str) -> None:
    raise ValueError(msg)


def validate(data: dict) -> None:
    if data.get("batch_id") != "BQ001-BATCH3-REINCARNATION-METHODS":
        fail("unexpected batch_id")
    if data.get("question_id") != "BQ001" or data.get("question_status") != "UNRESOLVED":
        fail("BQ001 must remain UNRESOLVED")

    sources = data.get("sources")
    if not isinstance(sources, list) or len(sources) < 5:
        fail("at least five reproducible sources are required")
    source_map = {}
    for source in sources:
        sid = source.get("source_id")
        if not sid or sid in source_map:
            fail("source IDs must be present and unique")
        source_map[sid] = source
        url = source.get("url")
        if not isinstance(url, str) or not url.startswith("https://"):
            fail(f"{sid}: HTTPS source URL required")
        if not isinstance(source.get("limitations"), list) or not source["limitations"]:
            fail(f"{sid}: source limitations required")

    claims = data.get("claims")
    if not isinstance(claims, list) or len(claims) < 4:
        fail("at least four claims are required")
    seen = set()
    for claim in claims:
        cid = claim.get("claim_id")
        if not cid or cid in seen:
            fail("claim IDs must be present and unique")
        seen.add(cid)
        if claim.get("evidence_label") not in ALLOWED_LABELS:
            fail(f"{cid}: invalid evidence label")
        if claim.get("domain") != "reincarnation_case_research_and_critiques":
            fail(f"{cid}: wrong domain")
        if not claim.get("provenance"):
            fail(f"{cid}: provenance required")
        if not claim.get("limitations"):
            fail(f"{cid}: limitations required")
        if not isinstance(claim.get("uncertainty"), str) or not claim["uncertainty"].strip():
            fail(f"{cid}: uncertainty required")
        if not isinstance(claim.get("methodological_risks"), list) or not claim["methodological_risks"]:
            fail(f"{cid}: methodological_risks required")
        for sid in claim.get("source_ids", []):
            if sid not in source_map:
                fail(f"{cid}: unknown source {sid}")
        if claim.get("claim_type") == "INTERPRETATION" and claim.get("evidence_label") == "Established Evidence":
            fail(f"{cid}: interpretation may not be labelled Established Evidence")
        text = claim.get("text", "").lower()
        if "proves reincarnation" in text or "reincarnation is proven" in text:
            fail(f"{cid}: forbidden reincarnation proof promotion")

    conclusion = data.get("batch_conclusion", {})
    if conclusion.get("status") != "UNRESOLVED":
        fail("batch conclusion must remain UNRESOLVED")

    guards = data.get("promotion_guards", {})
    for key in REQUIRED_GUARDS_FALSE:
        if guards.get(key) is not False:
            fail(f"promotion guard must remain false: {key}")


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: validate_bq001_batch3_v01.py <batch.json>", file=sys.stderr)
        return 2
    try:
        data = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
        validate(data)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"BQ001 BATCH3 FAIL: {exc}", file=sys.stderr)
        return 1
    print("BQ001 BATCH3 PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
