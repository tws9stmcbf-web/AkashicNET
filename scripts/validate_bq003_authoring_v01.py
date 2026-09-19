#!/usr/bin/env python3
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = ROOT / "references/big-questions/BQ003/spec-v0.1.json"
ASSESSMENT = ROOT / "references/big-questions/BQ003/progress-assessment-v0.1.json"
BRIDGE = ROOT / "references/big-questions/BQ003/bq001-meta-awareness-bridge-v0.1.json"
AGHOR = ROOT / "references/big-questions/BQ003/aghori-research-candidates-v0.1.json"
ARCH = ROOT / "references/big-questions/architecture-v0.1.json"

EXPECTED_MODELS = {
    "MODEL-BQ003-BRAIN-GENERATED",
    "MODEL-BQ003-PSYCHOLOGICAL-SYMBOLIC",
    "MODEL-BQ003-RELATIONAL-EMERGENCE",
    "MODEL-BQ003-RECEIVER-FILTER",
    "MODEL-BQ003-FUNDAMENTAL-CONSCIOUSNESS",
    "MODEL-BQ003-LOVE-FIELD",
}
EXPECTED_CONTINUITY_TYPES = {
    "PERSONAL_IDENTITY_CONTINUITY",
    "META_AWARENESS_CONTINUITY",
    "INFORMATION_CONTINUITY",
    "RELATIONAL_OR_ANIMISTIC_CONTINUITY",
}
EXPECTED_BRIDGE_MODELS = {
    "BRIDGE-MODEL-BIOLOGICAL-DEPENDENCE",
    "BRIDGE-MODEL-RECEIVER-FILTER",
    "BRIDGE-MODEL-PANPSYCHIC",
    "BRIDGE-MODEL-RELATIONAL-ANIMISTIC",
}
EXPECTED_CULTURAL_GOVERNANCE = {
    "indigenous_relational_cosmologies_are_not_generic_evidence",
    "community_authority_permission_and_care_required",
    "restricted_knowledge_must_remain_restricted",
    "perceived_beings_must_not_be_authenticated_by_default",
    "traditions_must_not_be_collapsed_into_one_cosmology",
}
FALSE_GUARDS = {
    "truth_inference_allowed",
    "scientific_evidence_promotion_allowed",
    "rights_promotion_allowed",
}
ASSESSMENT_FALSE_GUARDS = FALSE_GUARDS | {
    "canonical_promotion_applied",
    "public_synthesis_updated",
    "website_updated",
    "model_edges_upgrade_evidence",
}

AGHOR_FALSE_GUARDS = FALSE_GUARDS | {
    "canonical_promotion_applied",
    "public_synthesis_updated",
    "website_updated",
}
EXPECTED_AGHOR_CLAIMS = {
    "CLAIM-BQ003-AGHOR-ETHNOGRAPHY-01": (
        "SRC-BQ003-BARRETT-AGHOR-MEDICINE-2008", "OBSERVATION", "Established Evidence"),
    "CLAIM-BQ003-AGHOR-LINEAGE-01": (
        "SRC-BQ003-SHANKAR-AGHOR-2011", "INTERPRETATION", "Interpretation"),
    "CLAIM-BQ003-KINA-RAMI-HISTORY-01": (
        "SRC-BQ003-GUPTA-KINA-RAMI-1993", "INTERPRETATION", "Interpretation"),
    "CLAIM-BQ003-DEATH-TEACHER-01": (
        "SRC-BQ003-SURI-PITCHFORD-DEATH-2010", "INTERPRETATION", "Interpretation"),
}

def fail(message):
    raise ValueError(message)

