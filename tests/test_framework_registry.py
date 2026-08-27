import copy
import json
import unittest

from tools.framework_registry.validate import DEFAULT_REGISTRY, validate_registry


class FrameworkRegistryTests(unittest.TestCase):
    def setUp(self):
        self.registry = json.loads(DEFAULT_REGISTRY.read_text(encoding="utf-8"))

    def test_curated_registry_is_valid(self):
        self.assertEqual([], validate_registry(self.registry))

    def test_seed_is_conservative_and_akashicnet_is_meta_framework(self):
        frameworks = {item["name"]: item for item in self.registry["frameworks"]}
        self.assertEqual(
            {"UMASC", "METAD", "ACTC", "N2N Signal & Synthesis", "HOMESENSE", "AkashicNET"},
            set(frameworks),
        )
        self.assertEqual("meta-framework", frameworks["AkashicNET"]["entity_type"])
        self.assertEqual("curated_seed_only", self.registry["count_status"])

    def test_duplicate_id_and_alias_collision_are_rejected(self):
        registry = copy.deepcopy(self.registry)
        duplicate = copy.deepcopy(registry["frameworks"][0])
        duplicate["name"] = "Another framework"
        duplicate["short_name"] = "Another"
        registry["frameworks"].append(duplicate)
        registry["generated_count"] += 1
        registry["frameworks"][1]["aliases"].append("HOMESENSE")
        errors = validate_registry(registry)
        self.assertTrue(any("duplicate framework_id" in error for error in errors))
        self.assertTrue(any("duplicate canonical name/short name/alias" in error for error in errors))

    def test_dangling_relationship_and_provenance_are_rejected(self):
        registry = copy.deepcopy(self.registry)
        registry["relationships"][0]["target_framework_id"] = "fw-missing"
        registry["relationships"][0]["source_refs"] = ["src-missing"]
        errors = validate_registry(registry)
        self.assertTrue(any("unknown target_framework_id" in error for error in errors))
        self.assertTrue(any("unknown source_ref" in error for error in errors))

    def test_undocumented_latest_version_is_rejected(self):
        registry = copy.deepcopy(self.registry)
        registry["frameworks"][0]["latest_version"] = "1.0"
        self.assertTrue(any("latest_version" in error for error in validate_registry(registry)))


if __name__ == "__main__":
    unittest.main()
