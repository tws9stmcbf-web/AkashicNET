#!/usr/bin/env python3

from __future__ import annotations

import json
import sys
from pathlib import Path

LABELS = {
    "Established Evidence",
    "Interpretation",
    "Lived Experience/Testimony",
    "Hypothesis",
    "Speculation",
}
REQUIRED_MODELS = {"MODEL-BQ001-CONTINUITY", "MODEL-BQ001-BIOLOGICAL-DEPENDENCE"}
FORBIDDEN_SOURCE_TYPES_FOR_ESTABLISHED = {"FRAMEWORK_PLACEHOLDER", "AI_SYNTHESIS", "TESTIMONY_ONLY"}


def fail(msg: str) -> None:
    raise ValueError(msg)


def validate(payload: dict) -> None:
    if payload.get("id") != "BQ001":
        fail("id must be BQ001")
    if payload.get("status") != "UNRESOLVED":
        fail("BQ001 seed must remain UNRESOLVED")
    if payload.get("conclusion_policy") != "UNDETERMINED_AT_INGESTION":
        fail("conclusion must be undetermined at ingestion")
    if set(payload.get("canonical_evidence_labels", [])) != LABELS:
        fail("BQ001 must use the exact v0.10 public evidence labels")

    models = payload.get("models")
    if not isinstance(models, list) or len(models) < 2:
        fail("at least two competing models are required")
    model_ids = {m.get("model_id") for m in models}
    if not REQUIRED_MODELS.issubset(model_ids):
        fail("required competing seed models are missing")
    if any(m.get("status") != "UNRESOLVED" for m in models):
        fail("seed model status must remain UNRESOLVED")

    sources = payload.get("sources", [])
    source_map = {s.get("source_id"): s for s in sources}
    if len(source_map) != len(sources):
        fail("source IDs must be unique")

    claims = payload.get("claims")
    if not isinstance(claims, list) or not claims:
        fail("at least one scoped project-state claim is required")
    claim_ids = set()
    for claim in claims:
        cid = claim.get("claim_id")
        if not cid or cid in claim_ids:
            fail("claim IDs must be present and unique")
        claim_ids.add(cid)
        label = claim.get("evidence_label")
        if label not in LABELS:
            fail(f"{cid}: invalid evidence label")
        provenance = claim.get("provenance")
        if not isinstance(provenance, list) or not provenance:
            fail(f"{cid}: provenance is required")
        if not isinstance(claim.get("uncertainty"), str) or not claim["uncertainty"].strip():
            fail(f"{cid}: uncertainty is required")
        for sid in claim.get("source_ids", []):
            if sid not in source_map:
                fail(f"{cid}: unknown source {sid}")
        if label == "Established Evidence":
            if claim.get("reviewed_support") is not True:
                fail(f"{cid}: Established Evidence requires reviewed_support=true")
            for sid in claim.get("source_ids", []):
                if source_map[sid].get("source_type") in FORBIDDEN_SOURCE_TYPES_FOR_ESTABLISHED:
                    fail(f"{cid}: forbidden source type for Established Evidence")
        if label == "Lived Experience/Testimony" and claim.get("universalised") is True:
            fail(f"{cid}: testimony may not be universalised")

    graph = payload.get("graph", {})
    if graph.get("truth_inference_allowed") is not False:
        fail("graph truth inference must remain false")
    if graph.get("edge_state_may_upgrade_evidence") is not False:
        fail("graph edges may not upgrade evidence")

    guards = payload.get("promotion_guards", {})
    required_true = {
        "testimony_may_not_auto_promote_to_established_evidence",
        "source_count_may_not_upgrade_evidence",
        "retrieval_rank_may_not_upgrade_evidence",
        "semantic_similarity_may_not_upgrade_evidence",
        "tradition_longevity_may_not_upgrade_evidence",
        "ai_synthesis_may_not_be_primary_source",
    }
    for key in required_true:
        if guards.get(key) is not True:
            fail(f"promotion guard must remain true: {key}")
    if guards.get("rights_promotion_allowed") is not False:
        fail("rights promotion must remain false")
    if guards.get("scientific_truth_inference_allowed") is not False:
        fail("scientific truth inference must remain false")

    open_questions = payload.get("open_questions")
    if not isinstance(open_questions, list) or len(open_questions) < 2:
        fail("open questions must remain first-class data")


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: validate_bq001_v01.py <spec.json>", file=sys.stderr)
        return 2
    try:
        payload = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
        validate(payload)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"BQ001 FAIL: {exc}", file=sys.stderr)
        return 1
    print("BQ001 PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
