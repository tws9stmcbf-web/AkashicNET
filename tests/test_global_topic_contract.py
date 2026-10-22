"""Fail-closed regressions for the public topic discovery contract."""
import copy
import json
import unittest
from pathlib import Path

from jsonschema import ValidationError
from scripts.validate_global_topic_contract import SCHEMA, VALIDATOR, validate_topic, validate_seed

ROOT = Path(__file__).resolve().parents[1]
SEED = json.loads((ROOT / "data/global_metadata_discovery_v01.seed.json").read_text())


class TopicContractTests(unittest.TestCase):
    def test_seed_and_controlled_vocabulary(self):
        self.assertEqual(SEED["controlled_values"]["ultimate_status"],
                         SCHEMA["properties"]["origin"]["properties"]["ultimate_status"]["enum"])
        for topic in SEED["topics"]:
            self.assertFalse(list(VALIDATOR.iter_errors(topic)), topic["slug"])

    def test_schema_valid_records_have_page_consumed_fields(self):
        record = copy.deepcopy(SEED["topics"][1])
        for key in ("aliases", "summary", "entities", "open_questions", "review"):
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
            altered["public_clearance"] = self.clearance()
            self.assertFalse(VALIDATOR.is_valid(altered), status)
            altered["review"] = {"human_reviewed": True, "last_reviewed": "2026-09-29", "notes": "Test"}
            altered["sources"] = copy.deepcopy(SEED["topics"][0]["sources"])
            altered["rights"]["mode"] = "link-only"
            self.assertTrue(VALIDATOR.is_valid(altered), status)
            altered["rights"]["mode"] = "unknown"
            self.assertFalse(VALIDATOR.is_valid(altered), status)

    @staticmethod
    def clearance():
        return {"decision": "CLEARED", "reviewed_on": "2026-09-30",
                "decision_ref": "test-fixture-only", "privacy_checked": True,
                "rights_checked": True, "cultural_sovereignty_checked": True}

    def reject(self, topic):
        with self.assertRaises((ValidationError, ValueError)):
            validate_topic(topic)

    def test_claim_refs_and_ratings(self):
        validate_seed(SEED)
        page = (ROOT / "website/app/topics/[slug]/page.tsx").read_text()
        self.assertIn("ids={connection.source_ids}", page)
        self.assertIn("ids={candidate.source_ids}", page)

    def test_documented_edge_requires_registered_nonempty_provenance(self):
        for status in ("documented", "taxonomic", "co-occurrence"):
            for refs in ([], ["NOT-REGISTERED"], ["CON-SRC-001", "CON-SRC-001"]):
                topic = copy.deepcopy(SEED["topics"][0])
                topic["connections"][0].update(edge_status=status, source_ids=refs)
                self.reject(topic)

    def test_strong_ratings_reject_context_and_testimony(self):
        for rating in ("supported", "mixed", "established"):
            for kind, role in (("institutional-record", "definition"),
                               ("institutional-record", "context"), ("testimony", "claim")):
                topic = copy.deepcopy(SEED["topics"][0])
                topic["sources"][1].update(source_type=kind, evidence_role=role)
                topic["solution_space"]["candidates"][0]["evidence_status"] = rating
                self.reject(topic)

    def test_established_unavailable_even_with_replication(self):
        topic = copy.deepcopy(SEED["topics"][0])
        topic["solution_space"]["candidates"][0]["evidence_status"] = "established"
        topic["review"].update(human_reviewed=True, last_reviewed="2026-09-30")
        self.reject(topic)

    def test_public_requires_clearance_and_each_review_rights_field(self):
        topic = copy.deepcopy(SEED["topics"][0])
        topic.update(status="public", public_clearance=self.clearance())
        topic["review"].update(human_reviewed=True, last_reviewed="2026-09-30")
        validate_topic(topic)
        for field in self.clearance():
            altered = copy.deepcopy(topic)
            del altered["public_clearance"][field]
            self.reject(altered)
        for decision in ("HOLD", "cleared"):
            altered = copy.deepcopy(topic)
            altered["public_clearance"]["decision"] = decision
            self.reject(altered)
        altered = copy.deepcopy(topic)
        del altered["public_clearance"]
        self.reject(altered)
        for field, value in (("human_reviewed", False), ("last_reviewed", None)):
            altered = copy.deepcopy(topic)
            altered["review"][field] = value
            self.reject(altered)
        for mode in ("unknown", "metadata-only"):
            altered = copy.deepcopy(topic)
            altered["rights"]["mode"] = mode
            self.reject(altered)

    def test_older_intervention_finding_stays_downgraded(self):
        topic = next(t for t in SEED["topics"] if t["slug"] == "quality-of-life")
        candidate = next(c for c in topic["solution_space"]["candidates"] if c["label"].startswith("Support sleep"))
        self.assertEqual(candidate["evidence_status"], "unassessed")
        altered = copy.deepcopy(topic)
        next(c for c in altered["solution_space"]["candidates"] if c["label"].startswith("Support sleep"))["evidence_status"] = "supported"
        self.reject(altered)

    def test_duplicate_source_identity_rejected(self):
        topic = copy.deepcopy(SEED["topics"][0])
        topic["sources"].append(copy.deepcopy(topic["sources"][0]))
        self.reject(topic)

    def test_claimed_origins_and_routes_use_filtered_records(self):
        page = (ROOT / "website/app/topics/[slug]/page.tsx").read_text()
        data = (ROOT / "website/app/topics/data.ts").read_text()
        self.assertIn("topic.origin.claimed_origins.map", page)
        self.assertIn("No claimed origins recorded.", page)
        self.assertIn("topicSeed.topics.filter(isPublicTopic)", data)
        self.assertIn("return topics.find", data)
        self.assertIn("return topics.map", page)
        self.assertIn("dynamicParams = false", page)
        self.assertIn("if (!topic) notFound()", page)



if __name__ == "__main__":
    unittest.main()
