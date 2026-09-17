import copy
import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts/validate_bq001_level7_prediction_registry.py"
spec = importlib.util.spec_from_file_location("bq001_level7_validator", VALIDATOR)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class BQ001Level7PredictionRegistryTests(unittest.TestCase):
    def setUp(self):
        self.registry = json.loads(module.REGISTRY.read_text(encoding="utf-8"))
        self.spec = json.loads(module.SPEC.read_text(encoding="utf-8"))
        self.batch1 = json.loads(module.BATCH1.read_text(encoding="utf-8"))
        self.batch3 = json.loads(module.BATCH3.read_text(encoding="utf-8"))

    def validate(self, registry=None):
        module.validate(registry or self.registry, self.spec, self.batch1, self.batch3)

    def test_candidate_passes(self):
        self.validate()

    def test_level_cannot_be_applied_before_review(self):
        candidate = copy.deepcopy(self.registry)
        candidate["maturity"]["candidate_level_applied"] = True
        with self.assertRaises(ValueError):
            self.validate(candidate)

    def test_candidate_level_name_mutation_rejected(self):
        candidate = copy.deepcopy(self.registry)
        candidate["maturity"]["candidate_level_name"] = "TRUTH_CONFIRMED"
        with self.assertRaises(ValueError):
            self.validate(candidate)

    def test_maturity_disclaimer_reversal_rejected(self):
        candidate = copy.deepcopy(self.registry)
        candidate["maturity"]["meaning"] = "Research-method maturity is evidence strength; model support and promotion are granted."
        with self.assertRaises(ValueError):
            self.validate(candidate)

    def test_canonical_input_mutation_rejected(self):
        candidate = copy.deepcopy(self.registry)
        candidate["source_scope"]["canonical_inputs"][0] = "references/big-questions/BQ001/missing.json"
        with self.assertRaises(ValueError):
            self.validate(candidate)

    def test_question_resolution_rejected(self):
        candidate = copy.deepcopy(self.registry)
        candidate["question_status"] = "RESOLVED"
        with self.assertRaises(ValueError):
            self.validate(candidate)

    def test_model_support_rejected(self):
        candidate = copy.deepcopy(self.registry)
        candidate["models"][0]["supports_models"] = ["MODEL-BQ001-BIOLOGICAL-DEPENDENCE"]
        with self.assertRaises(ValueError):
            self.validate(candidate)

    def test_neutral_outcome_removal_rejected(self):
        candidate = copy.deepcopy(self.registry)
        del candidate["discriminating_tests"][0]["outcome_rules"]["neutral_or_ambiguous"]
        with self.assertRaises(ValueError):
            self.validate(candidate)

    def test_empty_prediction_fields_rejected(self):
        for key in ("prediction_id", "statement", "boundary"):
            with self.subTest(key=key):
                candidate = copy.deepcopy(self.registry)
                candidate["models"][0]["predictions"][0][key] = ""
                with self.assertRaises(ValueError):
                    self.validate(candidate)

    def test_duplicate_prediction_and_challenge_ids_rejected(self):
        for collection, key in (("predictions", "prediction_id"), ("potential_disconfirming_observations", "observation_id")):
            with self.subTest(collection=collection):
                candidate = copy.deepcopy(self.registry)
                records = candidate["models"][0][collection]
                records[1][key] = records[0][key]
                with self.assertRaises(ValueError):
                    self.validate(candidate)

    def test_cross_model_record_id_duplicates_rejected(self):
        mutations = (
            ("predictions", "prediction_id"),
            ("potential_disconfirming_observations", "observation_id"),
        )
        for collection, key in mutations:
            with self.subTest(collection=collection):
                candidate = copy.deepcopy(self.registry)
                candidate["models"][1][collection][0][key] = candidate["models"][0][collection][0][key]
                with self.assertRaises(ValueError):
                    self.validate(candidate)

    def test_empty_challenge_statement_rejected(self):
        candidate = copy.deepcopy(self.registry)
        candidate["models"][0]["potential_disconfirming_observations"][0]["statement"] = None
        with self.assertRaises(ValueError):
            self.validate(candidate)

    def test_empty_outcome_rule_rejected(self):
        candidate = copy.deepcopy(self.registry)
        candidate["discriminating_tests"][0]["outcome_rules"]["neutral_or_ambiguous"] = ""
        with self.assertRaises(ValueError):
            self.validate(candidate)

    def test_empty_test_domain_and_design_rejected(self):
        for key, value in (("domain", ""), ("design", None)):
            with self.subTest(key=key):
                candidate = copy.deepcopy(self.registry)
                candidate["discriminating_tests"][0][key] = value
                with self.assertRaises(ValueError):
                    self.validate(candidate)

    def test_child_safeguard_relaxation_rejected(self):
        candidate = copy.deepcopy(self.registry)
        test = next(item for item in candidate["discriminating_tests"] if item["test_id"] == "TEST-BQ001-PASTLIFE-PROSPECTIVE")
        test["safeguards"]["public_identification_forbidden"] = False
        with self.assertRaises(ValueError):
            self.validate(candidate)

    def test_child_safeguard_omission_rejected(self):
        candidate = copy.deepcopy(self.registry)
        test = next(item for item in candidate["discriminating_tests"] if item["test_id"] == "TEST-BQ001-PASTLIFE-PROSPECTIVE")
        del test["safeguards"]["public_identification_forbidden"]
        with self.assertRaises(ValueError):
            self.validate(candidate)

    def test_missing_null_results_rejected(self):
        candidate = copy.deepcopy(self.registry)
        candidate["method_rules"]["null_results_retained"] = False
        with self.assertRaises(ValueError):
            self.validate(candidate)

    def test_promotion_and_boundary_mutations_rejected(self):
        paths = [
            ("accepted_canonical_edges", 1),
            ("supports_models", ["MODEL-BQ001-CONTINUITY"]),
            ("canonical_promotion_applied", True),
            ("evidence_promotion_applied", True),
            ("public_synthesis_updated", True),
            ("website_updated", True),
            ("truth_inference_allowed", True),
            ("rights_promotion_allowed", True),
            ("privacy_posture_changed", True),
            ("cultural_safeguarding_relaxed", True),
        ]
        for key, value in paths:
            with self.subTest(key=key):
                candidate = copy.deepcopy(self.registry)
                candidate["governance"][key] = value
                with self.assertRaises(ValueError):
                    self.validate(candidate)


if __name__ == "__main__":
    unittest.main()
