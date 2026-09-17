import copy
import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts/validate_bq002_level5_evidence_atlas.py"
spec = importlib.util.spec_from_file_location("bq002_level5_validator", VALIDATOR)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class BQ002Level5EvidenceAtlasTests(unittest.TestCase):
    def setUp(self):
        self.atlas = json.loads(module.ATLAS.read_text(encoding="utf-8"))
        self.spec = json.loads(module.SPEC.read_text(encoding="utf-8"))

    def validate(self, atlas=None, spec=None):
        module.validate(self.atlas if atlas is None else atlas, self.spec if spec is None else spec)

    def test_canonical_support_edge_rejected(self):
        candidate = copy.deepcopy(self.spec)
        candidate["claims"][0]["supports_models"] = ["MODEL-BQ002-COGNITIVE-GENERATION"]
        with self.assertRaises(ValueError):
            self.validate(spec=candidate)

    def test_corrigendum_mutations_rejected(self):
        for field in (None, "doi", "pmid", "type"):
            with self.subTest(field=field):
                candidate = copy.deepcopy(self.atlas)
                source = next(s for s in candidate["sources"] if s["source_id"] == "SRC-BQ002-FOX-2015")
                if field is None:
                    del source["related_notice"]
                else:
                    source["related_notice"][field] = "unrelated"
                with self.assertRaises(ValueError):
                    self.validate(candidate)

    def test_claim_qualification_promotion_rejected(self):
        for key, value in (("limitations", ["This proves all thoughts arise transpersonally."]), ("unresolved_gap", "The complete origin is resolved.")):
            with self.subTest(key=key):
                candidate = copy.deepcopy(self.atlas)
                candidate["claims"][0][key] = value
                with self.assertRaises(ValueError):
                    self.validate(candidate)

    def test_canonical_edges_rejected(self):
        for field in ("source_ids", "contradicts"):
            with self.subTest(field=field):
                candidate = copy.deepcopy(self.spec)
                candidate["claims"][0][field] = ["SRC-BQ002-SEED-001"]
                with self.assertRaises(ValueError):
                    self.validate(spec=candidate)

    def test_canonical_model_promotion_rejected(self):
        candidate = copy.deepcopy(self.spec)
        candidate["models"][0]["status"] = "ESTABLISHED"
        with self.assertRaises(ValueError):
            self.validate(spec=candidate)

    def test_source_limitations_promotion_rejected(self):
        candidate = copy.deepcopy(self.atlas)
        candidate["sources"][0]["limitations"] = ["This proves all thought is transpersonal."]
        with self.assertRaises(ValueError):
            self.validate(candidate)

    def test_canonical_semantic_promotion_rejected(self):
        for change in ("claim_text", "extra_claim", "policy", "model_name", "model_position"):
            with self.subTest(change=change):
                candidate = copy.deepcopy(self.spec)
                if change == "claim_text":
                    candidate["claims"][0]["text"] = "The origin of thought is resolved."
                elif change == "extra_claim":
                    candidate["claims"].append(copy.deepcopy(candidate["claims"][0]))
                elif change == "policy":
                    candidate["conclusion_policy"] = "DETERMINED_AT_INGESTION"
                elif change == "model_name":
                    candidate["models"][0]["name"] = "established_answer"
                else:
                    candidate["models"][0]["position"] = "This proves the origin of all thought."
                with self.assertRaises(ValueError):
                    self.validate(spec=candidate)

    def test_candidate_passes(self):
        self.validate()

    def test_level_cannot_be_applied_before_review(self):
        candidate = copy.deepcopy(self.atlas)
        candidate["maturity"]["candidate_level_applied"] = True
        with self.assertRaises(ValueError):
            self.validate(candidate)

    def test_source_count_cannot_advance_level(self):
        candidate = copy.deepcopy(self.atlas)
        candidate["scope"]["source_count_advances_level"] = True
        with self.assertRaises(ValueError):
            self.validate(candidate)

    def test_established_label_cannot_be_applied_to_hypothesis(self):
        candidate = copy.deepcopy(self.atlas)
        claim = next(x for x in candidate["claims"] if x["claim_id"] == "CLAIM-BQ002-ATLAS-PREDICTIVE-01")
        claim["evidence_label"] = "Established Evidence"
        with self.assertRaises(ValueError):
            self.validate(candidate)

    def test_counter_source_removal_rejected(self):
        candidate = copy.deepcopy(self.atlas)
        for claim in candidate["claims"]:
            claim["counter_source_ids"] = [x for x in claim["counter_source_ids"] if x != "SRC-BQ002-BRUINEBERG-2018"]
        with self.assertRaises(ValueError):
            self.validate(candidate)

    def test_counter_source_moved_to_support_rejected(self):
        candidate = copy.deepcopy(self.atlas)
        claim = next(x for x in candidate["claims"] if x["claim_id"] == "CLAIM-BQ002-ATLAS-PREDICTIVE-01")
        claim["source_ids"].append("SRC-BQ002-BRUINEBERG-2018")
        claim["counter_source_ids"].remove("SRC-BQ002-BRUINEBERG-2018")
        with self.assertRaises(ValueError):
            self.validate(candidate)

    def test_source_identity_and_provenance_mutations_rejected(self):
        for key, value in (("doi", "10.0000/unrelated"), ("pmid", "0"), ("url", "https://example.invalid/"), ("provenance", "")):
            with self.subTest(key=key):
                candidate = copy.deepcopy(self.atlas)
                candidate["sources"][0][key] = value
                with self.assertRaises(ValueError):
                    self.validate(candidate)

    def test_source_bibliographic_metadata_swap_rejected(self):
        candidate = copy.deepcopy(self.atlas)
        first, second = candidate["sources"][0], candidate["sources"][1]
        first["provenance"], second["provenance"] = second["provenance"], first["provenance"]
        with self.assertRaises(ValueError):
            self.validate(candidate)

    def test_bounded_claim_text_mutation_rejected(self):
        candidate = copy.deepcopy(self.atlas)
        candidate["claims"][0]["text"] = "This source proves a complete transpersonal origin theory."
        with self.assertRaises(ValueError):
            self.validate(candidate)

    def test_claim_type_mutation_rejected(self):
        candidate = copy.deepcopy(self.atlas)
        candidate["claims"][0]["claim_type"] = "HYPOTHESIS"
        with self.assertRaises(ValueError):
            self.validate(candidate)

    def test_model_support_rejected(self):
        candidate = copy.deepcopy(self.atlas)
        candidate["claims"][0]["supports_models"] = ["MODEL-BQ002-COGNITIVE-GENERATION"]
        with self.assertRaises(ValueError):
            self.validate(candidate)

    def test_domain_omission_rejected(self):
        candidate = copy.deepcopy(self.atlas)
        candidate["coverage"].pop()
        with self.assertRaises(ValueError):
            self.validate(candidate)

    def test_coverage_claim_domain_mismatch_rejected(self):
        candidate = copy.deepcopy(self.atlas)
        candidate["coverage"][0]["claim_ids"] = ["CLAIM-BQ002-ATLAS-DREAM-MEMORY-01"]
        with self.assertRaises(ValueError):
            self.validate(candidate)

    def test_canonical_spec_boundary_mutations_rejected(self):
        mutations = [
            (("status",), "RESOLVED"),
            (("public_beta_gate",), True),
            (("graph", "truth_inference_allowed"), True),
            (("graph", "edge_state_may_upgrade_evidence"), True),
            (("promotion_guards", "rights_promotion_allowed"), True),
            (("promotion_guards", "scientific_truth_inference_allowed"), True),
        ]
        for path, value in mutations:
            with self.subTest(path=path):
                candidate_spec = copy.deepcopy(self.spec)
                target = candidate_spec
                for key in path[:-1]:
                    target = target[key]
                target[path[-1]] = value
                with self.assertRaises(ValueError):
                    self.validate(spec=candidate_spec)

    def test_every_canonical_no_promotion_guard_is_required(self):
        for key in module.REQUIRED_TRUE_PROMOTION_GUARDS:
            with self.subTest(key=key):
                candidate_spec = copy.deepcopy(self.spec)
                candidate_spec["promotion_guards"][key] = False
                with self.assertRaises(ValueError):
                    self.validate(spec=candidate_spec)

    def test_promotion_and_boundary_mutations_rejected(self):
        paths = [
            ("question_status", "RESOLVED"),
            ("public_beta_gate", True),
            ("accepted_canonical_edges", 1),
            ("supports_models", ["MODEL-BQ002-COGNITIVE-GENERATION"]),
            ("canonical_promotion_applied", True),
            ("evidence_promotion_applied", True),
            ("public_synthesis_updated", True),
            ("website_updated", True),
            ("truth_inference_allowed", True),
            ("transpersonal_claim_promoted", True),
            ("rights_promotion_allowed", True),
        ]
        for key, value in paths:
            with self.subTest(key=key):
                candidate = copy.deepcopy(self.atlas)
                candidate["governance"][key] = value
                with self.assertRaises(ValueError):
                    self.validate(candidate)


if __name__ == "__main__":
    unittest.main()
