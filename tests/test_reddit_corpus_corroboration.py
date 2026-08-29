import json
import tempfile
import unittest
from pathlib import Path

from scripts.reddit_corpus_corroboration import audit


class RedditCorpusCorroborationTests(unittest.TestCase):
    def test_corroboration_states(self):
        corpus = "reddit_url\n" + "\n".join([
            "https://www.reddit.com/r/x/comments/1000/a/",
            "https://www.reddit.com/r/x/comments/1001/b/",
            "https://www.reddit.com/r/x/comments/1002/c/",
            "https://www.reddit.com/r/x/comments/1003/d/",
            "https://www.reddit.com/r/x/comments/zzzzz/e/",
        ]) + "\n"
        seed = {
            "schema": "test",
            "source_type": "public_web_discovery",
            "records": [
                {"subreddit": "x", "post_id": "zzzzz"},
                {"subreddit": "x", "post_id": "abcde"},
            ],
        }
        with tempfile.TemporaryDirectory() as tmp:
            corpus_path = Path(tmp) / "corpus.csv"
            seed_path = Path(tmp) / "seed.json"
            corpus_path.write_text(corpus, encoding="utf-8")
            seed_path.write_text(json.dumps(seed), encoding="utf-8")
            report = audit(corpus_path, seed_path, min_run=4)
        self.assertEqual(report["historical_unique_structural_candidates"], 5)
        self.assertEqual(report["suspected_generated_by_sequence_filter"], 4)
        self.assertEqual(report["candidate_pool_after_sequence_filter"], 1)
        self.assertEqual(report["corroborated_candidates"], 1)
        self.assertEqual(report["uncorroborated_candidates"], 0)
        self.assertEqual(report["seed_records_not_in_historical_candidate_pool"], 1)


if __name__ == "__main__":
    unittest.main()
