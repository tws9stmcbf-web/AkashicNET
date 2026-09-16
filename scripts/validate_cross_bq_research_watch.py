#!/usr/bin/env python3
import json
import sys
from pathlib import Path

EXPECTED_SOURCES = {
    "SRC-CROSSBQ-WALLECZEK-TPP-2025",
    "SRC-CROSSBQ-MARTIAL-NEPTUNE-2025",
    "SRC-CROSSBQ-BARRETO-NDE-REVIEW-2025",
    "SRC-CROSSBQ-KOVAROVA-ECPR-NDE-2025",
    "SRC-CROSSBQ-FINCHAM-A2A-2026",
    "SRC-CROSSBQ-RABOURDIN-OBE-2026",
    "SRC-CROSSBQ-GALLO-CERTIFICATION-2026",
    "SRC-CROSSBQ-HOURAN-DRAKES-2025",
    "SRC-CROSSBQ-MAYER-GHOST-HUNTERS-2026",
    "SRC-CROSSBQ-CHARMAN-MEDIUMSHIP-2026",
}
EXPECTED_INSTITUTIONS = {
    "INST-UVA-DOPS",
    "INST-NYU-PARNIA",
    "INST-ULIEGE-COMA",
    "ORG-IANDS",
}
ALLOWED_CURRENT_BQS = {"BQ001", "BQ002"}
ALLOWED_LABELS = {
    "Established Evidence",
    "Interpretation",
    "Lived Experience/Testimony",
    "Hypothesis",
    "Speculation",
}
FALSE_ADJUDICATION_GUARDS = {
    "canonical_promotion_applied",
    "public_synthesis_updated",
    "website_updated",
    "truth_inference_allowed",
    "scientific_evidence_promotion_allowed",
    "rights_promotion_allowed",
    "model_edges_upgrade_evidence",
}

def fail(message):
    raise ValueError(message)

