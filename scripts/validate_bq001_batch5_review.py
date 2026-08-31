#!/usr/bin/env python3

import json
import sys
from pathlib import Path

EXPECTED_SOURCES = {
    "SRC-BQ001-XU-PNAS-2023",
    "SRC-BQ001-COGITATE-2025",
    "SRC-BQ001-PARNIA-GUIDELINES-2022",
}
EXPECTED_EXTERNAL_SOURCES = {"SRC-BQ001-MARTIAL-2022"}
ALLOWED_LABELS = {
    "Established Evidence",
    "Interpretation",
    "Lived Experience/Testimony",
    "Hypothesis",
    "Speculation",
}
REQUIRED_GUARDS_FALSE = {
    "neural_activity_proves_conscious_experience",
    "dying_process_equals_post_mortem_survival",
    "theory_challenge_resolves_consciousness",
    "consensus_language_counts_as_primary_evidence",
    "methodological_consensus_proves_survival_or_non_survival",
    "model_support_edges_upgrade_evidence",
    "canonical_promotion_applied",
    "public_synthesis_updated",
    "website_updated",
}


def fail(message):
    raise ValueError(message)


def validate(data):
    if data.get("batch_id") != "BQ001-BATCH5-ADJUDICATED-SUPPLEMENTAL-SCIENCE":
        fail("unexpected batch_id")
    if data.get("status") != "REVIEW_CANDIDATE":
        fail("batch 5 must remain REVIEW_CANDIDATE")
    if data.get("question_id") != "BQ001" or data.get("question_status") != "UNRESOLVED":
        fail("BQ001 must remain UNRESOLVED")
    if data.get("taxonomy_ref") != "references/community/evidence-taxonomy-v0.10.json":
        fail("evidence taxonomy binding required")

    sources = data.get("sources")
    if not isinstance(sources, list) or len(sources) != 3:
        fail("exactly three adjudicated source candidates required")
    source_map = {source.get("source_id"): source for source in sources}
    if set(source_map) != EXPECTED_SOURCES or len(source_map) != len(sources):
        fail("source candidate set changed or contains duplicates")

    for sid, source in source_map.items():
        if not source.get("doi") or not source.get("url", "").startswith("https://"):
            fail(f"{sid}: DOI and HTTPS URL required")
        if not source.get("limitations"):
            fail(f"{sid}: limitations required")
        check = source.get("link_check", {})
        if check.get("status") != "AVAILABLE" or check.get("title_match") is not True:
            fail(f"{sid}: successful link and title check required")
        if check.get("retraction_notice") != "NO_NOTICE_OBSERVED_AT_CHECK_TIME":
            fail(f"{sid}: time-scoped retraction check metadata required")

    external = set(data.get("external_source_ids", []))
    if external != EXPECTED_EXTERNAL_SOURCES:
        fail("required Martial 2022 external critique link changed")

    claims = data.get("claims")
    if not isinstance(claims, list) or len(claims) != 3:
        fail("exactly three review claims required")
    seen = set()
    for claim in claims:
        cid = claim.get("claim_id")
        if not cid or cid in seen:
            fail("claim IDs must be present and unique")
        seen.add(cid)
        if claim.get("evidence_label") not in ALLOWED_LABELS:
            fail(f"{cid}: invalid evidence label")
        if not claim.get("provenance") or not claim.get("limitations") or not claim.get("uncertainty"):
            fail(f"{cid}: provenance, limitations and uncertainty required")
        for sid in claim.get("source_ids", []):
            if sid not in source_map and sid not in external:
                fail(f"{cid}: unknown source {sid}")
        if claim.get("claim_type") == "INTERPRETATION" and claim.get("evidence_label") != "Interpretation":
            fail(f"{cid}: interpretation label promotion")
        if claim.get("evidence_label") == "Established Evidence" and claim.get("claim_type") != "OBSERVATION":
            fail(f"{cid}: Established Evidence must be an observation")
        text = claim.get("text", "").lower()
        for phrase in ("proves consciousness", "proves survival", "proves non-survival", "establishes post-mortem"):
            if phrase in text:
                fail(f"{cid}: forbidden overclaim")

    conclusion = data.get("batch_conclusion", {})
    if conclusion.get("status") != "UNRESOLVED" or not conclusion.get("statement"):
        fail("batch conclusion must remain explicit and UNRESOLVED")

    guards = data.get("promotion_guards", {})
    for key in REQUIRED_GUARDS_FALSE:
        if guards.get(key) is not False:
            fail(f"promotion guard must remain false: {key}")

    adjudication = data.get("adjudication", {})
    if adjudication.get("decision") != "REVIEW_CANDIDATE":
        fail("adjudication must remain review-only")
    for key in (
        "canonical_promotion_applied",
        "public_synthesis_updated",
        "website_updated",
        "truth_inference_allowed",
        "scientific_evidence_promotion_allowed",
        "model_edges_upgrade_evidence",
    ):
        if adjudication.get(key) is not False:
            fail(f"adjudication guard must remain false: {key}")


def main():
    if len(sys.argv) != 2:
        print("usage: validate_bq001_batch5_review.py <batch.json>", file=sys.stderr)
        return 2
    try:
        validate(json.loads(Path(sys.argv[1]).read_text(encoding="utf-8")))
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"BQ001 BATCH5 REVIEW FAIL: {exc}", file=sys.stderr)
        return 1
    print("BQ001 BATCH5 REVIEW PASS: review candidate only; BQ001 remains UNRESOLVED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
