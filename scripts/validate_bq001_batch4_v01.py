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
    "contemplative_tradition_proves_metaphysical_claim",
    "historical_longevity_upgrades_evidence",
    "cross_tradition_similarity_upgrades_evidence",
    "meditation_self_processing_proves_ontological_nonself",
    "self_transcendence_proves_nonlocal_consciousness",
    "physicalism_counts_as_empirical_verdict",
    "dualism_counts_as_empirical_verdict",
    "panpsychism_counts_as_empirical_verdict",
    "philosophical_coherence_proves_postmortem_survival",
    "model_support_edges_upgrade_evidence",
}
PHILOSOPHY_SOURCES = {
    "SRC-BQ001-SIDERITS-2011",
    "SRC-BQ001-SEP-PHYSICALISM",
    "SRC-BQ001-SEP-DUALISM",
    "SRC-BQ001-SEP-PANPSYCHISM",
}


def fail(msg: str) -> None:
    raise ValueError(msg)


def validate(data: dict) -> None:
    if data.get("batch_id") != "BQ001-BATCH4-CONTEMPLATIVE-PHILOSOPHY":
        fail("unexpected batch_id")
    if data.get("question_id") != "BQ001" or data.get("question_status") != "UNRESOLVED":
        fail("BQ001 must remain UNRESOLVED")

    sources = data.get("sources")
    if not isinstance(sources, list) or len(sources) < 7:
        fail("at least seven reproducible sources required")
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
    if not isinstance(claims, list) or len(claims) < 6:
        fail("at least six scoped claims required")
    seen = set()
    for claim in claims:
        cid = claim.get("claim_id")
        if not cid or cid in seen:
            fail("claim IDs must be present and unique")
        seen.add(cid)
        label = claim.get("evidence_label")
        if label not in ALLOWED_LABELS:
            fail(f"{cid}: invalid evidence label")
        if claim.get("domain") != "contemplative_philosophical_and_wisdom_traditions":
            fail(f"{cid}: wrong domain")
        if not claim.get("provenance") or not claim.get("limitations"):
            fail(f"{cid}: provenance and limitations required")
        if not isinstance(claim.get("uncertainty"), str) or not claim["uncertainty"].strip():
            fail(f"{cid}: uncertainty required")
        if not isinstance(claim.get("methodological_risks"), list) or not claim["methodological_risks"]:
            fail(f"{cid}: methodological risks required")
        source_ids = claim.get("source_ids", [])
        if not source_ids:
            fail(f"{cid}: source IDs required")
        for sid in source_ids:
            if sid not in source_map:
                fail(f"{cid}: unknown source {sid}")
        if claim.get("claim_type") == "INTERPRETATION" and label == "Established Evidence":
            fail(f"{cid}: interpretation may not be Established Evidence")
        if any(sid in PHILOSOPHY_SOURCES for sid in source_ids) and claim.get("claim_type") != "OBSERVATION":
            if label == "Established Evidence":
                fail(f"{cid}: philosophy may not be promoted to Established Evidence")
        text = claim.get("text", "").lower()
        forbidden = (
            "proves non-self",
            "proves consciousness survives",
            "proves post-mortem survival",
            "proves nonlocal consciousness",
            "physicalism is proven",
            "dualism is proven",
            "panpsychism is proven",
        )
        if any(fragment in text for fragment in forbidden):
            fail(f"{cid}: forbidden metaphysical promotion")

    if data.get("batch_conclusion", {}).get("status") != "UNRESOLVED":
        fail("batch conclusion must remain UNRESOLVED")
    guards = data.get("promotion_guards", {})
    for key in REQUIRED_GUARDS_FALSE:
        if guards.get(key) is not False:
            fail(f"promotion guard must remain false: {key}")


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: validate_bq001_batch4_v01.py <batch.json>", file=sys.stderr)
        return 2
    try:
        validate(json.loads(Path(sys.argv[1]).read_text(encoding="utf-8")))
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"BQ001 BATCH4 FAIL: {exc}", file=sys.stderr)
        return 1
    print("BQ001 BATCH4 PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