def validate(spec, assessment, bridge, aghor, architecture):
    if spec.get("id") != "BQ003" or spec.get("status") != "UNRESOLVED":
        fail("BQ003 identity/status changed")
    if spec.get("authoring_status") != "REVIEW_CANDIDATE" or spec.get("public_beta_gate") is not False:
        fail("BQ003 must remain a gated review candidate")
    boundary = spec.get("hypothesis_boundary", {})
    if "already exist" not in boundary.get("proposed_hypothesis", ""):
        fail("pre-existing field hypothesis lost")
    if "creates" not in boundary.get("excluded_claim", ""):
        fail("field-creation exclusion lost")
    if boundary.get("ontology_status") != "UNCONFIRMED" or boundary.get("access_status") != "UNCONFIRMED":
        fail("field ontology/access must remain unconfirmed")
    model_items = spec.get("models", [])
    models = {item.get("model_id") for item in model_items}
    if models != EXPECTED_MODELS or len(model_items) != len(EXPECTED_MODELS):
        fail("competing model set changed")
    if any(item.get("status") != "UNRESOLVED" for item in model_items):
        fail("competing models must remain unresolved")
    for claim in spec.get("claims", []):
        if claim.get("supports_models") != []:
            fail("BQ003 model support promotion")
    guards = spec.get("promotion_guards", {})
    if guards.get("rights_promotion_allowed") is not False or guards.get("scientific_truth_inference_allowed") is not False:
        fail("BQ003 promotion guards weakened")
    for key in ("truth_inference_allowed", "edge_state_may_upgrade_evidence"):
        if spec.get("graph", {}).get(key) is not False:
            fail(f"BQ003 graph guard weakened: {key}")
    lenses = spec.get("culturally_situated_interpretive_lenses", [])
    if len(lenses) != 1 or lenses[0].get("lens_id") != "LENS-BQ003-AGHOR-NONDUAL-SHAIVA":
        fail("bounded Aghor interpretive lens required")
    lens = lenses[0]
    if lens.get("evidence_label") != "Interpretation" or lens.get("status") != "REVIEW_CANDIDATE":
        fail("Aghor lens must remain a review-candidate Interpretation")
    if lens.get("supports_models") != []:
        fail("Aghor lens supports_models must remain empty")
    attribution = lens.get("attribution_boundary", "").lower()
    if "do not state that all aghoris teach" not in attribution or "akashicnet comparative interpretation" not in attribution:
        fail("Aghor attribution boundary missing")
    scientific = lens.get("scientific_boundary", "").lower()
    if "not scientific confirmation" not in scientific:
        fail("Aghor scientific boundary missing")
    if len(lens.get("sources", [])) < 2:
        fail("Aghor lens requires lineage and scholarly context")

    cultural = spec.get("cultural_governance")
    if not isinstance(cultural, dict) or set(cultural) != EXPECTED_CULTURAL_GOVERNANCE:
        fail("BQ003 cultural governance requirements changed")
    if any(cultural.get(key) is not True for key in EXPECTED_CULTURAL_GOVERNANCE):
        fail("BQ003 cultural governance must remain fail-closed")

    if assessment.get("status") != "REVIEW_CANDIDATE":
        fail("assessment must remain review candidate")
    progress = assessment.get("overall_progress", {})
    if assessment.get("question_status") != "UNRESOLVED":
        fail("assessment must remain unresolved")
    if assessment.get("ladder_ref") != "references/big-questions/research-maturity-ladder-v0.1.json":
        fail("assessment must reference the canonical maturity ladder")
    if "level_semantics" in assessment:
        fail("assessment must not embed a divergent maturity ladder")
    if progress.get("level") != 4 or progress.get("maximum") != 10:
        fail("overall progress must remain Level 4/10 pending review")
    if progress.get("stage_id") != "MODELS_SEPARATED" or progress.get("completed_stages") != [1, 2, 3, 4]:
        fail("BQ003 completed stages must remain canonical and consecutive")
    meaning = progress.get("meaning", "").lower()
    if "does not estimate truth" not in meaning or "field exists" not in meaning:
        fail("progress-is-not-truth boundary missing")
    axes = assessment.get("axis_assessments", [])
    if not axes:
        fail("axis assessments required")
    for axis in axes:
        if "level" in axis or "label" in axis:
            fail("axis assessments must not embed maturity-ladder fields")
        if not isinstance(axis.get("evidence_state"), str) or not axis["evidence_state"]:
            fail("every axis requires a nonempty evidence_state")
    interpersonal = next((item for item in axes if item.get("axis") == "interpersonal_harmony"), None)
    if not interpersonal or interpersonal.get("evidence_state") != "RELEVANT_EVIDENCE_MAPPED":
        fail("interpersonal harmony evidence-state boundary changed")
    if interpersonal.get("source_ids") != ["SRC-BQ003-MOGAN-SYNCHRONY-2017"]:
        fail("interpersonal synchrony source binding changed")
    source_ids = {item.get("source_id") for item in assessment.get("sources", [])}
    if "SRC-BQ003-MOGAN-SYNCHRONY-2017" not in source_ids:
        fail("corrected Mogan synchrony source required")
    cosmic = next((item for item in axes if item.get("axis") == "literal_cosmic_ontology"), None)
    if not cosmic or cosmic.get("evidence_state") != "QUESTION_FRAMED" or "unconfirmed" not in cosmic.get("boundary", "").lower():
        fail("literal cosmic ontology must remain question-framed and unconfirmed")
    assessment_governance = assessment.get("governance", {})
    for key in ASSESSMENT_FALSE_GUARDS:
        if assessment_governance.get(key) is not False:
            fail(f"assessment guard weakened: {key}")

    if bridge.get("status") != "REVIEW_CANDIDATE":
        fail("bridge must remain review candidate")
    if bridge.get("questions") != ["BQ001", "BQ003"]:
        fail("bridge must bind exactly BQ001 and BQ003")
    if " if consciousness is fundamental or pervasive?" not in bridge.get("bridge_question", "").lower():
        fail("bridge must remain conditional")
    types = {item.get("continuity_type") for item in bridge.get("distinctions", [])}
    if types != EXPECTED_CONTINUITY_TYPES:
        fail("continuity distinctions changed")
    bridge_model_items = bridge.get("candidate_models", [])
    bridge_models = {item.get("model_id") for item in bridge_model_items}
    if bridge_models != EXPECTED_BRIDGE_MODELS or len(bridge_model_items) != len(EXPECTED_BRIDGE_MODELS):
        fail("bridge competing model set changed")
    hypothesis = bridge.get("named_hypothesis", {})
    if hypothesis.get("hypothesis_id") != "HYP-BQ001-META-AWARENESS-REINCARNATION-REIMAGINED":
        fail("named meta-awareness hypothesis missing")
    if hypothesis.get("evidence_label") != "Hypothesis" or hypothesis.get("status") != "UNRESOLVED":
        fail("meta-awareness hypothesis promoted")
    if hypothesis.get("supports_models") != []:
        fail("meta-awareness hypothesis supports_models must remain empty")
    boundary = hypothesis.get("decisive_boundary", "").lower()
    if "causal continuity" not in boundary or "universal re-expression rather than reincarnation" not in boundary:
        fail("reincarnation/re-expression boundary missing")

    bridge_governance = bridge.get("governance", {})
    if bridge_governance.get("bq001_status") != "UNRESOLVED" or bridge_governance.get("bq003_status") != "UNRESOLVED":
        fail("bridge questions must remain unresolved")
    if bridge_governance.get("supports_models") != []:
        fail("bridge supports_models must remain empty")
    for key in FALSE_GUARDS:
        if bridge_governance.get(key) is not False:
            fail(f"bridge guard weakened: {key}")

    expected_aghor_sources = {
        "SRC-BQ003-BARRETT-AGHOR-MEDICINE-2008",
        "SRC-BQ003-SHANKAR-AGHOR-2011",
        "SRC-BQ003-GUPTA-KINA-RAMI-1993",
        "SRC-BQ003-SURI-PITCHFORD-DEATH-2010",
    }
    if aghor.get("status") != "REVIEW_CANDIDATE" or aghor.get("question_id") != "BQ003":
        fail("Aghor batch must remain a BQ003 review candidate")
    sources = aghor.get("sources", [])
    source_map = {item.get("source_id"): item for item in sources}
    if set(source_map) != expected_aghor_sources or len(source_map) != len(sources):
        fail("Aghor candidate source set changed")
    if source_map["SRC-BQ003-GUPTA-KINA-RAMI-1993"].get("review_disposition") != "HOLD_FULL_TEXT_ACCESS_LIMITED":
        fail("Gupta dissertation must remain on access-limited hold")
    claims = aghor.get("bounded_claims", [])
    claimed = []
    for claim in claims:
        if claim.get("supports_models") != []:
            fail("Aghor claims supports_models must remain empty")
        expected = EXPECTED_AGHOR_CLAIMS.get(claim.get("claim_id"))
        if expected is None:
            fail("unexpected Aghor claim identity")
        source_id, claim_type, evidence_label = expected
        source_ids = claim.get("source_ids")
        if (source_ids != [source_id] or claim.get("claim_type") != claim_type
                or claim.get("evidence_label") != evidence_label):
            fail("Aghor claim source/type/evidence binding changed")
        claimed.extend(source_ids)
    if set(claimed) != expected_aghor_sources or len(claimed) != len(set(claimed)):
        fail("Aghor claims must bind each source exactly once")
    if aghor.get("governance", {}).get("question_status") != "UNRESOLVED":
        fail("Aghor question must remain unresolved")
    for key in AGHOR_FALSE_GUARDS:
        if aghor.get("governance", {}).get(key) is not False:
            fail(f"Aghor batch guard weakened: {key}")
    if aghor.get("governance", {}).get("accepted_evidence_batch") is not False:
        fail("Aghor batch must not be accepted canonically")
    if aghor.get("governance", {}).get("full_text_copied") is not False:
        fail("Aghor full text must not be copied")

    if "BQ003" in architecture.get("questions", {}):
        fail("BQ003 must not enter the canonical questions registry without an accepted evidence batch")
    reg = architecture.get("authoring_candidates", {}).get("BQ003", {})
    if reg.get("registration_status") != "REVIEW_CANDIDATE" or reg.get("public_beta_gate") is not False:
        fail("BQ003 authoring-candidate gate changed")
    if reg.get("canonical_registration_applied") is not False:
        fail("BQ003 canonical registration must remain unapplied")
    if reg.get("accepted_evidence_batches") != []:
        fail("BQ003 has no accepted evidence batches yet")

def main():
    try:
        validate(
            json.loads(SPEC.read_text(encoding="utf-8")),
            json.loads(ASSESSMENT.read_text(encoding="utf-8")),
            json.loads(BRIDGE.read_text(encoding="utf-8")),
            json.loads(AGHOR.read_text(encoding="utf-8")),
            json.loads(ARCH.read_text(encoding="utf-8")),
        )
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"BQ003 AUTHORING FAIL: {exc}", file=sys.stderr)
        return 1
    print("BQ003 AUTHORING PASS: Level 3 review candidate; BQ001/BQ003 unresolved; field ontology unconfirmed")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
