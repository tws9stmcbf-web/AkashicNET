#!/usr/bin/env python3
"""Validate Batch 6 as review-only; validation is never promotion approval."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BATCH = "references/big-questions/BQ001/evidence-batch6-review-candidates-v0.1.json"
OLD_BATCH = "references/big-questions/BQ001/evidence-batch6-v0.1.json"
REQUIRED_FALSE_GUARDS = {
    "reports_or_associations_prove_reincarnation",
    "xenoglossy_coding_authenticates_transferred_language",
    "follow_up_impact_proves_historical_accuracy",
    "dream_content_proves_past_life_memory",
    "hypnotic_vividness_authenticates_memory",
    "source_counting_upgrades_evidence",
    "truth_inference_allowed",
    "scientific_evidence_auto_promotion_allowed",
    "rights_promotion_allowed",
    "canonical_promotion_applied",
    "public_synthesis_updated",
    "public_export_allowed",
    "privacy_promotion_allowed",
    "publication_promotion_allowed",
}


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def validate(data, spec):
    if data.get("batch_id") != "BQ001-BATCH6-REINCARNATION-DREAM-MEMORY":
        raise ValueError("unexpected Batch 6 identity")
    if data.get("status") != "REVIEW_CANDIDATE":
        raise ValueError("Batch 6 must remain REVIEW_CANDIDATE pending separate approval")
    if data.get("question_id") != "BQ001" or data.get("question_status") != "UNRESOLVED":
        raise ValueError("BQ001 must remain UNRESOLVED")
    if data.get("batch_conclusion", {}).get("status") != "UNRESOLVED":
        raise ValueError("Batch 6 conclusion must remain UNRESOLVED")
    if not data.get("review_boundary") or "public_route" in data:
        raise ValueError("explicit review-only boundary required; no public route")
    for key in REQUIRED_FALSE_GUARDS:
        if data.get("promotion_guards", {}).get(key) is not False:
            raise ValueError(f"promotion guard must remain false: {key}")
    sources = data.get("sources", [])
    source_ids = {source.get("source_id") for source in sources}
    if len(sources) != 5 or len(source_ids) != 5 or None in source_ids:
        raise ValueError("five distinct source records required")
    for source in sources:
        if any(not source.get(key) for key in ("url", "rights", "retrieval_result", "limitations")):
            raise ValueError("source provenance, rights and limitations required")
    claims = data.get("claims", [])
    if len(claims) != 5 or len({c.get("claim_id") for c in claims}) != 5:
        raise ValueError("five distinct review claims required")
    for claim in claims:
        if claim.get("domain") not in spec["domains"]:
            raise ValueError(f"domain drift: {claim.get('domain')}")
        if claim.get("supports_models") != []:
            raise ValueError("supports_models must remain []")
        if not claim.get("source_ids") or not set(claim["source_ids"]) <= source_ids:
            raise ValueError("claim requires traceable source_ids")
        if any(not claim.get(key) for key in ("claim_id", "provenance", "limitations", "uncertainty")):
            raise ValueError("claim identity and evidence boundaries required")
        if claim.get("evidence_label") not in spec["canonical_evidence_labels"]:
            raise ValueError("unknown proposed evidence label")


def validate_repository(root=ROOT):
    data = load(root / BATCH)
    validate(data, load(root / "references/big-questions/BQ001/spec-v0.1.json"))
    batches = load(root / "references/big-questions/architecture-v0.1.json")["questions"]["BQ001"]["evidence_batches"]
    if batches.count(BATCH) != 1 or OLD_BATCH in batches or (root / OLD_BATCH).exists():
        raise ValueError("Batch 6 must be registered only at its review-candidates path")
    synthesis = load(root / "references/big-questions/BQ001/public-synthesis-v0.1.json")
    if any(path in synthesis.get("source_batches", []) for path in (BATCH, OLD_BATCH)):
        raise ValueError("Batch 6 cannot enter public synthesis before separate approval")
    claim_ids = {c["claim_id"] for c in data["claims"]}
    source_ids = {s["source_id"] for s in data["sources"]}
    for section in synthesis.get("sections", []):
        if claim_ids.intersection(section.get("claim_ids", [])) or source_ids.intersection(section.get("source_ids", [])):
            raise ValueError("review-only Batch 6 claims/sources leaked into public synthesis")


if __name__ == "__main__":
    validate_repository()
    print("BQ001 BATCH6 REVIEW PASS: review-only; domains canonical; no synthesis promotion")
