import json
import subprocess
import tempfile
import unittest
from pathlib import Path


class RedditBridgeCliTests(unittest.TestCase):
    def test_validate_registry_cli(self):
        result = subprocess.run(
            ["python3", "tools/reddit_bridge/cli.py", "validate-registry"],
            check=True,
            capture_output=True,
            text=True,
        )
        payload = json.loads(result.stdout)
        self.assertTrue(payload["valid"])
        self.assertTrue(payload["read_only"])

    def test_ingest_fixture_writes_local_artifacts_only_when_requested(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            output_jsonl = Path(tmpdir) / "records.jsonl"
            output_dedupe = Path(tmpdir) / "dedupe.csv"
            output_lineage = Path(tmpdir) / "lineage.csv"
            result = subprocess.run(
                [
                    "python3", "tools/reddit_bridge/cli.py", "ingest",
                    "--fixture", "tools/reddit_bridge/fixtures/sample_listing.json",
                    "--source", "all",
                    "--write-records",
                    "--output-jsonl", str(output_jsonl),
                    "--output-dedupe", str(output_dedupe),
                    "--output-lineage", str(output_lineage),
                ],
                check=True,
                capture_output=True,
                text=True,
            )
            payload = json.loads(result.stdout)
            self.assertTrue(payload["read_only"])
            self.assertTrue(output_jsonl.exists())
            self.assertTrue(output_dedupe.exists())
            self.assertTrue(output_lineage.exists())


if __name__ == "__main__":
    unittest.main()
