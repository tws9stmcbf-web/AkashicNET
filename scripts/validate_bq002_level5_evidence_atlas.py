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
EXPECTED_SOURCE_IDENTITIES = {
    "SRC-BQ002-HUDACHEK-WAMSLEY-2023": ("10.1093/sleep/zsad111", "37058584", "https://pubmed.ncbi.nlm.nih.gov/37058584/"),
    "SRC-BQ002-FOX-2015": ("10.1016/j.neuroimage.2015.02.039", "25725466", "https://pubmed.ncbi.nlm.nih.gov/25725466/"),
    "SRC-BQ002-CHRISTOFF-2016": ("10.1038/nrn.2016.113", "27654862", "https://pubmed.ncbi.nlm.nih.gov/27654862/"),
    "SRC-BQ002-SMALLWOOD-SCHOOLER-2015": ("10.1146/annurev-psych-010814-015331", "25293689", "https://pubmed.ncbi.nlm.nih.gov/25293689/"),
    "SRC-BQ002-BARSALOU-2008": ("10.1146/annurev.psych.59.103006.093639", "17705682", "https://pubmed.ncbi.nlm.nih.gov/17705682/"),
    "SRC-BQ002-FRISTON-KIEBEL-2009": ("10.1098/rstb.2008.0300", None, "https://pmc.ncbi.nlm.nih.gov/articles/PMC2666703/"),
    "SRC-BQ002-BRUINEBERG-2018": ("10.1007/s11229-016-1239-1", "30996493", "https://pubmed.ncbi.nlm.nih.gov/30996493/"),
    "SRC-BQ002-SELI-2018": ("10.1016/j.tics.2018.03.010", None, "https://doi.org/10.1016/j.tics.2018.03.010"),
}
EXPECTED_CLAIMS = {
    "CLAIM-BQ002-ATLAS-DREAM-MEMORY-01": ("Established Evidence", "OBSERVATION", "dreaming_and_sleep_cognition", {"SRC-BQ002-HUDACHEK-WAMSLEY-2023"}, set()),
    "CLAIM-BQ002-ATLAS-NETWORKS-01": ("Established Evidence", "OBSERVATION", "neural_dynamics_and_predictive_processing", {"SRC-BQ002-FOX-2015"}, {"SRC-BQ002-SELI-2018"}),
    "CLAIM-BQ002-ATLAS-SPONTANEOUS-01": ("Interpretation", "INTERPRETATION", "spontaneous_thought_and_mind_wandering", {"SRC-BQ002-CHRISTOFF-2016", "SRC-BQ002-SMALLWOOD-SCHOOLER-2015"}, {"SRC-BQ002-SELI-2018"}),
    "CLAIM-BQ002-ATLAS-GROUNDED-01": ("Interpretation", "INTERPRETATION", "language_action_and_embodied_cognition", {"SRC-BQ002-BARSALOU-2008"}, set()),
    "CLAIM-BQ002-ATLAS-PREDICTIVE-01": ("Hypothesis", "HYPOTHESIS", "perception_memory_and_learning", {"SRC-BQ002-FRISTON-KIEBEL-2009"}, {"SRC-BQ002-BRUINEBERG-2018"}),
    "CLAIM-BQ002-ATLAS-PHENOMENAL-01": ("Interpretation", "INTERPRETATION", "phenomenology_and_unresolved_origins", {"SRC-BQ002-CHRISTOFF-2016", "SRC-BQ002-BARSALOU-2008", "SRC-BQ002-FRISTON-KIEBEL-2009"}, {"SRC-BQ002-BRUINEBERG-2018"}),
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
    if spec.get("id") != "BQ002" or spec.get("status") != "UNRESOLVED":
        fail("canonical BQ002 spec must remain UNRESOLVED")
    if spec.get("public_beta_gate") is not False:
        fail("canonical BQ002 public beta gate must remain closed")
    graph = spec.get("graph", {})
    if graph.get("truth_inference_allowed") is not False or graph.get("edge_state_may_upgrade_evidence") is not False:
        fail("canonical graph truth and evidence-upgrade boundaries weakened")
    promotion_guards = spec.get("promotion_guards", {})
    if promotion_guards.get("rights_promotion_allowed") is not False or promotion_guards.get("scientific_truth_inference_allowed") is not False:
        fail("canonical rights or scientific truth-inference boundary weakened")
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
        if not source.get("title") or not source.get("provenance"):
            fail("source provenance incomplete")
        expected_doi, expected_pmid, expected_url = EXPECTED_SOURCE_IDENTITIES[source["source_id"]]
        if (source.get("doi"), source.get("pmid"), source.get("url")) != (expected_doi, expected_pmid, expected_url):
            fail(f"source identity changed: {source['source_id']}")
        if not source.get("limitations"):
            fail("every source requires limitations")

    allowed_labels = set(spec.get("canonical_evidence_labels", []))
    claims = atlas.get("claims", [])
    claim_map = {item.get("claim_id"): item for item in claims}
    if set(claim_map) != set(EXPECTED_CLAIMS) or len(claim_map) != len(claims):
        fail("claim set changed or duplicated")
    used_sources = set()
    for claim_id, claim in claim_map.items():
        expected_label, expected_type, expected_domain, expected_source_ids, expected_counter_ids = EXPECTED_CLAIMS[claim_id]
        label = claim.get("evidence_label")
        if label != expected_label or label not in allowed_labels:
            fail("claim evidence label changed")
        if claim.get("claim_type") != expected_type:
            fail("claim type changed")
        if claim.get("domain") != expected_domain:
            fail("claim domain changed")
        source_ids = claim.get("source_ids", [])
        counter_ids = claim.get("counter_source_ids", [])
        if set(source_ids) != expected_source_ids or set(counter_ids) != expected_counter_ids:
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
        if any(claim_map[claim_id].get("domain") != item.get("domain") for claim_id in ids):
            fail("coverage domain does not match its bound claims")

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
