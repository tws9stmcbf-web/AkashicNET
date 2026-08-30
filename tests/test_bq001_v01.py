import copy
import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = ROOT / "scripts" / "validate_bq001_v01.py"
SPEC_PATH = ROOT / "references" / "big-questions" / "BQ001" / "spec-v0.1.json"

spec = importlib.util.spec_from_file_location("validate_bq001_v01", VALIDATOR_PATH)
module = importlib.util.module_from_spec(spec)
assert spec.loader
spec.loader.exec_module(module)


def payload():
    return json.loads(SPEC_PATH.read_text(encoding="utf-8"))


class BQ001ContractTests(unittest.TestCase):
    def test_seed_passes(self):
        module.validate(payload())

    def test_forced_conclusion_fails_closed(self):
        p = payload()
        p["status"] = "PROVEN_CONTINUITY"
        with self.assertRaises(ValueError):
            module.validate(p)

    def test_single_model_fails(self):
        p = payload()
        p["models"] = p["models"][:1]
        with self.assertRaises(ValueError):
            module.validate(p)

    def test_claim_without_provenance_fails(self):
        p = payload()
        p["claims"][0]["provenance"] = []
        with self.assertRaises(ValueError):
            module.validate(p)

    def test_testimony_cannot_be_universalised(self):
        p = payload()
        c = copy.deepcopy(p["claims"][0])
        c.update({
            "claim_id": "CLAIM-BQ001-TESTIMONY-NEGATIVE",
            "text": "A reported experience proves a universal survival claim.",
            "evidence_label": "Lived Experience/Testimony",
            "reviewed_support": False,
            "universalised": True,
        })
        p["claims"].append(c)
        with self.assertRaises(ValueError):
            module.validate(p)

    def test_placeholder_cannot_support_established_evidence(self):
        p = payload()
        p["claims"][0]["source_ids"] = ["SRC-BQ001-SEED-001"]
        with self.assertRaises(ValueError):
            module.validate(p)

    def test_graph_truth_inference_fails(self):
        p = payload()
        p["graph"]["truth_inference_allowed"] = True
        with self.assertRaises(ValueError):
            module.validate(p)


if __name__ == "__main__":
    unittest.main()
