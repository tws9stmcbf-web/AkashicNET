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


class AkashicImporterLocalMockTests(unittest.TestCase):
    def test_mock_dataset_traversal_and_index_generation(self):
        mock_data = {
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
                ],
                "folder_1": [
                    {
                        "id": "file_2",
                        "name": "Consciousness Essay.pdf",
                        "mimeType": "application/pdf",
                        "parents": ["folder_1"],
                        "size": "245000",
                        "modifiedTime": "2024-01-13T13:00:00Z",
                        "owners": [{"displayName": "Archive Curator"}],
                    }
                ],
            },
        }

        with tempfile.TemporaryDirectory() as tmpdir:
            local_path = os.path.join(tmpdir, "mock_drive.json")
            with open(local_path, "w", encoding="utf-8") as handle:
                json.dump(mock_data, handle)

            session = module.DriveImportSession(
                root_folder_id="root",
                auth_mode="mock",
                mock_data_path=local_path,
                batch_size=10,
                dry_run=True,
                checkpoint_path=os.path.join(tmpdir, "checkpoint.json"),
                audit_log_path=os.path.join(tmpdir, "audit.jsonl"),
                error_log_path=os.path.join(tmpdir, "errors.jsonl"),
                output_csv_path=os.path.join(tmpdir, "index.csv"),
                output_md_path=os.path.join(tmpdir, "index.md"),
            )

            result = session.run()
            self.assertEqual(result["discovered_count"], 3)
            self.assertEqual(result["index_only_count"], 3)
            self.assertTrue(os.path.exists(result["output_csv"]))
            self.assertTrue(os.path.exists(result["output_md"]))
            self.assertTrue(any("Consciousness" in line for line in open(result["output_csv"], encoding="utf-8")))


if __name__ == "__main__":
    unittest.main()
