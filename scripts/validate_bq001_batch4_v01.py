#!/usr/bin/env python3

import json
import sys
from pathlib import Path

REQUIRED_GUARDS = {
    "tradition_longevity_upgrades_evidence": False,
    "spiritual_authority_upgrades_evidence": False,
    "cross_tradition_similarity_upgrades_evidence": False,
    "meditation_self_change_proves_metaphysical_nonself": False,
    "philosophical_coherence_proves_survival": False,
    "physicalism_as_philosophy_proves_non_survival": False,
    "dualism_as_philosophy_proves_survival": False,
    "panpsychism_entails_personal_survival": False,
    "model_support_edges_upgrade_evidence": False,
}

ALLOWED_LABELS = {"Interpretation", "Established Evidence", "Lived Experience/Testimony", "Hypothesis", "Speculation"}
PHILOSOPHY_SOURCE_TYPES = {"SCHOLARLY_PHILOSOPHY_CHAPTER", "SCHOLARLY_REFERENCE_ENTRY"}


def fail(msg):
    raise ValueError(msg)


def validate(payload):
    if payload.get("batch_id") != "BQ001-BATCH4-CONTEMPLATIVE-PHILOSOPHY":
        fail("wrong batch id")
    if payload.get("question_id") != "BQ001" or payload.get("question_status") != "UNRESOLVED":
        fail("BQ001 must remain UNRESOLVED")

    sources = payload.get("sources", [])
    claims = payload.get("claims", [])
    if len(sources) < 6 or len(claims) < 6:
        fail("Batch 4 requires at least six sources and six claims")
    source_map = {s.get("source_id"): s for s in sources}
    if len(source_map) != len(sources):
        fail("source ids must be unique")

    for source in sources:
        if not source.get("url", "").startswith("https://"):
            fail("all sources require HTTPS provenance")
        if not source.get("limitations"):
            fail("every source requires limitations")

    for claim in claims:
        cid = claim.get("claim_id")
        if claim.get("evidence_label") not in ALLOWED_LABELS:
            fail(f"{cid}: invalid evidence label")
        if not claim.get("source_ids") or not claim.get("provenance") or not claim.get("limitations") or not claim.get("uncertainty"):
            fail(f"{cid}: provenance, limitations and uncertainty required")
        for sid in claim["source_ids"]:
            if sid not in source_map:
                fail(f"{cid}: unknown source {sid}")
        if any(source_map[sid].get("source_type") in PHILOSOPHY_SOURCE_TYPES for sid in claim["source_ids"]):
            if claim.get("evidence_label") == "Established Evidence":
                fail(f"{cid}: philosophy/reference source cannot establish an empirical BQ001 claim")
        text = (claim.get("text") or "").lower()
        if "proves survival" in text or "proves non-survival" in text or "establishes reincarnation" in text:
            fail(f"{cid}: forbidden overclaim")

    guards = payload.get("promotion_guards", {})
    for key, expected in REQUIRED_GUARDS.items():
        if guards.get(key) is not expected:
            fail(f"guard violated: {key}")

    conclusion = payload.get("batch_conclusion", {})
    if conclusion.get("status") != "UNRESOLVED":
        fail("batch conclusion must remain UNRESOLVED")


def main():
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
