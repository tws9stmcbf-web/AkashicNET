#!/usr/bin/env python3

from __future__ import annotations

import json
import sys
from pathlib import Path

EXPECTED_SOURCE_IDS = {
    "SRC-BQ001-ELHAJ-2019",
    "SRC-BQ001-SOW-2022",
    "SRC-BQ001-SEDIKIDES-2023",
    "SRC-BQ001-MARTIAL-2022",
    "SRC-BQ001-MARTIAL-2025",
}
EXPECTED_GUARDS = {
    "psychological_self_continuity_equals_metaphysical_identity": False,
    "memory_dependence_proves_non_survival": False,
    "methodological_critique_proves_non_survival": False,
    "neuroscientific_model_proves_complete_explanation": False,
    "review_article_counts_as_primary_experiment": False,
    "model_support_edges_upgrade_evidence": False,
}
ALLOWED_LABELS = {"Established Evidence", "Interpretation"}
PRIMARY = "PRIMARY_PEER_REVIEWED_STUDY"


def fail(message: str) -> None:
    raise ValueError(message)


def validate(data: dict) -> None:
    if data.get("batch_id") != "BQ001-BATCH2-MEMORY-IDENTITY-NDE-METHODS":
        fail("unexpected batch_id")
    if data.get("question_id") != "BQ001":
        fail("question_id must be BQ001")
    if data.get("question_status") != "UNRESOLVED":
        fail("BQ001 must remain UNRESOLVED")
    if data.get("taxonomy_ref") != "references/community/evidence-taxonomy-v0.10.json":
        fail("batch must remain bound to evidence taxonomy v0.10")

    sources = data.get("sources")
    if not isinstance(sources, list) or len(sources) != 5:
        fail("Batch 2 must contain exactly five seed sources")
    source_map = {s.get("source_id"): s for s in sources}
    if set(source_map) != EXPECTED_SOURCE_IDS:
        fail("Batch 2 source set changed")
    if len(source_map) != len(sources):
        fail("source IDs must be unique")

    for sid, source in source_map.items():
        if not source.get("doi") or not source.get("url", "").startswith("https://"):
            fail(f"{sid}: reproducible DOI and HTTPS URL required")
        if not source.get("limitations"):
            fail(f"{sid}: limitations required")
        if source.get("source_type") not in {
            PRIMARY,
            "PEER_REVIEWED_REVIEW",
            "PEER_REVIEWED_COMMENTARY",
        }:
            fail(f"{sid}: unsupported source type")

    claims = data.get("claims")
    if not isinstance(claims, list) or len(claims) != 5:
        fail("Batch 2 must contain exactly five scoped claims")
    claim_ids = set()
    for claim in claims:
        cid = claim.get("claim_id")
        if not cid or cid in claim_ids:
            fail("claim IDs must be present and unique")
        claim_ids.add(cid)
        if claim.get("evidence_label") not in ALLOWED_LABELS:
            fail(f"{cid}: unsupported evidence label")
        if claim.get("claim_type") not in {"OBSERVATION", "INTERPRETATION"}:
            fail(f"{cid}: invalid claim type")
        if not claim.get("provenance") or not claim.get("limitations") or not claim.get("uncertainty"):
            fail(f"{cid}: provenance, limitations and uncertainty are required")
        source_ids = claim.get("source_ids")
        if not isinstance(source_ids, list) or not source_ids:
            fail(f"{cid}: at least one source link required")
        for sid in source_ids:
            if sid not in source_map:
                fail(f"{cid}: unknown source {sid}")
        if claim.get("evidence_label") == "Established Evidence":
            if claim.get("claim_type") != "OBSERVATION":
                fail(f"{cid}: Established Evidence must be encoded as an observation in this batch")
            if any(source_map[sid].get("source_type") != PRIMARY for sid in source_ids):
                fail(f"{cid}: review/commentary cannot silently become primary Established Evidence")
        if claim.get("claim_type") == "INTERPRETATION" and claim.get("evidence_label") != "Interpretation":
            fail(f"{cid}: interpretation must retain Interpretation evidence label")

    conclusion = data.get("batch_conclusion", {})
    if conclusion.get("status") != "UNRESOLVED":
        fail("Batch 2 conclusion must remain UNRESOLVED")
    statement = conclusion.get("statement", "").lower()
    if not statement:
        fail("Batch 2 conclusion statement required")
    forbidden_conclusion_phrases = (
        "proves survival",
        "proves non-survival",
        "proves consciousness survives",
        "proves consciousness ends",
        "establishes post-mortem survival",
        "establishes the impossibility",
    )
    if any(phrase in statement for phrase in forbidden_conclusion_phrases):
        fail("Batch 2 conclusion contains forbidden ontological promotion")

    guards = data.get("promotion_guards", {})
    for key, expected in EXPECTED_GUARDS.items():
        if guards.get(key) is not expected:
            fail(f"promotion guard changed: {key}")

    for claim in claims:
        text = claim.get("text", "").lower()
        if "self-continuity" in text and "post-mortem identity" in text and claim.get("evidence_label") == "Established Evidence":
            fail("psychological self-continuity may not be promoted into post-mortem identity")
        if "complete mechanistic proof" in text or "proves non-survival" in text:
            fail("claim contains forbidden completeness/non-survival promotion")


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: validate_bq001_batch2_v01.py <evidence-batch2.json>", file=sys.stderr)
        return 2
    try:
        payload = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
        validate(payload)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"BQ001 BATCH2 FAIL: {exc}", file=sys.stderr)
        return 1
    print("BQ001 BATCH2 PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