def validate(data):
    if data.get("artifact_id") != "CROSS-BQ-RESEARCH-WATCH-2026-09-16":
        fail("unexpected artifact_id")
    if data.get("status") != "REVIEW_CANDIDATE":
        fail("artifact must remain REVIEW_CANDIDATE")
    scope = data.get("question_scope", {})
    if set(scope.get("current_public_profiles", [])) != ALLOWED_CURRENT_BQS:
        fail("current public BQ scope changed")
    if scope.get("planned_questions_are_not_treated_as_canonical") is not True:
        fail("planned questions must remain noncanonical")
    statuses = data.get("question_status", {})
    if statuses != {"BQ001": "UNRESOLVED", "BQ002": "UNRESOLVED"}:
        fail("current BQs must remain UNRESOLVED")

    sources = data.get("sources")
    if not isinstance(sources, list) or len(sources) != len(EXPECTED_SOURCES):
        fail("exact source candidate count required")
    source_map = {item.get("source_id"): item for item in sources}
    if set(source_map) != EXPECTED_SOURCES or len(source_map) != len(sources):
        fail("source set changed or contains duplicates")
    for sid, source in source_map.items():
        if not source.get("doi") or not source.get("url", "").startswith("https://"):
            fail(f"{sid}: DOI and HTTPS URL required")
        if not source.get("limitations"):
            fail(f"{sid}: limitations required")
        links = source.get("candidate_bq_links")
        if not isinstance(links, list) or not links or not set(links).issubset(ALLOWED_CURRENT_BQS):
            fail(f"{sid}: nonempty current-BQ candidate mapping required")
        check = source.get("link_check", {})
        if check.get("status") != "AVAILABLE" or check.get("title_match") is not True:
            fail(f"{sid}: link and title check required")
        if check.get("retraction_notice") != "NO_NOTICE_OBSERVED_AT_CHECK_TIME":
            fail(f"{sid}: time-scoped retraction metadata required")

    held = source_map["SRC-CROSSBQ-CHARMAN-MEDIUMSHIP-2026"]
    if held.get("review_disposition") != "HOLD_PENDING_FULL_TEXT_METHOD_REVIEW":
        fail("single mediumship case must remain on methodological hold")
    for sid in EXPECTED_SOURCES - {"SRC-CROSSBQ-CHARMAN-MEDIUMSHIP-2026"}:
        disposition = source_map[sid].get("review_disposition")
        if disposition not in (None, "REVIEW_CANDIDATE"):
            fail(f"{sid}: unexpected review disposition")

    institutions = data.get("research_institution_watch")
    if not isinstance(institutions, list) or len(institutions) != len(EXPECTED_INSTITUTIONS):
        fail("exact institutional watch count required")
    institution_map = {item.get("institution_id"): item for item in institutions}
    if set(institution_map) != EXPECTED_INSTITUTIONS or len(institution_map) != len(institutions):
        fail("institutional watch set changed or contains duplicates")
    for iid, institution in institution_map.items():
        if not institution.get("url", "").startswith("https://"):
            fail(f"{iid}: HTTPS URL required")
        if not institution.get("topics") or not institution.get("evidence_boundary"):
            fail(f"{iid}: topics and evidence boundary required")
    if institution_map["ORG-IANDS"].get("role") != "SPECIALIST_NONPROFIT_JOURNAL_REGISTRY_AND_SUPPORT_NETWORK":
        fail("IANDS must remain distinguished from academic research groups")

    claims = data.get("claims")
    if not isinstance(claims, list) or len(claims) != len(EXPECTED_SOURCES):
        fail("one bounded claim per source required")
    seen = set()
    claimed_source_ids = []
    for claim in claims:
        cid = claim.get("claim_id")
        if not cid or cid in seen:
            fail("claim IDs must be present and unique")
        seen.add(cid)
        if claim.get("evidence_label") not in ALLOWED_LABELS:
            fail(f"{cid}: invalid evidence label")
        if not claim.get("uncertainty") or not claim.get("movement_type"):
            fail(f"{cid}: uncertainty and movement type required")
        if claim.get("supports_models") != []:
            fail(f"{cid}: supports_models must remain empty")
        links = claim.get("candidate_bq_links")
        if not isinstance(links, list) or not links or not set(links).issubset(ALLOWED_CURRENT_BQS):
            fail(f"{cid}: nonempty current-BQ candidate mapping required")
        source_ids = claim.get("source_ids")
        if not isinstance(source_ids, list) or len(source_ids) != 1:
            fail(f"{cid}: exactly one source binding required")
        sid = source_ids[0]
        if sid not in source_map:
            fail(f"{cid}: unknown source {sid}")
        claimed_source_ids.append(sid)
        if claim.get("claim_type") == "INTERPRETATION" and claim.get("evidence_label") != "Interpretation":
            fail(f"{cid}: interpretation promotion")
        if claim.get("evidence_label") == "Established Evidence" and claim.get("claim_type") != "OBSERVATION":
            fail(f"{cid}: Established Evidence must be observational")
        text = claim.get("text", "").lower()
        for phrase in (
            "proves psi",
            "proves consciousness",
            "proves survival",
            "establishes post-mortem",
            "disproves psi",
        ):
            if phrase in text:
                fail(f"{cid}: forbidden overclaim")
    if set(claimed_source_ids) != EXPECTED_SOURCES or len(set(claimed_source_ids)) != len(claimed_source_ids):
        fail("claims must bind each source exactly once")

    case_claim = next(
        claim for claim in claims
        if claim.get("source_ids") == ["SRC-CROSSBQ-CHARMAN-MEDIUMSHIP-2026"]
    )
    if case_claim.get("claim_type") != "TESTIMONY" or case_claim.get("evidence_label") != "Lived Experience/Testimony":
        fail("held single case must remain testimony, not promoted evidence")

    adjudication = data.get("adjudication", {})
    if adjudication.get("decision") != "REVIEW_CANDIDATE":
        fail("adjudication must remain review-only")
    for key in FALSE_ADJUDICATION_GUARDS:
        if adjudication.get(key) is not False:
            fail(f"guard must remain false: {key}")

    rights = data.get("rights", {})
    if rights.get("full_text_copied") is not False:
        fail("full text must not be copied")
    if rights.get("public_integration_allowed") is not False:
        fail("public integration must remain disabled")
    if rights.get("rights_review_required") is not True:
        fail("rights review must remain required")

    conclusion = data.get("batch_conclusion", {})
    if conclusion.get("status") != "UNRESOLVED" or not conclusion.get("statement"):
        fail("batch conclusion must remain UNRESOLVED")

def main():
    if len(sys.argv) != 2:
        print("usage: validate_cross_bq_research_watch.py <artifact.json>", file=sys.stderr)
        return 2
    try:
        validate(json.loads(Path(sys.argv[1]).read_text(encoding="utf-8")))
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"CROSS-BQ RESEARCH WATCH FAIL: {exc}", file=sys.stderr)
        return 1
    print("CROSS-BQ RESEARCH WATCH PASS: review candidates only; BQ001 and BQ002 remain UNRESOLVED")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
