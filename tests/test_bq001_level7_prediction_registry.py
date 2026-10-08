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

    def test_cross_kind_id_collision_rejected(self):
        candidate = copy.deepcopy(self.registry)
        candidate["models"][1]["potential_disconfirming_observations"][0]["observation_id"] = candidate["models"][0]["predictions"][0]["prediction_id"]
        with self.assertRaises(ValueError):
            self.validate(candidate)

    def test_missing_operational_scope_rejected(self):
        candidate = copy.deepcopy(self.registry)
        candidate["models"][0]["operational_scope"] = "   "
        with self.assertRaises(ValueError):
            self.validate(candidate)

    def test_duplicate_outcomes_rejected(self):
        candidate = copy.deepcopy(self.registry)
        rules = candidate["discriminating_tests"][0]["outcome_rules"]
        rules["neutral_or_ambiguous"] = rules["continuity_strengthened"].upper() + "  "
        with self.assertRaises(ValueError):
            self.validate(candidate)

    def test_duplicate_statements_rejected(self):
        for collection in ("predictions", "potential_disconfirming_observations"):
            with self.subTest(collection=collection):
                candidate = copy.deepcopy(self.registry)
                records = candidate["models"][0][collection]
                records[1]["statement"] = records[0]["statement"].upper() + "  "
                with self.assertRaises(ValueError):
                    self.validate(candidate)

    def test_cross_kind_normalized_statements_rejected(self):
        for model_index in range(len(self.registry["models"])):
            for normalized in (False, True):
                with self.subTest(model=model_index, normalized=normalized):
                    candidate = copy.deepcopy(self.registry)
                    model = candidate["models"][model_index]
                    statement = model["predictions"][0]["statement"]
                    if normalized:
                        statement = "  " + " \t\n ".join(statement.upper().split()) + "  "
                    model["potential_disconfirming_observations"][0]["statement"] = statement
                    with self.assertRaisesRegex(ValueError, "statements must be distinct"):
                        self.validate(candidate)

    def test_design_context_source_set_mutations_rejected(self):
        original = self.registry["source_scope"]["source_ids_used_for_design_context_only"]
        mutations = {
            "empty": [],
            "duplicate": original + [original[0]],
            "known_addition": original + ["SRC-BQ001-KOCH-2016"],
            "known_substitution": ["SRC-BQ001-KOCH-2016"] + original[1:],
            "unknown_substitution": ["UNKNOWN"] + original[1:],
            "duplicate_substitution": [original[1]] + original[1:],
        }
        for index in range(len(original)):
            mutations[f"missing_{index}"] = original[:index] + original[index + 1:]
        for name, source_ids in mutations.items():
            with self.subTest(mutation=name):
                candidate = copy.deepcopy(self.registry)
                candidate["source_scope"]["source_ids_used_for_design_context_only"] = source_ids
                with self.assertRaisesRegex(ValueError, "design-context source"):
                    self.validate(candidate)

    def test_design_context_source_order_is_irrelevant(self):
        candidate = copy.deepcopy(self.registry)
        candidate["source_scope"]["source_ids_used_for_design_context_only"].reverse()
        self.validate(candidate)

    def test_design_context_sources_must_still_exist_in_canonical_inputs(self):
        self.batch1["sources"] = [
            item for item in self.batch1["sources"]
            if item["source_id"] != "SRC-BQ001-AWARE-2014"
        ]
        with self.assertRaisesRegex(ValueError, "design-context source"):
            self.validate()

    def test_invalid_test_domain_rejected(self):
        candidate = copy.deepcopy(self.registry)
        candidate["discriminating_tests"][0]["domain"] = "not_a_canonical_bq001_domain"
        with self.assertRaises(ValueError):
            self.validate(candidate)

    def test_registry_identity_rejected(self):
        candidate = copy.deepcopy(self.registry)
        candidate["registry_id"] = "OTHER-REGISTRY"
        with self.assertRaises(ValueError):
            self.validate(candidate)

    def test_candidate_passes(self):
        self.validate()

    def test_model_record_swap_rejected(self):
        candidate = copy.deepcopy(self.registry)
        candidate["models"][0]["model_id"], candidate["models"][1]["model_id"] = (
            candidate["models"][1]["model_id"], candidate["models"][0]["model_id"]
        )
        with self.assertRaises(ValueError):
            self.validate(candidate)

    def test_registry_version_mutation_rejected(self):
        candidate = copy.deepcopy(self.registry)
        candidate["version"] = "99.0.0"
        with self.assertRaises(ValueError):
            self.validate(candidate)

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

    def test_canonical_inputs_require_exact_list_cardinality(self):
        original = self.registry["source_scope"]["canonical_inputs"]
        for value in (original + [original[0]], dict.fromkeys(original), None, ""):
            with self.subTest(value=value):
                candidate = copy.deepcopy(self.registry)
                candidate["source_scope"]["canonical_inputs"] = value
                with self.assertRaisesRegex(ValueError, "canonical provenance"):
                    self.validate(candidate)

    def test_canonical_input_order_is_irrelevant(self):
        candidate = copy.deepcopy(self.registry)
        candidate["source_scope"]["canonical_inputs"].reverse()
        self.validate(candidate)

    def test_maturity_levels_require_exact_integer_types(self):
        for key, value in (("current_level", 6.0), ("candidate_level", 7.0)):
            with self.subTest(key=key):
                candidate = copy.deepcopy(self.registry)
                candidate["maturity"][key] = value
                with self.assertRaisesRegex(ValueError, "Level 6 to Level 7"):
                    self.validate(candidate)

    def test_accepted_edge_count_requires_exact_integer_type(self):
        for value in (False, 0.0):
            with self.subTest(value=value):
                candidate = copy.deepcopy(self.registry)
                candidate["governance"]["accepted_canonical_edges"] = value
                with self.assertRaisesRegex(ValueError, "canonical/model edges"):
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
