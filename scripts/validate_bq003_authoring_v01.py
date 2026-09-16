#!/usr/bin/env python3
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = ROOT / "references/big-questions/BQ003/spec-v0.1.json"
ASSESSMENT = ROOT / "references/big-questions/BQ003/progress-assessment-v0.1.json"
BRIDGE = ROOT / "references/big-questions/BQ003/bq001-meta-awareness-bridge-v0.1.json"
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
FALSE_GUARDS = {
    "truth_inference_allowed",
    "scientific_evidence_promotion_allowed",
    "rights_promotion_allowed",
}

def fail(message):
    raise ValueError(message)

def validate(spec, assessment, bridge, architecture):
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
    models = {item.get("model_id") for item in spec.get("models", [])}
    if models != EXPECTED_MODELS:
        fail("competing model set changed")
    for claim in spec.get("claims", []):
        if claim.get("supports_models") != []:
            fail("BQ003 model support promotion")
    guards = spec.get("promotion_guards", {})
    if guards.get("rights_promotion_allowed") is not False or guards.get("scientific_truth_inference_allowed") is not False:
        fail("BQ003 promotion guards weakened")
    cultural = spec.get("cultural_governance", {})
    if not all(cultural.values()):
        fail("BQ003 cultural governance must remain fail-closed")

    progress = assessment.get("overall_progress", {})
    if assessment.get("question_status") != "UNRESOLVED":
        fail("assessment must remain unresolved")
    if progress.get("level") != 3 or progress.get("maximum") != 10:
        fail("overall progress must remain Level 3/10 pending review")
    meaning = progress.get("meaning", "").lower()
    if "does not estimate truth" not in meaning or "field exists" not in meaning:
        fail("progress-is-not-truth boundary missing")
    axes = assessment.get("axis_assessments", [])
    if not axes:
        fail("axis assessments required")
    interpersonal = next((item for item in axes if item.get("axis") == "interpersonal_harmony"), None)
    if not interpersonal or interpersonal.get("level") != 5:
        fail("interpersonal harmony must remain Level 5 until independent replication is verified")
    if interpersonal.get("source_ids") != ["SRC-BQ003-MOGAN-SYNCHRONY-2017"]:
        fail("interpersonal synchrony source binding changed")
    source_ids = {item.get("source_id") for item in assessment.get("sources", [])}
    if "SRC-BQ003-MOGAN-SYNCHRONY-2017" not in source_ids:
        fail("corrected Mogan synchrony source required")
    cosmic = next((item for item in axes if item.get("axis") == "literal_cosmic_ontology"), None)
    if not cosmic or cosmic.get("level") != 1 or "unconfirmed" not in cosmic.get("boundary", "").lower():
        fail("literal cosmic ontology must remain Level 1 and unconfirmed")
    for key in FALSE_GUARDS:
        if assessment.get("governance", {}).get(key) is not False:
            fail(f"assessment guard weakened: {key}")

    if bridge.get("status") != "REVIEW_CANDIDATE":
        fail("bridge must remain review candidate")
    if " if consciousness is fundamental or pervasive?" not in bridge.get("bridge_question", "").lower():
        fail("bridge must remain conditional")
    types = {item.get("continuity_type") for item in bridge.get("distinctions", [])}
    if types != EXPECTED_CONTINUITY_TYPES:
        fail("continuity distinctions changed")
    bridge_governance = bridge.get("governance", {})
    if bridge_governance.get("bq001_status") != "UNRESOLVED" or bridge_governance.get("bq003_status") != "UNRESOLVED":
        fail("bridge questions must remain unresolved")
    if bridge_governance.get("supports_models") != []:
        fail("bridge supports_models must remain empty")
    for key in FALSE_GUARDS:
        if bridge_governance.get(key) is not False:
            fail(f"bridge guard weakened: {key}")

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
            json.loads(ARCH.read_text(encoding="utf-8")),
        )
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"BQ003 AUTHORING FAIL: {exc}", file=sys.stderr)
        return 1
    print("BQ003 AUTHORING PASS: Level 3 review candidate; BQ001/BQ003 unresolved; field ontology unconfirmed")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
