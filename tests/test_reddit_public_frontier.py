import tempfile
import unittest
from pathlib import Path

from scripts.reddit_public_frontier import classify_frontier, load_known_ids, parse_listing


class RedditPublicFrontierTests(unittest.TestCase):
    def test_parse_listing_keeps_only_target_subreddit_and_deduplicates(self):
        html = """
        <shreddit-post id="t3_new123" permalink="/r/NeuronsToNirvana/comments/new123/example/"></shreddit-post>
        <a href="https://www.reddit.com/r/NeuronsToNirvana/comments/new123/example/">duplicate</a>
        <a href="/r/NeuronsToNirvana/comments/known456/example/">known</a>
        <a href="/r/other/comments/wrong999/example/">wrong subreddit</a>
        """
        posts = parse_listing(html, "NeuronsToNirvana")
        self.assertEqual([post.post_id for post in posts], ["new123", "known456"])

    def test_load_known_ids_reads_urls_and_manual_batch_ids(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "known.csv"
            path.write_text(
                "feed_rank,subreddit,reddit_post_id,canonical_url\n"
                "1,NeuronsToNirvana,manual123,https://www.reddit.com/r/NeuronsToNirvana/comments/manual123/\n"
                "https://www.reddit.com/r/NeuronsToNirvana/comments/index456/\n",
                encoding="utf-8",
            )
            self.assertEqual(load_known_ids([path]), {"manual123", "index456"})

    def test_classify_frontier_stops_at_consecutive_known_boundary(self):
        html = "".join(
            f'<a href="/r/NeuronsToNirvana/comments/{post_id}/x/">x</a>'
            for post_id in ("new1", "new2", "old1", "old2", "old3")
        )
        posts = parse_listing(html, "NeuronsToNirvana")
        result = classify_frontier(posts, {"old1", "old2", "old3"}, 3)
        self.assertTrue(result["boundary_reached"])
        self.assertEqual(result["boundary_first_id"], "old1")
        self.assertEqual(
            [item["reddit_post_id"] for item in result["new_candidates"]],
            ["new1", "new2"],
        )

    def test_interrupted_known_run_does_not_create_false_boundary(self):
        html = "".join(
            f'<a href="/r/NeuronsToNirvana/comments/{post_id}/x/">x</a>'
            for post_id in ("new1", "old1", "new2", "old2", "old3")
        )
        posts = parse_listing(html, "NeuronsToNirvana")
        result = classify_frontier(posts, {"old1", "old2", "old3"}, 3)
        self.assertFalse(result["boundary_reached"])


if __name__ == "__main__":
    unittest.main()
