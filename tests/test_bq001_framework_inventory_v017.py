import copy
import json
import unittest
import tempfile
from pathlib import Path
from unittest.mock import patch

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

    def test_coordinated_governed_file_and_hash_change_rejected(self):
        artifact = self.data["governed_artifacts"][0]
        document = validator.load_json((validator.ROOT / artifact["path"]).read_bytes())
        document["synthetic_unreviewed_field"] = "changed"
        raw = validator.canonical(document).encode()
        candidate = copy.deepcopy(self.data)
        candidate["governed_artifacts"][0]["git_blob_sha"] = validator.git_blob_sha(raw)
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = root / artifact["path"]
            target.parent.mkdir(parents=True)
            target.write_bytes(raw)
            with patch.object(validator, "ROOT", root):
                with self.assertRaisesRegex(
                    ValueError, "unscoped git blob rejected|governed artifact pin drift"
                ):
                    validator.validate(candidate)

    def test_governed_artifact_path_substitution_rejected(self):
        self.mutate(lambda d: d["governed_artifacts"][0].update(
            path="references/big-questions/BQ001/substitute.json"
        ))

    def test_each_governed_document_is_privacy_scanned(self):
        mutations = (
            {"drive%255fid": "synthetic"},
            {"file%70ath": "synthetic"},
            {"synthetic_note": "https%253A%252F%252Fdrive.google.com%252Ffile%252Fd%252Fsynthetic"},
        )
        for artifact in self.data["governed_artifacts"]:
            for mutation in mutations:
                with self.subTest(path=artifact["path"], mutation=mutation):
                    document = validator.load_json((validator.ROOT / artifact["path"]).read_bytes())
                    document.update(mutation)
                    raw = validator.canonical(document).encode()
                    read_bytes = Path.read_bytes
                    def substituted_read(path):
                        if path == validator.ROOT / artifact["path"]:
                            return raw
                        return read_bytes(path)
                    hash_blob = validator.git_blob_sha
                    def isolated_hash(value):
                        # Isolate the scanner from the independently tested pin gate.
                        return artifact["git_blob_sha"] if value == raw else hash_blob(value)
                    with patch.object(Path, "read_bytes", substituted_read):
                        with patch.object(validator, "git_blob_sha", isolated_hash):
                            with self.assertRaisesRegex(ValueError, "private metadata rejected"):
                                validator.validate(self.data)

    def test_collection_locators_are_rejected(self):
        def broaden(data):
            item = data["inventory"][2]
            item["pinned_locators"] = [p.rsplit("/", 1)[0] for p in item["pinned_locators"]]
        self.mutate(broaden)

    def test_terminal_identity_and_claim_relationship_are_required(self):
        item = copy.deepcopy(self.data["inventory"][2])
        documents = {Path(a["path"]).name: validator.load_json(
            (validator.ROOT / a["path"]).read_bytes()) for a in self.data["governed_artifacts"]}
        validator.validate_locators(item, documents)
        # A represented ID hidden in prose must not substitute for a record identity.
        source = documents["evidence-batch4-v0.1.json"]["sources"][3]
        source["synthetic_note"] = source["source_id"]
        source["source_id"] = "SRC-BQ001-SYNTHETIC"
        with self.assertRaisesRegex(ValueError, "terminal record"):
            validator.validate_locators(item, documents)
        source["source_id"] = source.pop("synthetic_note")
        documents["evidence-batch4-v0.1.json"]["claims"][3]["source_ids"] = ["SRC-BQ001-SYNTHETIC"]
        with self.assertRaisesRegex(ValueError, "relationship drift"):
            validator.validate_locators(item, documents)

    def test_category_swaps_and_semantic_drift_are_rejected(self):
        def swap_categories(data):
            a, b = data["inventory"][2], data["inventory"][5]
            a["category"], b["category"] = b["category"], a["category"]
        self.mutate(swap_categories)
        self.mutate(lambda d: d["inventory"][2].update(canonical_name="Unreviewed framework"))
        self.mutate(lambda d: d["inventory"][2].update(status="EMPIRICALLY_TESTED_NOT_ADJUDICATED_FOR_BQ001"))

    def test_third_shared_source_owner_and_independence_drift_rejected(self):
        def add_third_owner(data):
            third = data["inventory"][2]
            gnwt = data["inventory"][-2]
            third["represented_by"] += gnwt["represented_by"]
            third["pinned_locators"] += gnwt["pinned_locators"]
        self.mutate(add_third_owner)
        items = copy.deepcopy(self.data["inventory"])
        items[2]["represented_by"] += items[-2]["represented_by"]
        with self.assertRaisesRegex(ValueError, "membership requires review"):
            validator.validate_shared_sources(items)
        for index in (-2, -1):
            items = copy.deepcopy(self.data["inventory"])
            items[index]["independence_state"] = "UNASSESSED_REVIEW_REQUIRED"
            with self.assertRaisesRegex(ValueError, "independence state drift"):
                validator.validate_shared_sources(items)

    def test_slice_cannot_claim_exhaustive_coverage(self):
        self.assertFalse(self.data["scope"]["exhaustive_for_pinned_artifacts"])
        self.assertIn("CLAIM-BQ001-KOCH-2016-INTERP-01", self.data["scope"]["description"])
        self.mutate(lambda d: d["scope"].update(exhaustive_for_pinned_artifacts=True))

    def test_review_only_scope_description_is_pinned(self):
        self.mutate(lambda d: d["scope"].update(
            description="BQ001 has been conclusively resolved."
        ))

    def test_schema_private_metadata_is_rejected_before_schema_validation(self):
        schema = validator.load_json(validator.SCHEMA.read_bytes())
        schema["$comment"] = (
            "https%253A%252F%252Fdrive.google.com%252Ffile%252Fd%252Fsynthetic"
        )
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "schema.json"
            path.write_text(validator.canonical(schema), encoding="utf-8")
            with patch.object(validator, "SCHEMA", path):
                with self.assertRaisesRegex(ValueError, "private metadata rejected"):
                    validator.validate(self.data)

    def test_core_review_only_invariants_do_not_trust_mutable_schema(self):
        schema = validator.load_json(validator.SCHEMA.read_bytes())
        schema["properties"]["question_status"]["const"] = "RESOLVED"
        schema["properties"]["mode"]["const"] = "PUBLIC_ANSWER"
        schema["properties"]["scope"]["properties"]["synthesis_or_answer"]["const"] = True
        candidate = copy.deepcopy(self.data)
        candidate["question_status"] = "RESOLVED"
        candidate["mode"] = "PUBLIC_ANSWER"
        candidate["scope"]["synthesis_or_answer"] = True
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "schema.json"
            path.write_text(validator.canonical(schema), encoding="utf-8")
            with patch.object(validator, "SCHEMA", path):
                with self.assertRaisesRegex(ValueError, "core invariant drift"):
                    validator.validate(candidate)

    def test_reviewed_exclusions_are_complete_and_unique(self):
        def duplicate_exclusion(data):
            data["exclusions"] = [copy.deepcopy(data["exclusions"][0]) for _ in range(4)]
        self.mutate(duplicate_exclusion)

    def test_schema_unscoped_git_blob_is_rejected(self):
        schema = validator.load_json(validator.SCHEMA.read_bytes())
        schema["git_blob_sha"] = "a" * 40
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "schema.json"
            path.write_text(validator.canonical(schema), encoding="utf-8")
            with patch.object(validator, "SCHEMA", path):
                with self.assertRaisesRegex(ValueError, "unscoped git blob rejected"):
                    validator.validate(self.data)

    def test_complete_safety_mappings_do_not_trust_mutable_schema(self):
        schema = validator.load_json(validator.SCHEMA.read_bytes())
        schema["properties"]["promotion_guards"]["required"] = []
        schema["properties"]["operational_boundaries"]["required"] = ["reddit_live_access"]
        candidate = copy.deepcopy(self.data)
        candidate["promotion_guards"] = {}
        candidate["operational_boundaries"] = {"reddit_live_access": "HOLD"}
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "schema.json"
            path.write_text(validator.canonical(schema), encoding="utf-8")
            with patch.object(validator, "SCHEMA", path):
                with self.assertRaisesRegex(
                    ValueError,
                    "promotion guards exact allowed-key set drift|promotion guard mapping drift",
                ):
                    validator.validate(candidate)

    def test_exact_allowed_keys_survive_coordinated_schema_weakening(self):
        schema = validator.load_json(validator.SCHEMA.read_bytes())

        def allow_extensions(value):
            if isinstance(value, dict):
                if "additionalProperties" in value:
                    value["additionalProperties"] = True
                for child in value.values():
                    allow_extensions(child)
            elif isinstance(value, list):
                for child in value:
                    allow_extensions(child)

        allow_extensions(schema)
        mutations = (
            lambda d: d.update(answer="synthetic"),
            lambda d: d["scope"].update(answer="synthetic"),
            lambda d: d["summary"].update(answer=1),
            lambda d: d["promotion_guards"].update(answer=False),
            lambda d: d["operational_boundaries"].update(answer=False),
            lambda d: d["governed_artifacts"][0].update(answer="synthetic"),
            lambda d: d["exclusions"][0].update(answer="synthetic"),
            lambda d: d["inventory"][0].update(answer="synthetic"),
        )
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "schema.json"
            path.write_text(validator.canonical(schema), encoding="utf-8")
            with patch.object(validator, "SCHEMA", path):
                for mutation in mutations:
                    with self.subTest(mutation=mutation):
                        candidate = copy.deepcopy(self.data)
                        mutation(candidate)
                        with self.assertRaisesRegex(ValueError, "allowed-key set drift"):
                            validator.validate(candidate)

    def test_idna_dot_variants_in_private_hosts_are_rejected(self):
        for encoded_dot in ("%E3%80%82", "%EF%BC%8E", "%EF%BD%A1"):
            with self.subTest(encoded_dot=encoded_dot):
                with self.assertRaisesRegex(ValueError, "private metadata rejected"):
                    validator.privacy_check(
                        f"https://drive{encoded_dot}google{encoded_dot}com/file/d/private"
                    )

    def test_nfkc_normalized_forbidden_metadata_keys_are_rejected(self):
        keys = (
            "ｄｒｉｖｅ＿ｉｄ",
            "%EF%BD%84%EF%BD%92%EF%BD%89%EF%BD%96%EF%BD%85%EF%BC%BF%EF%BD%89%EF%BD%84",
        )
        for key in keys:
            with self.subTest(key=key):
                with self.assertRaisesRegex(ValueError, "private metadata rejected"):
                    validator.privacy_check({key: "synthetic"})

    def test_unicode_normalized_private_url_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "private metadata rejected"):
            validator.privacy_check(
                "https://drive%EF%BC%8Egoogle%EF%BC%8Ecom/file/d/private"
            )

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


    def test_item_boundaries_relations_and_locators_are_pinned(self):
        self.mutate(lambda d: d["inventory"][0].update(
            boundary="This changed boundary would weaken review-only scope."
        ))
        self.mutate(lambda d: d["inventory"][0].update(
            relation_to_bq001="This changed relation would be unreviewed."
        ))
        self.mutate(lambda d: d["inventory"][0]["pinned_locators"].pop())

    def test_governed_artifact_roles_are_path_bound(self):
        def swap_roles(data):
            data["governed_artifacts"][0]["role"], data["governed_artifacts"][1]["role"] = (
                data["governed_artifacts"][1]["role"],
                data["governed_artifacts"][0]["role"],
            )
        self.mutate(swap_roles)


if __name__ == "__main__":
    unittest.main()
