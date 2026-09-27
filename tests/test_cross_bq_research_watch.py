import copy
import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "references/big-questions/cross-bq-research-watch-2026-09-16.json"
VALIDATOR = ROOT / "scripts/validate_cross_bq_research_watch.py"

spec = importlib.util.spec_from_file_location("cross_bq_watch_validator", VALIDATOR)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

class CrossBQResearchWatchTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads(ARTIFACT.read_text(encoding="utf-8"))

    def test_candidate_passes(self):
        module.validate(self.data)

    def assert_rejected(self, mutate):
        candidate = copy.deepcopy(self.data)
        mutate(candidate)
        with self.assertRaises(ValueError):
            module.validate(candidate)

    def test_status_promotion_rejected(self):
        self.assert_rejected(lambda d: d.__setitem__("status", "ACCEPTED"))

    def test_bq_resolution_rejected(self):
        self.assert_rejected(lambda d: d["question_status"].__setitem__("BQ001", "RESOLVED"))

    def test_model_support_promotion_rejected(self):
        self.assert_rejected(lambda d: d["claims"][0]["supports_models"].append("MODEL-PSI"))

    def test_public_integration_rejected(self):
        self.assert_rejected(lambda d: d["rights"].__setitem__("public_integration_allowed", True))

    def test_truth_inference_rejected(self):
        self.assert_rejected(lambda d: d["adjudication"].__setitem__("truth_inference_allowed", True))

    def test_planned_bq_mapping_rejected(self):
        self.assert_rejected(lambda d: d["claims"][0]["candidate_bq_links"].append("BQ009"))

    def test_missing_limitation_rejected(self):
        self.assert_rejected(lambda d: d["sources"][0].__setitem__("limitations", []))

    def test_missing_link_check_timestamp_rejected(self):
        self.assert_rejected(lambda d: d["sources"][0]["link_check"].pop("checked_at"))

    def test_invalid_link_check_timestamp_rejected(self):
        self.assert_rejected(
            lambda d: d["sources"][0]["link_check"].__setitem__("checked_at", "2026-02-30")
        )

    def test_claim_mapping_outside_bound_source_scope_rejected(self):
        def remap_claim(d):
            claim = next(
                claim for claim in d["claims"]
                if claim["source_ids"] == ["SRC-CROSSBQ-KOVAROVA-ECPR-NDE-2025"]
            )
            claim["candidate_bq_links"] = ["BQ002"]
        self.assert_rejected(remap_claim)

    def test_overclaim_rejected(self):
        self.assert_rejected(lambda d: d["claims"][0].__setitem__("text", "This proves psi."))

    def test_empty_source_binding_rejected(self):
        self.assert_rejected(lambda d: d["claims"][0].__setitem__("source_ids", []))

    def test_duplicate_source_binding_rejected(self):
        self.assert_rejected(lambda d: d["claims"][1].__setitem__("source_ids", d["claims"][0]["source_ids"][:]))

    def test_empty_bq_mapping_rejected(self):
        self.assert_rejected(lambda d: d["claims"][0].__setitem__("candidate_bq_links", []))

    def test_mediumship_case_hold_removal_rejected(self):
        self.assert_rejected(
            lambda d: next(
                source for source in d["sources"]
                if source["source_id"] == "SRC-CROSSBQ-CHARMAN-MEDIUMSHIP-2026"
            ).__setitem__("review_disposition", "REVIEW_CANDIDATE")
        )

    def test_mediumship_case_evidence_promotion_rejected(self):
        def promote(d):
            claim = next(
                claim for claim in d["claims"]
                if claim["source_ids"] == ["SRC-CROSSBQ-CHARMAN-MEDIUMSHIP-2026"]
            )
            claim["claim_type"] = "OBSERVATION"
            claim["evidence_label"] = "Established Evidence"
        self.assert_rejected(promote)

    def test_iands_academic_reclassification_rejected(self):
        self.assert_rejected(
            lambda d: next(
                institution for institution in d["research_institution_watch"]
                if institution["institution_id"] == "ORG-IANDS"
            ).__setitem__("role", "ACADEMIC_RESEARCH_GROUP")
        )

    def test_institute_evidence_boundary_required(self):
        self.assert_rejected(
            lambda d: d["research_institution_watch"][0].__setitem__("evidence_boundary", "")
        )

if __name__ == "__main__":
    unittest.main()
