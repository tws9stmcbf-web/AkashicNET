import unittest

from tools.reddit_bridge.canonicalize import extract_post_id, normalize_reddit_url, post_identity


class RedditBridgeCanonicalizeTests(unittest.TestCase):
    def test_extracts_post_id(self):
        self.assertEqual(extract_post_id("https://www.reddit.com/r/x/comments/abc123/title/"), "abc123")

    def test_normalizes_host_and_strips_tracking(self):
        url = "https://old.reddit.com/r/microdosing/comments/plrxca/faq/?utm_source=chatgpt.com&share_id=abc"
        self.assertEqual(
            normalize_reddit_url(url, "microdosing"),
            "https://www.reddit.com/r/microdosing/comments/plrxca/faq/",
        )

    def test_full_url_subreddit_is_not_overridden_by_registry(self):
        url = "https://old.reddit.com/r/TribalGathering/comments/abc123/example/?utm_source=test"
        self.assertEqual(
            normalize_reddit_url(url, "NeuronsToNirvana"),
            "https://www.reddit.com/r/TribalGathering/comments/abc123/example/",
        )

    def test_registry_resolves_relative_permalink_without_subreddit(self):
        self.assertEqual(
            normalize_reddit_url("/comments/abc123/example/", "NeuronsToNirvana"),
            "https://www.reddit.com/r/NeuronsToNirvana/comments/abc123/example/",
        )

    def test_post_identity_requires_post_url(self):
        with self.assertRaises(ValueError):
            post_identity("https://www.reddit.com/r/microdosing/", "microdosing")


if __name__ == "__main__":
    unittest.main()
