import csv
import tempfile
import unittest
from pathlib import Path

from scripts.reddit_corpus_census import audit, canonicalise

ROOT = Path(__file__).resolve().parents[1]
HISTORICAL_REDDIT = ROOT / "references" / "community" / "reddit-uri-index.csv"


class RedditCorpusCensusTests(unittest.TestCase):
    def test_candidate_post(self):
        result = canonicalise("https://www.reddit.com/r/NeuronsToNirvana/comments/abc123/example/?utm_source=x")
        self.assertEqual(result["status"], "candidate")
        self.assertEqual(result["post_id"], "abc123")
        self.assertEqual(result["canonical_url"], "https://www.reddit.com/r/NeuronsToNirvana/comments/abc123/example/")

    def test_annotation_row_is_not_independent_post(self):
        result = canonicalise("https://www.reddit.com/r/NeuronsToNirvana/comments/abc123/example/,HIERATIC,What")
        self.assertEqual(result["status"], "annotation_derived")
        self.assertEqual(result["annotation"], "HIERATIC,What")
        self.assertEqual(result["post_id"], "abc123")

    def test_qmm_composite_annotation_is_not_independent_post(self):
        result = canonicalise("https://www.reddit.com/r/NeuronsToNirvana/comments/abc123/example/,QMM,What")
        self.assertEqual(result["status"], "annotation_derived")
        self.assertEqual(result["annotation"], "QMM,What")
        self.assertEqual(result["post_id"], "abc123")

    def test_subreddit_root_and_malformed(self):
        root = canonicalise("https://www.reddit.com/r/NeuronsToNirvana")
        bad = canonicalise("https://example.com/r/test/comments/abc/title")
        self.assertEqual(root["status"], "non_post_subreddit")
        self.assertEqual(bad["status"], "malformed")

    def test_audit_counts_duplicates(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "sample.csv"
            with path.open("w", encoding="utf-8", newline="") as handle:
                writer = csv.writer(handle)
                writer.writerow(["reddit_url"])
                writer.writerow(["https://www.reddit.com/r/Test/comments/abc/title"])
                writer.writerow(["https://www.reddit.com/r/Test/comments/abc/title/,Original"])
                writer.writerow(["https://old.reddit.com/r/Test/comments/def/other?utm_source=x"])
                writer.writerow(["not-a-url"])
            report = audit(path)
        self.assertEqual(report["schema"], "akashicnet.reddit.corpus-census.v0.2")
        self.assertEqual(report["total_rows"], 4)
        self.assertEqual(report["post_rows"], 3)
        self.assertEqual(report["unique_post_ids"], 2)
        self.assertEqual(report["duplicate_post_id_rows"], 1)
        self.assertEqual(report["status_counts"]["annotation_derived"], 1)
        self.assertEqual(report["status_counts"]["malformed"], 1)
        self.assertEqual(report["unique_post_ids_by_subreddit"], {"Test": 2})

    def test_historical_archive_exact_structural_denominators(self):
        report = audit(HISTORICAL_REDDIT)
        self.assertEqual(report["total_rows"], 9401)
        self.assertEqual(report["post_rows"], 9400)
        self.assertEqual(report["status_counts"]["annotation_derived"], 2042)
        self.assertEqual(report["status_counts"]["candidate"], 7358)
        self.assertEqual(report["status_counts"]["non_post_subreddit"], 1)
        self.assertEqual(report["unique_post_ids"], 7356)
        self.assertEqual(report["unique_canonical_urls"], 7356)
        self.assertEqual(report["duplicate_post_id_rows"], 2044)
        self.assertEqual(report["duplicate_canonical_url_rows"], 2044)
        self.assertEqual(report["subreddits"]["NeuronsToNirvana"], 9341)
        self.assertEqual(report["subreddits"]["TribalGathering"], 57)
        self.assertEqual(report["subreddits"]["microdosing"], 2)
        self.assertEqual(
            report["unique_post_ids_by_subreddit"],
            {"microdosing": 1, "NeuronsToNirvana": 7298, "TribalGathering": 57},
        )


if __name__ == "__main__":
    unittest.main()
