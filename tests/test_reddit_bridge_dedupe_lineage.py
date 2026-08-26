import unittest

from tools.reddit_bridge.bridge import build_records
from tools.reddit_bridge.models import RedditSource


class RedditBridgeDedupeLineageTests(unittest.TestCase):
    def setUp(self):
        self.source = RedditSource(
            source_id="reddit_neurons_to_nirvana",
            platform="reddit",
            kind="subreddit",
            subreddit="NeuronsToNirvana",
            canonical_url="https://www.reddit.com/r/NeuronsToNirvana/",
        )

    def test_duplicate_post_id_is_marked(self):
        records = build_records(self.source, [
            {"id": "abc123", "permalink": "/r/NeuronsToNirvana/comments/abc123/example/", "title": "Example", "created_utc": 1780000000},
            {"id": "abc123", "permalink": "https://old.reddit.com/r/NeuronsToNirvana/comments/abc123/example/?utm_source=x", "title": "Example", "created_utc": 1780000000},
        ])
        self.assertEqual(records[0].dedupe_status, "unique")
        self.assertEqual(records[1].dedupe_status, "duplicate_exact_post_id")
        self.assertEqual(records[1].duplicate_of, records[0].dedupe_key)

    def test_crosspost_lineage_is_preserved(self):
        records = build_records(self.source, [{
            "id": "child1",
            "permalink": "/r/NeuronsToNirvana/comments/child1/crosspost/",
            "title": "Crosspost",
            "created_utc": 1780000000,
            "crosspost_parent_list": [{"id": "root1", "subreddit": "TribalGathering", "permalink": "/r/TribalGathering/comments/root1/root/"}],
        }])
        self.assertEqual(records[0].crosspost_parent_id, "root1")
        self.assertEqual(records[0].crosspost_root_id, "root1")
        self.assertEqual(records[0].crosspost_chain, ["root1"])
        self.assertEqual(records[0].lineage_status, "official_crosspost")


if __name__ == "__main__":
    unittest.main()
