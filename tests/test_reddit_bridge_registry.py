import unittest

from tools.reddit_bridge.registry import load_registry


class RedditBridgeRegistryTests(unittest.TestCase):
    def test_registry_contains_required_read_only_subreddits(self):
        sources = load_registry()
        by_subreddit = {source.subreddit: source for source in sources}
        self.assertEqual(
            {"NeuronsToNirvana", "TribalGathering", "microdosing", "microDJPanPSYchic"},
            set(by_subreddit),
        )
        self.assertTrue(all(source.access_mode == "read_only" for source in sources))
        self.assertTrue(all(source.platform == "reddit" for source in sources))
        self.assertTrue(all(source.kind == "subreddit" for source in sources))


if __name__ == "__main__":
    unittest.main()
