import copy
import unittest

from scripts.build_public_safe_semantic_endpoint_registry_v019 import build_registry, is_public_question, parse_drive, validate_registry


ARTIFACTS = [{"artifact_id": "artifact:test", "repository_record": "fixture", "sha256": "1" * 64, "public_safe": True}]


class TestSemanticEndpointRegistry(unittest.TestCase):
    def test_drive_parser_excludes_markdown_separator(self):
        table = """| family_id | title | status | provenance |\n| --- | --- | --- | --- |\n| BARDON-001 | A real publication | merged | public |\n"""
        self.assertEqual(parse_drive(table), [("BARDON-001", "A real publication")])

    def test_unpublished_question_does_not_require_public_synthesis(self):
        from pathlib import Path
        from tempfile import TemporaryDirectory

        with TemporaryDirectory() as directory:
            root = Path(directory)
            spec_rel = "references/big-questions/BQ002/spec-v0.1.json"
            spec_path = root / spec_rel
            spec_path.parent.mkdir(parents=True)
            spec_path.write_text('{"id": "BQ002", "public_beta_gate": false}')
            self.assertFalse(is_public_question("BQ002", {"spec": spec_rel}, root))
            self.assertFalse((spec_path.parent / "public-synthesis-v0.1.json").exists())

    def registry(self):
        return build_registry(
            {"topic alpha": "Topic Alpha"}, {"Framework Alpha"}, [("PUB-001", "Publication Alpha")],
            [("BQ001", "Question Alpha?", "question-record")],
            [("SRC-001", "Evidence Alpha", "artifact:evidence", "source:evidence:src-001")], ARTIFACTS,
        )

    def test_all_real_endpoint_classes_except_source_record(self):
        data = self.registry()
        self.assertEqual(validate_registry(data), [])
        self.assertEqual({e["endpoint_type"] for e in data["endpoints"]}, {"TOPIC", "FRAMEWORK", "PUBLICATION", "QUESTION", "EVIDENCE_RECORD"})
        self.assertEqual(data["edges"], [])

    def mutate(self, change):
        data = self.registry()
        change(data)
        self.assertTrue(validate_registry(data))

    def test_truth_inference_fails_closed(self): self.mutate(lambda d: d["boundaries"].__setitem__("automated_truth_inference_allowed", True))
    def test_acceptance_fails_closed(self): self.mutate(lambda d: d["boundaries"].__setitem__("automated_acceptance_allowed", True))
    def test_edge_fails_closed(self): self.mutate(lambda d: d["edges"].append({"edge_id": "forbidden"}))
    def test_duplicate_id_fails_closed(self): self.mutate(lambda d: d["endpoints"][1].__setitem__("endpoint_id", d["endpoints"][0]["endpoint_id"]))
    def test_private_metadata_fails_closed(self): self.mutate(lambda d: d.__setitem__("drive_id", "private"))
    def test_provenance_fails_closed(self): self.mutate(lambda d: d["endpoints"][0]["provenance"].__setitem__("public_safe", False))
    def test_summary_fails_closed(self): self.mutate(lambda d: d["summary"].__setitem__("accepted_edges", 1))


if __name__ == "__main__":
    unittest.main()
