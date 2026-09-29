"""Fail-closed regressions for the public topic discovery contract."""
import copy
import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = json.loads((ROOT / "schemas/global_topic_v01.schema.json").read_text())
SEED = json.loads((ROOT / "data/global_metadata_discovery_v01.seed.json").read_text())
VALIDATOR = Draft202012Validator(SCHEMA, format_checker=FormatChecker())


class TopicContractTests(unittest.TestCase):
    def test_seed_and_controlled_vocabulary(self):
        self.assertEqual(SEED["controlled_values"]["ultimate_status"],
                         SCHEMA["properties"]["origin"]["properties"]["ultimate_status"]["enum"])
        for topic in SEED["topics"]:
            self.assertFalse(list(VALIDATOR.iter_errors(topic)), topic["slug"])

    def test_schema_valid_records_have_page_consumed_fields(self):
        record = copy.deepcopy(SEED["topics"][1])
        for key in ("summary", "entities", "open_questions", "review"):
            altered = copy.deepcopy(record)
            del altered[key]
            self.assertFalse(VALIDATOR.is_valid(altered), key)
        for container, key in (("origin", "evidence_note"), ("rights", "note")):
            altered = copy.deepcopy(record)
            del altered[container][key]
            self.assertFalse(VALIDATOR.is_valid(altered), key)

    def test_reviewed_and_public_are_not_self_promoting(self):
        record = copy.deepcopy(SEED["topics"][1])
        for status in ("reviewed", "public"):
            altered = copy.deepcopy(record)
            altered["status"] = status
            self.assertFalse(VALIDATOR.is_valid(altered), status)
            altered["review"] = {"human_reviewed": True, "last_reviewed": "2026-09-29", "notes": "Test"}
            altered["sources"] = copy.deepcopy(SEED["topics"][0]["sources"])
            altered["rights"]["mode"] = "link-only"
            self.assertTrue(VALIDATOR.is_valid(altered), status)
            altered["rights"]["mode"] = "unknown"
            self.assertFalse(VALIDATOR.is_valid(altered), status)

    def test_claim_refs_and_ratings(self):
        for topic in SEED["topics"]:
            sources = {source["id"]: source for source in topic["sources"]}
            for claim in topic["connections"] + topic.get("solution_space", {}).get("candidates", []):
                self.assertTrue(set(claim["source_ids"]) <= sources.keys(), topic["slug"])
                if claim.get("evidence_status") in ("supported", "established"):
                    self.assertTrue(any(sources[id]["evidence_role"] in ("claim", "replication")
                                        for id in claim["source_ids"]), claim["label"])
        page = (ROOT / "website/app/topics/[slug]/page.tsx").read_text()
        self.assertIn("ids={connection.source_ids}", page)
        self.assertIn("ids={candidate.source_ids}", page)


if __name__ == "__main__":
    unittest.main()
