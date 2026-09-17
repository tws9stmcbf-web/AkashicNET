#!/usr/bin/env python3
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ATLAS = ROOT / "references/big-questions/BQ002/evidence-atlas-level5-review-candidate-v0.1.json"
SPEC = ROOT / "references/big-questions/BQ002/spec-v0.1.json"

EXPECTED_SOURCES = {
    "SRC-BQ002-HUDACHEK-WAMSLEY-2023", "SRC-BQ002-FOX-2015",
    "SRC-BQ002-CHRISTOFF-2016", "SRC-BQ002-SMALLWOOD-SCHOOLER-2015",
    "SRC-BQ002-BARSALOU-2008", "SRC-BQ002-FRISTON-KIEBEL-2009",
    "SRC-BQ002-BRUINEBERG-2018", "SRC-BQ002-SELI-2018",
}
EXPECTED_CLAIMS = {
    "CLAIM-BQ002-ATLAS-DREAM-MEMORY-01": "Established Evidence",
    "CLAIM-BQ002-ATLAS-NETWORKS-01": "Established Evidence",
    "CLAIM-BQ002-ATLAS-SPONTANEOUS-01": "Interpretation",
    "CLAIM-BQ002-ATLAS-GROUNDED-01": "Interpretation",
    "CLAIM-BQ002-ATLAS-PREDICTIVE-01": "Hypothesis",
    "CLAIM-BQ002-ATLAS-PHENOMENAL-01": "Interpretation",
}
FALSE_GUARDS = {
    "public_beta_gate", "canonical_promotion_applied", "evidence_promotion_applied",
    "public_synthesis_updated", "website_updated", "truth_inference_allowed",
    "scientific_evidence_promotion_allowed", "transpersonal_claim_promoted",
    "rights_promotion_allowed", "privacy_posture_changed", "cultural_safeguarding_relaxed",
}


def fail(message):
    raise ValueError(message)


def validate(atlas, spec):
    if atlas.get("status") != "REVIEW_CANDIDATE":
        fail("evidence atlas must remain a review candidate")
    if atlas.get("question_id") != "BQ002" or atlas.get("question_status") != "UNRESOLVED":
        fail("BQ002 must remain UNRESOLVED")
    maturity = atlas.get("maturity", {})
    if maturity.get("current_level") != 4 or maturity.get("candidate_level") != 5:
        fail("atlas must describe the bounded Level 4 to Level 5 transition")
    if maturity.get("candidate_level_applied") is not False:
        fail("Level 5 may not be applied before review")
    meaning = maturity.get("meaning", "").lower()
    for phrase in ("research maturity", "not truth probability", "evidence strength", "transpersonal support"):
        if phrase not in meaning:
            fail("maturity meaning must remain claim bounded")

    scope = atlas.get("scope", {})
    for key in ("complete_origin_theory_claimed", "phenomenology_resolved", "transpersonal_information_established", "source_count_advances_level"):
        if scope.get(key) is not False:
            fail(f"scope boundary weakened: {key}")

    sources = atlas.get("sources", [])
    source_map = {item.get("source_id"): item for item in sources}
    if set(source_map) != EXPECTED_SOURCES or len(source_map) != len(sources):
        fail("source set changed or duplicated")
    for source in sources:
        if not source.get("title") or not source.get("url") or not source.get("doi"):
            fail("source provenance incomplete")
        if not source.get("limitations"):
            fail("every source requires limitations")

    allowed_labels = set(spec.get("canonical_evidence_labels", []))
    claims = atlas.get("claims", [])
    claim_map = {item.get("claim_id"): item for item in claims}
    if set(claim_map) != set(EXPECTED_CLAIMS) or len(claim_map) != len(claims):
        fail("claim set changed or duplicated")
    used_sources = set()
    for claim_id, claim in claim_map.items():
        label = claim.get("evidence_label")
        if label != EXPECTED_CLAIMS[claim_id] or label not in allowed_labels:
            fail("claim evidence label changed")
        source_ids = claim.get("source_ids", [])
        counter_ids = claim.get("counter_source_ids", [])
        if not source_ids or not set(source_ids + counter_ids).issubset(EXPECTED_SOURCES):
            fail("claim source binding invalid")
        if claim.get("supports_models") != []:
            fail("claim model support must remain empty")
        if not claim.get("limitations") or not claim.get("unresolved_gap"):
            fail("claim limitations or unresolved gap missing")
        used_sources.update(source_ids)
        used_sources.update(counter_ids)
    if used_sources != EXPECTED_SOURCES:
        fail("every source must be used by a bounded claim or counter-interpretation")

    domains = set(spec.get("domains", []))
    coverage = atlas.get("coverage", [])
    if {item.get("domain") for item in coverage} != domains or len(coverage) != len(domains):
        fail("all existing BQ002 domains must be mapped exactly once")
    for item in coverage:
        ids = item.get("claim_ids", [])
        if not ids or not set(ids).issubset(claim_map):
            fail("coverage claim binding invalid")

    rights = atlas.get("rights", {})
    if rights.get("record_type") != "bibliographic_metadata_and_bounded_summary":
        fail("rights scope changed")
    for key in ("full_text_republished", "audio_or_transcript_republished", "quotations_republished"):
        if rights.get(key) is not False:
            fail("rights boundary weakened")

    governance = atlas.get("governance", {})
    if governance.get("question_status") != "UNRESOLVED":
        fail("governed question status changed")
    if governance.get("accepted_canonical_edges") != 0 or governance.get("supports_models") != []:
        fail("canonical/model edges must remain empty")
    for key in FALSE_GUARDS:
        if governance.get(key) is not False:
            fail(f"governance guard weakened: {key}")


def main():
    try:
        validate(json.loads(ATLAS.read_text(encoding="utf-8")), json.loads(SPEC.read_text(encoding="utf-8")))
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"BQ002 LEVEL 5 EVIDENCE ATLAS FAIL: {exc}", file=sys.stderr)
        return 1
    print("BQ002 LEVEL 5 EVIDENCE ATLAS PASS: review candidate; BQ002 UNRESOLVED; accepted edges 0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
