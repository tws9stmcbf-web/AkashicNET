import copy
import importlib.util
import sys
import unittest
import tempfile
from unittest.mock import patch
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts/validate_bq001_framework_comparison_v017.py"
SPEC = importlib.util.spec_from_file_location("comparison_validator", MODULE_PATH)
validator = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = validator
SPEC.loader.exec_module(validator)


class FrameworkComparisonValidationTests(unittest.TestCase):
    def setUp(self):
        self.packet = validator.load_json(validator.PACKET)

    def validate(self, packet):
        validator.validate(packet, verify_git=False)

    def mutate(self, change, pattern=None):
        candidate = copy.deepcopy(self.packet)
        change(candidate)
        context = self.assertRaisesRegex(Exception, pattern) if pattern else self.assertRaises(Exception)
        with context:
            self.validate(candidate)

    def test_unicode_escape_digests_rejected(self):
        for token in (r"\u0061", r"\U00000061", r"\u{0061}", r"%5Cu0061", r"\u005cu0061"):
            encoded = token * 64
            for value in (encoded, [encoded[:99], encoded[99:]],
                          {encoded[:99]: encoded[99:]}):
                with self.subTest(token=token, value=value), self.assertRaisesRegex(
                    ValueError, "unscoped digest rejected"
                ):
                    validator.scan_safety(value)

    def test_unicode_escape_benign_text_passes(self):
        for value in (r"caf\u00e9", r"ordinary \U0001F333 text", r"\u{1F333}",
                      r"invalid \uZZZZ text", r"C:\users\notes"):
            validator.scan_safety(value)

    def test_nested_uppercase_unicode_escape_rejected(self):
        for encoded in (r"https://\u005c\u005500000064rive.google.com/file/d/private",
                        r"\u005c\u005500000061" * 64):
            for value in (encoded, [encoded[:17], encoded[17:]],
                          {encoded[:17]: encoded[17:]}):
                with self.subTest(value=value), self.assertRaises(ValueError):
                    validator.scan_safety(value)

    def test_reviewed_packet_passes(self):
        self.validate(self.packet)

    def test_hex_escape_private_locators_rejected(self):
        for encoded in (r"https://\x64rive.google.com/file/d/private",
                        r"https://%5Cx64rive.google.com/file/d/private",
                        r"https://\u005cx64rive.google.com/file/d/private",
                        r"https://\x5cU00000064rive.google.com/file/d/private",
                        r"\x66ile://private"):
            for value in (encoded, [encoded[:11], encoded[11:]],
                          {encoded[:11]: encoded[11:]}):
                with self.subTest(value=value), self.assertRaisesRegex(ValueError, "private"):
                    validator.scan_safety(value)
            schema = validator.load_json(validator.SCHEMA)
            schema["$comment"] = encoded
            with tempfile.TemporaryDirectory() as directory:
                path = Path(directory) / "schema.json"
                path.write_text(json.dumps(schema), encoding="utf-8")
                with patch.object(validator, "SCHEMA", path):
                    with self.assertRaisesRegex(ValueError, "private"):
                        self.validate(self.packet)

    def test_hex_escape_digest_and_benign_controls(self):
        for encoded in (r"\x61" * 64, r"\xff" * 32, r"\x00" * 32):
            with self.subTest(encoded=encoded), self.assertRaisesRegex(ValueError, "digest"):
                validator.scan_safety(encoded)
        for value in (r"ordinary \x41 text", r"invalid \xZZ text", r"https://example.com/\x61"):
            validator.scan_safety(value)

    def test_core_review_only_boundaries_are_closed(self):
        self.mutate(lambda d: d.update(question_status="RESOLVED"))
        self.mutate(lambda d: d.update(accepted_edges=1))
        self.mutate(lambda d: d.update(mode="PUBLIC_SYNTHESIS"))
        self.mutate(lambda d: d["operational_boundaries"].update(reddit_live_access="LIVE"))
        self.mutate(lambda d: d["promotion_guards"].update(truth_inference_allowed=True))

    def test_adjudicative_fields_fail_closed(self):
        self.mutate(lambda d: d["comparison_rows"][0].update(score=0.9))
        with self.assertRaisesRegex(ValueError, "adjudicative key rejected"):
            validator.scan_safety({"winner": "synthetic"})
        for key in ("s_c_o_r_e", "r-a-n-k", "s%63ore", "ｗｉｎｎｅｒ"):
            with self.subTest(key=key), self.assertRaisesRegex(
                ValueError, "adjudicative key rejected"
            ):
                validator.scan_safety({key: "synthetic"})

        schema = validator.load_json(validator.SCHEMA)
        schema["x-review-metadata"] = {"s_c_o_r_e": 0.9, "r-a-n-k": 1}
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "schema.json"
            path.write_text(json.dumps(schema), encoding="utf-8")
            with patch.object(validator, "SCHEMA", path):
                with self.assertRaisesRegex(ValueError, "adjudicative key rejected"):
                    self.validate(self.packet)

    def test_inventory_projection_cannot_drift(self):
        self.mutate(lambda d: d["comparison_rows"][2].update(canonical_name="Synthetic"), "inventory projection drift")
        self.mutate(lambda d: d["comparison_rows"][2]["linked_record_ids"].pop(), "inventory projection drift")
        self.mutate(lambda d: d["comparison_rows"][0].update(comparison_state="INTERPRETIVE_FRAMEWORK_NOT_EMPIRICAL_ADJUDICATION"), "comparison state drift")

    def test_row_membership_survives_coordinated_schema_changes(self):
        for variant in ("extra_duplicate", "shadowed_assertion", "replaced_duplicate", "missing", "non_list"):
            with self.subTest(variant=variant):
                candidate = copy.deepcopy(self.packet)
                rows = candidate["comparison_rows"]
                if variant == "non_list":
                    candidate["comparison_rows"] = {}
                elif variant == "missing":
                    rows.pop()
                elif variant == "replaced_duplicate":
                    rows[-1] = copy.deepcopy(rows[0])
                else:
                    extra = copy.deepcopy(rows[0])
                    if variant == "shadowed_assertion":
                        extra["evidence_role"] = "Established Evidence"
                    rows.insert(0, extra)
                schema = validator.load_json(validator.SCHEMA)
                schema["properties"]["comparison_rows"] = {}
                validator.Draft202012Validator(schema).validate(candidate)
                with tempfile.TemporaryDirectory() as directory:
                    path = Path(directory) / "schema.json"
                    path.write_text(json.dumps(schema), encoding="utf-8")
                    with patch.object(validator, "SCHEMA", path):
                        with self.assertRaisesRegex(ValueError, "comparison row (cardinality|uniqueness) drift"):
                            self.validate(candidate)

    def test_counter_inferences_and_research_gaps_are_preserved(self):
        self.mutate(lambda d: d["counter_inferences"].pop())
        self.mutate(lambda d: d["research_gaps"].pop())

    def test_shared_source_is_not_double_counted(self):
        self.mutate(lambda d: d["shared_ancestry_groups"][0]["inventory_item_ids"].pop())
        self.mutate(lambda d: d["comparison_rows"][-1].update(independence_state="UNASSESSED_REVIEW_REQUIRED"), "inventory projection drift")

    def test_correction_record_is_preserved(self):
        self.mutate(lambda d: d["correction_records"][0].update(evidence_label_changed=True))
        self.mutate(lambda d: d["correction_records"].clear())

    def test_correction_cardinality_survives_coordinated_schema_changes(self):
        for variant in ("empty", "duplicate", "changed_evidence", "non_list"):
            with self.subTest(variant=variant):
                candidate = copy.deepcopy(self.packet)
                if variant == "empty":
                    candidate["correction_records"] = []
                elif variant == "non_list":
                    candidate["correction_records"] = {}
                else:
                    extra = copy.deepcopy(candidate["correction_records"][0])
                    if variant == "changed_evidence":
                        extra["evidence_label_changed"] = True
                    candidate["correction_records"].append(extra)
                schema = validator.load_json(validator.SCHEMA)
                schema["properties"]["correction_records"] = {}
                validator.Draft202012Validator(schema).validate(candidate)
                with tempfile.TemporaryDirectory() as directory:
                    path = Path(directory) / "schema.json"
                    path.write_text(json.dumps(schema), encoding="utf-8")
                    with patch.object(validator, "SCHEMA", path):
                        with self.assertRaisesRegex(ValueError, "correction record cardinality drift"):
                            self.validate(candidate)

    def test_input_commit_and_blobs_are_pinned(self):
        self.mutate(lambda d: d.update(input_commit="0" * 40))
        self.mutate(lambda d: d["input_anchors"][0].update(git_blob_sha="0" * 40), "input anchor mapping drift|unscoped digest")

    def test_private_drive_markers_are_rejected(self):
        with self.assertRaisesRegex(ValueError, "private Drive/Docs marker rejected"):
            validator.scan_safety("https://drive.google.com/file/d/private")

    def test_duplicate_keys_and_nonfinite_json_fail_closed(self):
        for raw in ('{"x":1,"x":2}', '{"x":NaN}', '{"x":Infinity}'):
            with self.subTest(raw=raw), self.assertRaises(ValueError):
                validator.load_json(raw)

    def test_encoded_private_hosts_and_paths_fail_closed(self):
        for text in (
            "https://drive%2Egoogle%2Ecom/file/d/private",
            "https://drive%252Egoogle.com/private",
            "https://drive。google.com/private",
            "https://drive\u034f.google.com/private",
            "https://drive\ufe0f.google.com/private",
            "https://drive\t.google.com/private",
            "https://drive％２Ｅgoogle.com/private",
            "https://drive.usercontent.google.com/download?id=synthetic",
            "file%3A%2F%2Fprivate", "C:%5CMy%20Drive%5Cprivate",
        ):
            with self.subTest(text=text), self.assertRaisesRegex(ValueError, "private"):
                validator.scan_safety(text)
        validator.scan_safety("https://example.com/public")
        validator.scan_safety("https://images.googleusercontent.com/public")

    def test_identity_survives_coordinated_schema_changes(self):
        for key, value in {"question_id": "BQ002", "packet_id": "OTHER", "version": "2.0.0"}.items():
            candidate = copy.deepcopy(self.packet)
            candidate[key] = value
            schema = validator.load_json(validator.SCHEMA)
            schema["properties"][key]["const"] = value
            with tempfile.TemporaryDirectory() as directory:
                path = Path(directory) / "schema.json"
                path.write_text(json.dumps(schema), encoding="utf-8")
                with patch.object(validator, "SCHEMA", path):
                    with self.subTest(key=key), self.assertRaisesRegex(ValueError, "packet identity drift"):
                        self.validate(candidate)

    def test_boundary_types_survive_coordinated_schema_changes(self):
        for mapping, definition in (
            ("operational_boundaries", "operationalBoundaries"),
            ("promotion_guards", "promotionGuards"),
        ):
            for key, expected in self.packet[mapping].items():
                if type(expected) is not bool:
                    continue
                for value in (0, 0.0):
                    with self.subTest(mapping=mapping, key=key, value=value):
                        candidate = copy.deepcopy(self.packet)
                        candidate[mapping][key] = value
                        schema = validator.load_json(validator.SCHEMA)
                        schema["$defs"][definition]["properties"][key] = {"const": value}
                        validator.Draft202012Validator(schema).validate(candidate)
                        with tempfile.TemporaryDirectory() as directory:
                            path = Path(directory) / "schema.json"
                            path.write_text(json.dumps(schema), encoding="utf-8")
                            with patch.object(validator, "SCHEMA", path):
                                with self.assertRaisesRegex(ValueError, "mapping drift"):
                                    self.validate(candidate)

    def test_correction_types_survive_coordinated_schema_changes(self):
        for value in (0, 0.0):
            with self.subTest(value=value):
                candidate = copy.deepcopy(self.packet)
                candidate["correction_records"][0]["evidence_label_changed"] = value
                schema = validator.load_json(validator.SCHEMA)
                schema["$defs"]["correctionRecord"]["properties"]["evidence_label_changed"] = {"const": value}
                validator.Draft202012Validator(schema).validate(candidate)
                with tempfile.TemporaryDirectory() as directory:
                    path = Path(directory) / "schema.json"
                    path.write_text(json.dumps(schema), encoding="utf-8")
                    with patch.object(validator, "SCHEMA", path):
                        with self.assertRaisesRegex(ValueError, "correction record drift"):
                            self.validate(candidate)

    def test_unscoped_digests_fail_closed(self):
        digests = ["a" * size for size in (32, 40, 64, 128)]
        digests += ["%61" * 64, "Ａ" * 64, validator.INPUT_COMMIT]
        for separator in ("-", ":", " ", "_", ".", "/", "%2D", "%253A", "－", "：", "\u200b"):
            digests.append(separator.join(["a" * 8] * 8))
        digests.append(":".join(["ab"] * 32))
        digests += [":".join(["0xaa"] * 32), "0xaa" * 32,
                    "\\xaa" * 32, "%5Cx%61%61" * 32,
                    "0XAA " * 32, "０ｘａａ：" * 32]
        # Separators may occur inside a byte token, not only between bytes.
        for token in ("0x_aa", "0x_a_a", "0x-aa", "0x a a",
                      "0x%255faa", "０ｘ＿ａａ", "\\x_aa", "0x\u200b_aa",
                      "0_x_aa", "0%255fx%255faa", "０＿ｘ＿ａａ",
                      "\\_x_aa", "0 - x : a_a"):
            digests.append(",".join([token] * 32))
        for digest in digests:
            with self.subTest(digest=digest):
                schema = validator.load_json(validator.SCHEMA)
                schema["$comment"] = "Unscoped digest: " + digest
                with tempfile.TemporaryDirectory() as directory:
                    path = Path(directory) / "schema.json"
                    path.write_text(json.dumps(schema), encoding="utf-8")
                    with patch.object(validator, "SCHEMA", path):
                        with self.assertRaisesRegex(ValueError, "unscoped digest"):
                            self.validate(self.packet)
                with self.assertRaisesRegex(ValueError, "unscoped digest"):
                    validator.scan_safety({"annotation": [digest]})
                with self.assertRaisesRegex(ValueError, "unscoped digest"):
                    validator.scan_safety({digest: "annotation"})
        for digest in ("a" * 64, validator.INPUT_COMMIT):
            with self.assertRaisesRegex(ValueError, "unscoped digest"):
                validator.scan_safety({digest: "annotation"})
        validator.scan_safety("https://example.com/public-study-2025")

    def test_schema_annotations_are_privacy_scanned(self):
        schema = validator.load_json(validator.SCHEMA)
        schema["$comment"] = "https://drive%2Egoogle%2Ecom/file/d/private"
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "schema.json"
            path.write_text(json.dumps(schema), encoding="utf-8")
            with patch.object(validator, "SCHEMA", path):
                with self.assertRaisesRegex(ValueError, "private"):
                    self.validate(self.packet)

    def test_fragmented_annotation_digests_fail_closed(self):
        chunks = ["a1b2c3d4e5f60718", "192a3b4c5d6e7f80", "abcdef0123456789", "9876543210fedcba"]
        variants = [
            chunks,
            [[chunk] for chunk in chunks],
            {f"part{i}": chunk for i, chunk in enumerate(chunks)},
            [{"part": chunk} for chunk in chunks],
            ["%61" * 16] * 4,
            ["０ｘ＿ａａ"] * 32,
            list("a" * 64),
            ["1" * 16, 2222222222222222, "3" * 16, "4" * 16],
            {chunk: "annotation" for chunk in chunks},
        ]
        for annotation in variants:
            with self.subTest(annotation=annotation):
                schema = validator.load_json(validator.SCHEMA)
                schema["x-private-audit"] = annotation
                validator.Draft202012Validator(schema).validate(self.packet)
                with tempfile.TemporaryDirectory() as directory:
                    path = Path(directory) / "schema.json"
                    path.write_text(json.dumps(schema), encoding="utf-8")
                    with patch.object(validator, "SCHEMA", path):
                        with self.assertRaisesRegex(ValueError, "unscoped digest"):
                            self.validate(self.packet)

    def test_key_value_fragmented_digests_fail_closed(self):
        variants = [
            {"a" * 20: "b" * 20},
            {"a" * 16: "b" * 16},
            {"a" * 16: {"b" * 16: ["c" * 16, "d" * 16]}},
            [{"a" * 16: "b" * 16}, {"c" * 16: "d" * 16}],
            {"%2561" * 20: "%2562" * 20},
            {"Ａ" * 20: "Ｂ" * 20},
            {"0_x_aa," * 8: "0_x_bb," * 8},
        ]
        for annotation in variants:
            with self.subTest(annotation=annotation):
                with self.assertRaisesRegex(ValueError, "unscoped digest"):
                    validator.scan_safety({"annotation": annotation})
                schema = validator.load_json(validator.SCHEMA)
                schema["x-private-audit"] = annotation
                validator.Draft202012Validator(schema).validate(self.packet)
                with tempfile.TemporaryDirectory() as directory:
                    path = Path(directory) / "schema.json"
                    path.write_text(json.dumps(schema), encoding="utf-8")
                    with patch.object(validator, "SCHEMA", path):
                        with self.assertRaisesRegex(ValueError, "unscoped digest"):
                            self.validate(self.packet)

    def test_composite_scan_preserves_scoped_digests_and_text_barriers(self):
        validator.scan_safety({"a" * 20: "public annotation", "note": "b" * 20})
        validator.scan_safety(
            {"a" * 20: validator.INPUT_COMMIT, "note": "b" * 20},
            digest_paths={("a" * 20,): validator.INPUT_COMMIT},
        )
        validator.scan_safety({"parts": ["a" * 16, "public annotation", "b" * 16]})
        validator.scan_safety(
            {"parts": ["a" * 16, validator.INPUT_COMMIT, "b" * 16]},
            digest_paths={("parts", 1): validator.INPUT_COMMIT},
        )
        with self.assertRaisesRegex(ValueError, "unscoped digest"):
            validator.scan_safety(
                {"parts": [validator.INPUT_COMMIT]}, digest_paths={("elsewhere",): validator.INPUT_COMMIT}
            )

    def test_normalized_private_metadata_keys_are_rejected(self):
        keys = (
            "drive%5fid", "file%5fname", "drive%255fid",
            "ｄｒｉｖｅ＿ｉｄ", "private-path", "object.sha256",
        )
        for key in keys:
            with self.subTest(key=key), self.assertRaisesRegex(
                ValueError, "private metadata key rejected"
            ):
                validator.scan_safety({key: "synthetic"})

        schema = validator.load_json(validator.SCHEMA)
        schema["x-private-audit"] = {
            "drive%5fid": "opaque Drive ID",
            "file%5fname": "private-title.pdf",
        }
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "schema.json"
            path.write_text(json.dumps(schema), encoding="utf-8")
            with patch.object(validator, "SCHEMA", path):
                with self.assertRaisesRegex(ValueError, "private metadata key rejected"):
                    self.validate(self.packet)


if __name__ == "__main__":
    unittest.main()

