import copy
import hashlib
import json
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts.build_knowledge_graph_beta_fixture_v016 import OUTPUT, SOURCE_SPECS, build
from scripts.validate_knowledge_graph_beta_v016 import validate

DATA = json.loads(OUTPUT.read_text())
SCHEMA = json.loads(
    (Path(__file__).resolve().parents[1] / "schemas/knowledge-graph-beta-v0.16.schema.json").read_text()
)


class TestKnowledgeGraphBetaV016(unittest.TestCase):
    def mutate(self, operation, expected=None):
        data = copy.deepcopy(DATA)
        operation(data)
        errors = validate(data)
        self.assertTrue(errors)
        if expected:
            self.assertIn(expected, errors)

    def test_baseline(self):
        self.assertEqual(validate(DATA), [])

    def test_generation_is_deterministic(self):
        self.assertEqual(build(), DATA)
        self.assertEqual(build(), build())

    def test_review_generation_survives_source_digest_drift(self):
        original = Path.read_bytes

        def drifted(path):
            raw = original(path)
            if str(path).endswith("spec-v0.1.json"):
                return raw + b"\n"
            return raw

        with patch.object(Path, "read_bytes", autospec=True, side_effect=drifted):
            generated = build()
            self.assertNotEqual(
                generated["source_artifacts"][0]["sha256"],
                SOURCE_SPECS["artifact:bq001-spec:0.1"]["sha256"],
            )
            self.assertIn("source artifacts", validate(generated))

    def test_sealed_baseline_lock(self):
        self.mutate(lambda d: d["baseline_locks"].__setitem__("v0.14", "0" * 40), "sealed baseline locks")

    def test_schema_pins_sealed_baselines(self):
        properties = SCHEMA["properties"]["baseline_locks"]["properties"]
        self.assertEqual(
            {name: definition.get("const") for name, definition in properties.items()},
            {
                "v0.14": "7b6cfd89de570c4b945d574dad570c37825645fe",
                "v0.15_release": "ea46629558ff57970f6efd2485a7e9a288dc55f2",
                "v0.15_seal": "5ba6989aade68461c8f3953c4a82cc0e158b0730",
            },
        )

    def test_schema_relationships_bind_governance(self):
        expected = {
            "HAS_MODEL": ("DIRECT_SOURCE_METADATA", "SOURCE_ASSERTED", "DIRECT_RECORD"),
            "SUPPORTS_MODEL_CANDIDATE": ("INFERRED_CANDIDATE", "REVIEW_REQUIRED", "HUMAN_REVIEW_CANDIDATE"),
            "COMPETES_WITH_CANDIDATE": ("INFERRED_CANDIDATE", "REVIEW_REQUIRED", "HUMAN_REVIEW_CANDIDATE"),
            "CORRECTS": ("DIRECT_SOURCE_METADATA", "SOURCE_ASSERTED", "DIRECT_RECORD"),
        }
        actual = {}
        for condition in SCHEMA["$defs"]["edge"]["allOf"]:
            relationship = condition["if"]["properties"].get("relationship_type", {}).get("const")
            if relationship not in expected:
                continue
            properties = condition["then"]["properties"]
            actual[relationship] = (
                properties["assertion_class"]["const"],
                properties["review_state"]["const"],
                properties["provenance"]["properties"]["derivation_method"]["const"],
            )
        self.assertEqual(actual, expected)

    def test_schema_relationships_bind_endpoint_namespaces(self):
        expected = {
            "HAS_MODEL": ("^node:question:", "^node:model:"),
            "SUPPORTS_MODEL_CANDIDATE": ("^node:claim:", "^node:model:"),
            "COMPETES_WITH_CANDIDATE": ("^node:model:", "^node:model:"),
            "CORRECTS": ("^node:notice:", "^node:source:"),
        }
        actual = {}
        for condition in SCHEMA["$defs"]["edge"]["allOf"]:
            relationship = condition["if"]["properties"].get("relationship_type", {}).get("const")
            if relationship not in expected:
                continue
            properties = condition["then"]["properties"]
            actual[relationship] = (
                properties["source_node_id"]["pattern"],
                properties["target_node_id"]["pattern"],
            )
        self.assertEqual(actual, expected)

    def test_schema_nodes_bind_type_to_id_namespace(self):
        variants = SCHEMA["$defs"]["node"]["allOf"][0]["oneOf"]
        actual = {
            variant["properties"]["node_type"]["const"]: variant["properties"]["node_id"]["pattern"]
            for variant in variants
        }
        self.assertEqual(
            actual,
            {
                "QUESTION": "^node:question:",
                "MODEL": "^node:model:",
                "SOURCE": "^node:source:",
                "CLAIM": "^node:claim:",
                "NOTICE": "^node:notice:",
            },
        )

    def test_schema_pins_governed_sources(self):
        expected = {
            (
                "artifact:bq001-spec:0.1",
                "references/big-questions/BQ001/spec-v0.1.json",
                "0a0f1fc57b55df100fb8583fc6e28cd38324737c460465ea2269a51f637d4819",
                "source:bq001:spec-v0.1",
            ),
            (
                "artifact:bq001-evidence-batch2:0.1",
                "references/big-questions/BQ001/evidence-batch2-v0.1.json",
                "ddcf9bf5f909a98f289b7ef816673f23cd0ec8ae26b8416c15d87b8690926cc1",
                "source:bq001:evidence-batch2-v0.1",
            ),
        }

        def pins(variants):
            return {
                (
                    item["properties"]["artifact_id"]["const"],
                    item["properties"]["repository_path"]["const"],
                    item["properties"]["sha256"]["const"],
                    item["properties"]["independence_key"]["const"],
                )
                for item in variants
            }

        self.assertEqual(pins(SCHEMA["$defs"]["sourceArtifact"]["oneOf"]), expected)
        self.assertEqual(pins(SCHEMA["$defs"]["provenance"]["allOf"][0]["oneOf"]), expected)
        source_array = SCHEMA["properties"]["source_artifacts"]
        self.assertEqual((source_array["minItems"], source_array["maxItems"]), (2, 2))
        self.assertTrue(source_array["uniqueItems"])

    def test_schema_pins_fixed_fixture_cardinalities(self):
        properties = SCHEMA["properties"]
        self.assertEqual((properties["nodes"]["minItems"], properties["nodes"]["maxItems"]), (6, 6))
        self.assertEqual((properties["edges"]["minItems"], properties["edges"]["maxItems"]), (4, 4))
        self.assertEqual((properties["edges"]["minContains"], properties["edges"]["maxContains"]), (2, 2))
        self.assertEqual(
            properties["edges"]["contains"]["properties"]["assertion_class"]["const"],
            "INFERRED_CANDIDATE",
        )
        summary = properties["summary"]["properties"]
        self.assertEqual(
            {
                "node_count": summary["node_count"]["const"],
                "edge_count": summary["edge_count"]["const"],
                "accepted_edge_count": summary["accepted_edge_count"]["const"],
                "inferred_candidate_count": summary["inferred_candidate_count"]["const"],
                "unresolved_question_count": summary["unresolved_question_count"]["const"],
            },
            {
                "node_count": 6,
                "edge_count": 4,
                "accepted_edge_count": 0,
                "inferred_candidate_count": 2,
                "unresolved_question_count": 1,
            },
        )

    def test_question_remains_unresolved(self):
        self.mutate(lambda d: d.__setitem__("question_status", "RESOLVED"), "question status")

    def test_truth_inference_stays_off(self):
        self.mutate(lambda d: d["boundaries"].__setitem__("automated_truth_inference_allowed", True), "unsafe boundaries")

    def test_source_declaration_cannot_move(self):
        self.mutate(lambda d: d["source_artifacts"][0].__setitem__("sha256", "0" * 64), "source artifacts")

    def test_source_bytes_and_declaration_cannot_move_together(self):
        data = copy.deepcopy(DATA)
        tampered = json.dumps({"valid": "but not the governed source"}).encode()
        moved = hashlib.sha256(tampered).hexdigest()
        data["source_artifacts"][0]["sha256"] = moved
        for node in data["nodes"]:
            if node["provenance"]["artifact_id"] == data["source_artifacts"][0]["artifact_id"]:
                node["provenance"]["sha256"] = moved
        for edge in data["edges"]:
            if edge["provenance"]["artifact_id"] == data["source_artifacts"][0]["artifact_id"]:
                edge["provenance"]["sha256"] = moved
        with patch.object(Path, "read_bytes", return_value=tampered):
            self.assertTrue(validate(data))

    def test_duplicate_node_id(self):
        self.mutate(lambda d: d["nodes"][1].__setitem__("node_id", d["nodes"][0]["node_id"]), "node IDs")

    def test_invalid_node_type(self):
        self.mutate(lambda d: d["nodes"][0].__setitem__("node_type", "TRUTH"), "nodes")

    def test_node_id_cannot_use_edge_namespace(self):
        self.mutate(lambda d: d["nodes"][0].__setitem__("node_id", "edge:question:BQ001"), "nodes")

    def test_missing_endpoint(self):
        self.mutate(lambda d: d["edges"][0].__setitem__("target_node_id", "node:missing"), "edge endpoints")

    def test_self_edge(self):
        self.mutate(lambda d: d["edges"][0].__setitem__("target_node_id", d["edges"][0]["source_node_id"]), "self edge")

    def test_unknown_relationship(self):
        self.mutate(lambda d: d["edges"][0].__setitem__("relationship_type", "PROVES"), "edges")

    def test_edge_id_cannot_use_node_namespace(self):
        self.mutate(lambda d: d["edges"][0].__setitem__("edge_id", "node:not-an-edge"), "edges")

    def test_no_edge_is_accepted(self):
        self.mutate(lambda d: d["edges"][0].__setitem__("accepted_edge", True), "accepted edges prohibited")

    def test_inferred_candidate_requires_review(self):
        self.mutate(lambda d: d["edges"][1].__setitem__("review_state", "SOURCE_ASSERTED"), "inferred review boundary")

    def test_candidate_relationship_cannot_be_reclassified_as_direct(self):
        def reclassify(data):
            edge = data["edges"][1]
            edge["assertion_class"] = "DIRECT_SOURCE_METADATA"
            edge["review_state"] = "SOURCE_ASSERTED"
            edge["provenance"]["derivation_method"] = "DIRECT_RECORD"
        self.mutate(reclassify, "relationship assertion contract")

    def test_direct_metadata_requires_direct_provenance(self):
        self.mutate(lambda d: d["edges"][0]["provenance"].__setitem__("derivation_method", "HUMAN_REVIEW_CANDIDATE"), "direct metadata boundary")

    def test_correction_not_mislabeled_retracted(self):
        self.mutate(lambda d: d["edges"][3].__setitem__("edge_state", "RETRACTED"), "relationship state")

    def test_competing_models_remain_review_only(self):
        self.mutate(lambda d: d["edges"][2].__setitem__("edge_state", "ACTIVE"), "relationship state")

    def test_duplicate_independence_key_rejected(self):
        self.mutate(lambda d: d["edges"][0].__setitem__("evidence_independence_keys", [d["edges"][0]["evidence_independence_keys"][0]] * 2), "evidence independence")

    def test_unknown_independence_key_rejected(self):
        self.mutate(lambda d: d["edges"][0].__setitem__("evidence_independence_keys", ["source:invented"]), "evidence independence")

    def test_independence_key_must_be_traceable_to_edge_provenance(self):
        self.mutate(
            lambda d: d["edges"][0].__setitem__(
                "evidence_independence_keys",
                ["source:bq001:evidence-batch2-v0.1"],
            ),
            "evidence independence",
        )

    def test_missing_record_locator(self):
        self.mutate(lambda d: d["nodes"][0]["provenance"].__setitem__("record_locator", "/missing"), "record locator")

    def test_negative_list_index_is_rejected(self):
        self.mutate(
            lambda d: d["nodes"][1]["provenance"].__setitem__("record_locator", "/models/-1/model_id"),
            "record locator",
        )

    def test_existing_locator_must_identify_the_node_record(self):
        self.mutate(lambda d: d["nodes"][1]["provenance"].__setitem__("record_locator", "/models/1/model_id"), "record identity")

    def test_relationship_requires_typed_endpoints(self):
        self.mutate(lambda d: d["edges"][0].__setitem__("source_node_id", "node:claim:CLAIM-BQ001-MARTIAL-2025-INTERP-01"), "relationship endpoint types")

    def test_support_candidate_cannot_use_contradiction_state(self):
        self.mutate(lambda d: d["edges"][1].__setitem__("edge_state", "REVIEW_ONLY_CONTRADICTION"), "relationship state")

    def test_unknown_parent_edge(self):
        self.mutate(lambda d: d["edges"][0]["parent_edge_ids"].append("edge:missing"), "edge ancestry")

    def test_circular_parent_lineage(self):
        def cycle(data):
            data["edges"][0]["parent_edge_ids"] = [data["edges"][1]["edge_id"]]
            data["edges"][1]["parent_edge_ids"] = [data["edges"][0]["edge_id"]]
        self.mutate(cycle, "circular ancestry")

    def test_valid_nonempty_ancestry_preserves_one_lineage(self):
        data = copy.deepcopy(DATA)
        direct_edge = data["edges"][0]
        inferred_edge = data["edges"][2]
        inferred_edge["parent_edge_ids"] = [direct_edge["edge_id"]]
        errors = validate(data)
        self.assertIn("deterministic artifact", errors)
        self.assertNotIn("edge ancestry", errors)
        self.assertNotIn("edge ancestry policy", errors)
        self.assertNotIn("circular ancestry", errors)
        self.assertNotIn("evidence independence", errors)

    def test_child_must_disclose_every_inherited_lineage(self):
        data = copy.deepcopy(DATA)
        inferred_edge = data["edges"][2]
        correction_edge = data["edges"][3]
        inferred_edge["parent_edge_ids"] = [correction_edge["edge_id"]]
        errors = validate(data)
        self.assertIn("evidence independence", errors)

    def test_unrelated_parent_cannot_launder_independence(self):
        data = copy.deepcopy(DATA)
        inferred_edge = data["edges"][2]
        correction_edge = data["edges"][3]
        inferred_edge["parent_edge_ids"] = [correction_edge["edge_id"]]
        inferred_edge["evidence_independence_keys"] = [
            "source:bq001:spec-v0.1",
            "source:bq001:evidence-batch2-v0.1",
        ]
        self.assertIn("edge ancestry policy", validate(data))

    def test_model_membership_cannot_support_a_claim_inference(self):
        data = copy.deepcopy(DATA)
        model_membership_edge = data["edges"][0]
        support_edge = data["edges"][1]
        support_edge["parent_edge_ids"] = [model_membership_edge["edge_id"]]
        support_edge["evidence_independence_keys"] = sorted(
            set(
                support_edge["evidence_independence_keys"]
                + model_membership_edge["evidence_independence_keys"]
            )
        )
        errors = validate(data)
        self.assertIn("deterministic artifact", errors)
        self.assertIn("edge ancestry policy", errors)
        self.assertNotIn("edge ancestry", errors)
        self.assertNotIn("evidence independence", errors)

    def test_parent_has_model_must_use_question_membership_provenance(self):
        data = copy.deepcopy(DATA)
        model_membership_edge = data["edges"][0]
        support_edge = data["edges"][1]
        competing_edge = data["edges"][2]
        model_membership_edge["provenance"] = copy.deepcopy(support_edge["provenance"])
        model_membership_edge["provenance"]["derivation_method"] = "DIRECT_RECORD"
        model_membership_edge["evidence_independence_keys"] = [
            model_membership_edge["provenance"]["independence_key"]
        ]
        competing_edge["parent_edge_ids"] = [model_membership_edge["edge_id"]]
        competing_edge["evidence_independence_keys"] = sorted(
            set(
                competing_edge["evidence_independence_keys"]
                + model_membership_edge["evidence_independence_keys"]
            )
        )
        errors = validate(data)
        self.assertIn("deterministic artifact", errors)
        self.assertIn("edge ancestry policy", errors)
        self.assertNotIn("edge ancestry", errors)
        self.assertNotIn("evidence independence", errors)
        self.assertNotIn("record identity", errors)

    def test_parent_source_must_resolve_to_bq001_question_record(self):
        data = copy.deepcopy(DATA)
        question_node = data["nodes"][0]
        continuity_model_node = data["nodes"][1]
        model_membership_edge = data["edges"][0]
        competing_edge = data["edges"][2]
        question_node["record_id"] = continuity_model_node["record_id"]
        question_node["provenance"] = copy.deepcopy(continuity_model_node["provenance"])
        competing_edge["parent_edge_ids"] = [model_membership_edge["edge_id"]]
        errors = validate(data)
        self.assertIn("deterministic artifact", errors)
        self.assertIn("edge ancestry policy", errors)
        self.assertNotIn("edge ancestry", errors)
        self.assertNotIn("evidence independence", errors)
        self.assertNotIn("record identity", errors)
        self.assertNotIn("relationship endpoint types", errors)

    def test_parented_competition_requires_distinct_model_records(self):
        data = copy.deepcopy(DATA)
        continuity_node = next(
            node
            for node in data["nodes"]
            if node.get("record_id") == "MODEL-BQ001-CONTINUITY"
        )
        biological_node = next(
            node
            for node in data["nodes"]
            if node.get("record_id") == "MODEL-BQ001-BIOLOGICAL-DEPENDENCE"
        )
        model_membership_edge = data["edges"][0]
        competing_edge = data["edges"][2]
        continuity_node["record_id"] = biological_node["record_id"]
        continuity_node["label"] = biological_node["label"]
        continuity_node["provenance"] = copy.deepcopy(biological_node["provenance"])
        competing_edge["parent_edge_ids"] = [model_membership_edge["edge_id"]]
        errors = validate(data)
        self.assertIn("deterministic artifact", errors)
        self.assertIn("semantic self edge", errors)
        self.assertIn("edge ancestry policy", errors)
        self.assertNotIn("self edge", errors)

    def test_malformed_parent_source_provenance_fails_closed(self):
        data = copy.deepcopy(DATA)
        question_node = data["nodes"][0]
        model_membership_edge = data["edges"][0]
        competing_edge = data["edges"][2]
        question_node["provenance"] = None
        competing_edge["parent_edge_ids"] = [model_membership_edge["edge_id"]]
        errors = validate(data)
        self.assertIn("deterministic artifact", errors)
        self.assertIn("provenance", errors)
        self.assertIn("edge ancestry policy", errors)

    def test_malformed_parent_edge_provenance_fails_closed(self):
        data = copy.deepcopy(DATA)
        model_membership_edge = data["edges"][0]
        competing_edge = data["edges"][2]
        model_membership_edge["provenance"] = None
        competing_edge["parent_edge_ids"] = [model_membership_edge["edge_id"]]
        errors = validate(data)
        self.assertIn("deterministic artifact", errors)
        self.assertIn("provenance", errors)
        self.assertIn("direct metadata boundary", errors)
        self.assertIn("relationship assertion contract", errors)
        self.assertIn("edge ancestry policy", errors)

    def test_inferred_parent_cannot_amplify_inferred_child(self):
        data = copy.deepcopy(DATA)
        support_edge = data["edges"][1]
        competing_edge = data["edges"][2]
        competing_edge["parent_edge_ids"] = [support_edge["edge_id"]]
        competing_edge["evidence_independence_keys"] = [
            "source:bq001:spec-v0.1",
            "source:bq001:evidence-batch2-v0.1",
        ]
        self.assertIn("edge ancestry policy", validate(data))

    def test_direct_metadata_cannot_have_parent_edges(self):
        data = copy.deepcopy(DATA)
        correction_edge = data["edges"][3]
        support_edge = data["edges"][1]
        correction_edge["parent_edge_ids"] = [support_edge["edge_id"]]
        self.assertIn("edge ancestry policy", validate(data))

    def test_private_key_rejected(self):
        self.mutate(lambda d: d.__setitem__("drive_id", "private"), "private metadata")

    def test_private_marker_nested_in_array_rejected(self):
        self.mutate(lambda d: d["edges"][0]["evidence_independence_keys"].append("copy_AKM-001234.pdf"), "private metadata")

    def test_private_path_nested_in_array_rejected(self):
        self.mutate(lambda d: d["edges"][0]["parent_edge_ids"].append("/My Drive/private.pdf"), "private metadata")

    def test_summary_is_derived(self):
        self.mutate(lambda d: d["summary"].__setitem__("accepted_edge_count", 1), "summary")


if __name__ == "__main__":
    unittest.main()
