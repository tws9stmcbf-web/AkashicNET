import copy
import json
import unittest

from scripts import validate_bq001_framework_inventory_v017 as validator


class FrameworkInventoryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = validator.load_json(validator.INVENTORY.read_bytes())

    def mutate(self, change):
        candidate = copy.deepcopy(self.data)
        change(candidate)
        with self.assertRaises(ValueError):
            validator.validate(candidate)

    def test_committed_inventory_passes_and_is_canonical(self):
        validator.validate(self.data)
        self.assertEqual(
            validator.INVENTORY.read_text(encoding="utf-8"),
            validator.canonical(self.data),
        )

    def test_inventory_is_review_only_and_unresolved(self):
        self.assertEqual(self.data["question_status"], "UNRESOLVED")
        self.assertEqual(self.data["mode"], "REVIEW_ONLY")
        self.assertEqual(self.data["summary"]["accepted_edges"], 0)
        self.assertFalse(any(self.data["promotion_guards"].values()))
        self.assertEqual(
            self.data["operational_boundaries"]["reddit_live_access"], "HOLD"
        )

    def test_all_represented_records_are_bound_to_pinned_locators(self):
        validator.validate(self.data)
        self.assertEqual(len(self.data["inventory"]), 11)
        self.assertEqual(len(self.data["governed_artifacts"]), 7)

    def test_gnwt_and_iit_shared_source_cannot_be_double_counted(self):
        items = {item["inventory_item_id"]: item for item in self.data["inventory"]}
        gnwt = items["FW-BQ001-CONSCIOUSNESS-GNWT"]
        iit = items["FW-BQ001-CONSCIOUSNESS-IIT"]
        self.assertEqual(
            set(gnwt["represented_by"]) & set(iit["represented_by"]),
            {"SRC-BQ001-COGITATE-2025", "CLAIM-BQ001-COGITATE-2025-OBS-01"},
        )
        self.assertEqual(
            iit["independence_state"],
            "SHARED_SOURCE_WITH_GNWT_DO_NOT_DOUBLE_COUNT",
        )

    def test_schema_and_governance_mutations_fail_closed(self):
        changes = [
            lambda d: d.update(question_status="RESOLVED"),
            lambda d: d.update(mode="PUBLIC_ANSWER"),
            lambda d: d.update(inherited_v016_readiness_pin="a" * 40),
            lambda d: d["promotion_guards"].update(truth_inference_allowed=True),
            lambda d: d["promotion_guards"].update(framework_count_is_vote=True),
            lambda d: d["promotion_guards"].update(scientific_evidence_promotion_allowed=True),
            lambda d: d["promotion_guards"].update(rights_or_public_release_promotion_allowed=True),
            lambda d: d["promotion_guards"].update(accepted_edge_creation_allowed=True),
            lambda d: d["operational_boundaries"].update(reddit_live_access="APPROVED"),
            lambda d: d["operational_boundaries"].update(private_drive_material_allowed=True),
            lambda d: d["scope"].update(synthesis_or_answer=True),
            lambda d: d["scope"].update(exhaustive_beyond_pinned_artifacts=True),
            lambda d: d["summary"].update(inventory_items=12),
            lambda d: d["summary"].update(accepted_edges=1),
            lambda d: d["governed_artifacts"][0].update(git_blob_sha="a" * 40),
            lambda d: d["inventory"][0].update(unreviewed_score=0.9),
            lambda d: d["inventory"][0].update(status="RESOLVED"),
            lambda d: d["inventory"][0]["represented_by"].append("MODEL-BQ001-INVENTED"),
            lambda d: d["inventory"][0]["pinned_locators"].__setitem__(0, "missing.json#/models/0"),
            lambda d: d["inventory"][1].update(inventory_item_id=d["inventory"][0]["inventory_item_id"]),
            lambda d: next(i for i in d["inventory"] if i["inventory_item_id"] == "FW-BQ001-CONSCIOUSNESS-IIT").update(independence_state="SINGLE_GOVERNED_SOURCE_DO_NOT_COUNT_AS_REPLICATION"),
        ]
        for index, change in enumerate(changes):
            with self.subTest(index=index):
                self.mutate(change)

    def test_private_metadata_and_encoded_links_fail_closed(self):
        changes = [
            lambda d: d["inventory"][0].update(drive_id="synthetic"),
            lambda d: d["inventory"][0].update({"drive%5fid": "synthetic"}),
            lambda d: d["inventory"][0].update({"file%70ath": "synthetic"}),
            lambda d: d["inventory"][0].update({"drive%255fid": "synthetic"}),
            lambda d: d["inventory"][0].update(boundary="https://drive.google.com/file/d/synthetic/view"),
            lambda d: d["inventory"][0].update(boundary="https%3A%2F%2Fdrive.google.com%2Ffile%2Fd%2Fsynthetic"),
            lambda d: d["inventory"][0].update(boundary="/My Drive/private.pdf"),
        ]
        for index, change in enumerate(changes):
            with self.subTest(index=index):
                self.mutate(change)

    def test_json_pointer_array_indices_are_canonical(self):
        document = {"items": list(range(11))}
        self.assertEqual(validator.resolve_pointer(document, "/items/0"), 0)
        self.assertEqual(validator.resolve_pointer(document, "/items/10"), 10)
        for pointer in ("/items/-1", "/items/+1", "/items/", "/items/00", "/items/01"):
            with self.subTest(pointer=pointer), self.assertRaises(ValueError):
                validator.resolve_pointer(document, pointer)

    def test_duplicate_keys_and_nonfinite_json_fail_closed(self):
        for raw in (
            '{"question_id":"BQ001","question_id":"other"}',
            '{"x":NaN}',
            '{"x":Infinity}',
        ):
            with self.subTest(raw=raw), self.assertRaises(ValueError):
                validator.load_json(raw)


if __name__ == "__main__":
    unittest.main()
