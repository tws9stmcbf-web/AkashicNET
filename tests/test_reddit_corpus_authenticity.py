import tempfile
import unittest
from pathlib import Path

from scripts.reddit_corpus_authenticity import audit, consecutive_runs, parse_candidate


class RedditCorpusAuthenticityTests(unittest.TestCase):
    def test_parse_candidate(self):
        record = parse_candidate("https://www.reddit.com/r/NeuronsToNirvana/comments/abc123/example/")
        self.assertEqual(record["post_id"], "abc123")
        self.assertEqual(record["subreddit"], "NeuronsToNirvana")

    def test_annotation_is_excluded(self):
        self.assertIsNone(parse_candidate("https://www.reddit.com/r/x/comments/abc123/foo/,Research"))

    def test_consecutive_run(self):
        records = [parse_candidate(f"https://www.reddit.com/r/x/comments/{pid}/x/") for pid in ["1000", "1001", "1002", "1003", "2000"]]
        runs = consecutive_runs(records, min_run=4)
        self.assertEqual(len(runs), 1)
        self.assertEqual([r["post_id"] for r in runs[0]], ["1000", "1001", "1002", "1003"])

    def test_audit_sequence_filter(self):
        content = "reddit_url\n" + "\n".join(
            [f"https://www.reddit.com/r/x/comments/{pid}/x/" for pid in ["1000", "1001", "1002", "1003", "zzzzz"]]
        ) + "\n"
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "input.csv"
            path.write_text(content, encoding="utf-8")
            report = audit(path, min_run=4)
        self.assertEqual(report["unique_structural_candidates"], 5)
        self.assertEqual(report["suspected_generated_ids"], 4)
        self.assertEqual(report["remaining_candidates_after_sequence_filter"], 1)


if __name__ == "__main__":
    unittest.main()
