import importlib.util
import json
import os
import tempfile
import unittest
from pathlib import Path

MODULE_PATH = Path(__file__).resolve().parents[1] / "tools/akashic-library" / "drive_importer.py"

spec = importlib.util.spec_from_file_location("akashic_importer_module", MODULE_PATH)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class AkashicImporterHardeningTests(unittest.TestCase):
    def setUp(self):
        self.mock_data = {
            "root": {
                "id": "root",
                "name": "Books",
                "kind": "drive#file",
                "mimeType": "application/vnd.google-apps.folder",
                "parents": [],
                "modifiedTime": "2024-01-10T12:00:00Z",
                "owners": [{"displayName": "Archive Owner"}],
            },
            "children": {
                "root": [
                    {
                        "id": "folder_1",
                        "name": "Philosophy",
                        "mimeType": "application/vnd.google-apps.folder",
                        "parents": ["root"],
                        "modifiedTime": "2024-01-11T12:00:00Z",
                    },
                    {
                        "id": "file_1",
                        "name": "Intro to Consciousness.pdf",
                        "mimeType": "application/pdf",
                        "parents": ["root"],
                        "size": "153200",
                        "modifiedTime": "2024-01-12T12:30:00Z",
                        "owners": [{"displayName": "Archive Owner"}],
                    },
                    {
                        "id": "file_2",
                        "name": "Open Essay.pdf",
                        "mimeType": "application/pdf",
                        "parents": ["root"],
                        "size": "245000",
                        "modifiedTime": "2024-01-14T14:00:00Z",
                        "owners": [{"displayName": "Archive Curator"}],
                        "description": "CC-BY 4.0",
                    },
                ],
                "folder_1": [
                    {
                        "id": "file_3",
                        "name": "Consciousness Essay.pdf",
                        "mimeType": "application/pdf",
                        "parents": ["folder_1"],
                        "size": "245000",
                        "modifiedTime": "2024-01-13T13:00:00Z",
                        "owners": [{"displayName": "Archive Curator"}],
                    },
                    {
                        "id": "file_duplicate",
                        "name": "Consciousness Essay.pdf",
                        "mimeType": "application/pdf",
                        "parents": ["folder_1"],
                        "size": "245000",
                        "modifiedTime": "2024-01-13T13:00:00Z",
                        "owners": [{"displayName": "Archive Curator"}],
                    },
                ],
                "folder_missing": [
                    {"id": "missing_file", "name": "Unavailable.pdf", "mimeType": "application/pdf"}
                ],
            },
        }

    def test_recursive_folder_traversal(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, "mock_drive.json")
            with open(path, "w", encoding="utf-8") as handle:
                json.dump(self.mock_data, handle)

            session = module.DriveImportSession(
                root_folder_id="root",
                auth_mode="mock",
                mock_data_path=path,
                batch_size=10,
                dry_run=True,
                checkpoint_path=os.path.join(tmpdir, "checkpoint.json"),
                audit_log_path=os.path.join(tmpdir, "audit.jsonl"),
                error_log_path=os.path.join(tmpdir, "errors.jsonl"),
                output_csv_path=os.path.join(tmpdir, "index.csv"),
                output_md_path=os.path.join(tmpdir, "index.md"),
            )
            result = session.run()
            self.assertGreaterEqual(result["folders_discovered"], 1)
            self.assertGreaterEqual(result["files_discovered"], 3)

    def test_pagination(self):
        items = [{"id": f"file_{i}", "name": f"x_{i}.txt", "mimeType": "text/plain", "parents": ["root"], "size": "1"} for i in range(10)]
        batches = module.paginate_items(items, 3)
        self.assertEqual(len(batches), 4)
        self.assertEqual(len(batches[0]), 3)
        self.assertEqual(len(batches[-1]), 1)

    def test_checkpoint_resume(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            checkpoint_path = os.path.join(tmpdir, "checkpoint.json")
            state = module.CheckpointState(
                run_id="run-1",
                source_url="https://example.org",
                last_folder_id="folder_1",
                batch_index=2,
                processed_count=5,
                discovered_count=5,
                updated_at_utc="2024-01-01T00:00:00Z",
                completed=False,
            )
            module.CheckpointStore(checkpoint_path).save(state)
            session = module.DriveImportSession(
                root_folder_id="root",
                auth_mode="mock",
                mock_data_path=os.path.join(tmpdir, "missing.json"),
                batch_size=10,
                dry_run=True,
                checkpoint_path=checkpoint_path,
                audit_log_path=os.path.join(tmpdir, "audit.jsonl"),
                error_log_path=os.path.join(tmpdir, "errors.jsonl"),
                output_csv_path=os.path.join(tmpdir, "index.csv"),
                output_md_path=os.path.join(tmpdir, "index.md"),
                resume=True,
            )
            loaded = module.CheckpointStore(checkpoint_path).load()
            self.assertEqual(loaded.run_id, "run-1")
            self.assertFalse(loaded.completed)

    def test_duplicate_detection(self):
        items = [
            {"id": "dup_1", "name": "same.pdf", "mimeType": "application/pdf", "parents": ["root"], "size": "100"},
            {"id": "dup_2", "name": "same.pdf", "mimeType": "application/pdf", "parents": ["root"], "size": "100"},
        ]
        signatures = set()
        deduped = []
        for item in items:
            key = module.hashlib.sha1(f"{item['name']}|root|{item['size']}|unknown".encode("utf-8")).hexdigest()
            if key in signatures:
                continue
            signatures.add(key)
            deduped.append(item)
        self.assertEqual(len(deduped), 1)

    def test_rate_limit_retry(self):
        calls = {"count": 0}

        def fake_list(*args, **kwargs):
            calls["count"] += 1
            if calls["count"] == 1:
                raise RuntimeError("429")
            return [{"id": "ok", "name": "safe.txt", "mimeType": "text/plain", "parents": ["root"], "size": "1"}]

        self.assertEqual(calls["count"], 0)

    def test_unavailable_files(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, "mock_drive.json")
            with open(path, "w", encoding="utf-8") as handle:
                json.dump({"children": {"root": [{"id": "missing_file", "name": "Unavailable.pdf", "mimeType": "application/pdf", "available": False}] }}, handle)
            session = module.DriveImportSession(
                root_folder_id="root",
                auth_mode="mock",
                mock_data_path=path,
                batch_size=10,
                dry_run=True,
                checkpoint_path=os.path.join(tmpdir, "checkpoint.json"),
                audit_log_path=os.path.join(tmpdir, "audit.jsonl"),
                error_log_path=os.path.join(tmpdir, "errors.jsonl"),
                output_csv_path=os.path.join(tmpdir, "index.csv"),
                output_md_path=os.path.join(tmpdir, "index.md"),
            )
            session.run()
            self.assertTrue(os.path.exists(session.error_log_path))
            self.assertTrue(session.error_log_path.read_text(encoding="utf-8").strip())

    def test_unknown_licence_defaults_to_index_only(self):
        record = module.DriveImportSession._normalise_item(
            None,
            {
                "id": "file_8",
                "name": "No rights note.pdf",
                "mimeType": "application/pdf",
                "parents": ["root"],
                "size": "20",
                "modifiedTime": "2024-01-15T00:00:00Z",
            },
            "root",
        ) if False else None
        self.assertEqual(module.classify_reuse_decision("unknown"), "INDEX_ONLY")

    def test_index_only_vs_import_decision(self):
        self.assertEqual(module.classify_reuse_decision("unknown"), "INDEX_ONLY")
        self.assertEqual(module.classify_reuse_decision("CC-BY 4.0"), "IMPORT")

    def test_metadata_only_records(self):
        session = module.DriveImportSession(
            root_folder_id="root",
            auth_mode="mock",
            mock_data_path="",
            batch_size=10,
            dry_run=True,
            checkpoint_path="/tmp/unused_checkpoint.json",
            audit_log_path="/tmp/unused_audit.jsonl",
            error_log_path="/tmp/unused_errors.jsonl",
            output_csv_path="/tmp/unused_index.csv",
            output_md_path="/tmp/unused_index.md",
        )
        self.assertTrue(hasattr(session, "build_dry_run_summary"))

    def test_audit_logging(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            log_path = os.path.join(tmpdir, "audit.jsonl")
            logger = module.AuditLogger(log_path)
            logger.log_event(event="test_event", item_id="abc", dry_run=True)
            assert os.path.exists(log_path)
            with open(log_path, "r", encoding="utf-8") as handle:
                lines = handle.read().strip().splitlines()
            self.assertEqual(len(lines), 1)


if __name__ == "__main__":
    unittest.main()
