import copy
import json
import shutil
import sys
import tempfile
import types
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import validate_bq001_batch6_review as review
import validate_bq001_public_synthesis_v01 as synthesis
import build_public_safe_semantic_endpoint_registry_v019 as exporter


class Batch6ReviewTests(unittest.TestCase):
    def setUp(self):
        self.data = review.load(ROOT / review.BATCH)
        self.spec = review.load(ROOT / "references/big-questions/BQ001/spec-v0.1.json")

    def test_current_review_boundary(self):
        review.validate_repository(ROOT)
        synthesis.validate(review.load(ROOT / "references/big-questions/BQ001/public-synthesis-v0.1.json"), ROOT)

    def test_domain_drift_rejected_for_every_claim(self):
        for i in range(len(self.data["claims"])):
            for domain in ("reincarnation_case_literature", "dream_memory_consolidation", "reincarnation_methods", "unknown"):
                with self.subTest(claim=i, domain=domain):
                    data = copy.deepcopy(self.data)
                    data["claims"][i]["domain"] = domain
                    with self.assertRaisesRegex(ValueError, "domain drift"):
                        review.validate(data, self.spec)

    def test_unapproved_status_changes_rejected(self):
        for status in ("CANONICAL_REVIEW", "CANONICAL_APPROVED", None):
            with self.subTest(status=status):
                data = copy.deepcopy(self.data)
                data["status"] = status
                with self.assertRaisesRegex(ValueError, "REVIEW_CANDIDATE"):
                    review.validate(data, self.spec)

    def test_all_promotion_guards_fail_closed(self):
        for guard in review.REQUIRED_FALSE_GUARDS:
            for value in (True, None):
                with self.subTest(guard=guard, value=value):
                    data = copy.deepcopy(self.data)
                    data["promotion_guards"][guard] = value
                    with self.assertRaisesRegex(ValueError, "guard"):
                        review.validate(data, self.spec)

    def test_model_support_rejected(self):
        self.data["claims"][0]["supports_models"] = ["MODEL-BQ001-CONTINUITY"]
        with self.assertRaisesRegex(ValueError, "supports_models"):
            review.validate(self.data, self.spec)

    def test_untraceable_claim_rejected(self):
        for ids in ([], ["missing"]):
            self.data["claims"][0]["source_ids"] = ids
            with self.assertRaisesRegex(ValueError, "source_ids"):
                review.validate(self.data, self.spec)

    def test_synthesis_rejects_batch_claim_and_source_reintroduction(self):
        for field, value in (("source_batches", review.BATCH), ("source_batches", review.OLD_BATCH),
                             ("claim_ids", self.data["claims"][0]["claim_id"]),
                             ("source_ids", self.data["sources"][0]["source_id"])):
            with self.subTest(field=field, value=value):
                data = review.load(ROOT / "references/big-questions/BQ001/public-synthesis-v0.1.json")
                target = data if field == "source_batches" else data["sections"][0]
                target[field].append(value)
                with self.assertRaises(ValueError):
                    synthesis.validate(data, ROOT)

    def test_real_export_loader_excludes_batch6_sources_and_artifact(self):
        # Use the real BQ records and loader; stub only unrelated census inputs.
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            shutil.copytree(ROOT / "references/big-questions", root / "references/big-questions")
            community = root / "references/community"
            community.mkdir()
            (community / "n2n-test-batch-25.csv").write_text("toolkit_framework\n")
            (community / "knowledge-graph-seed-v0.1.md").write_text(
                "\n".join(f"| PUB-{i} | Publication {i} | public | fixture |" for i in range(13)))
            (root / "scripts").mkdir()
            (root / "scripts/topic_census_v075.py").write_text("# unrelated census fixture\n")
            census = types.SimpleNamespace(load_ontology=lambda: [f"topic {i}" for i in range(68)],
                                           load_wikispine=lambda: [], load_n2n_categories=lambda: [], norm=str)
            with patch.dict(sys.modules, {"topic_census_v075": census}), patch.object(exporter, "ROOT", root), patch.object(exporter, "COMMUNITY", community):
                registry = exporter.build_registry(*exporter.load_real_inputs())
            self.assertEqual(exporter.validate_registry(registry), [])
            records = {e["provenance"]["record_id"] for e in registry["endpoints"]}
            self.assertTrue(records.isdisjoint(s["source_id"] for s in self.data["sources"]))
            self.assertIn("SRC-BQ001-AWARE-2014", records)
            self.assertNotIn(review.BATCH, {a["repository_record"] for a in registry["source_artifacts"]})
            self.assertEqual(registry["edges"], [])
            self.assertEqual(registry["summary"]["accepted_edges"], 0)


if __name__ == "__main__":
    unittest.main()
