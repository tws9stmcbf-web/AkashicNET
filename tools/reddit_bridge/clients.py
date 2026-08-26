from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List


class FixtureRedditReadOnlyClient:
    """Read-only test client that loads listing payloads from local JSON fixtures."""

    def __init__(self, fixture_path: str | Path) -> None:
        self.fixture_path = Path(fixture_path)

    def list_subreddit_posts(self, subreddit: str, listing: str = "new", limit: int = 25, after: str | None = None) -> List[Dict[str, Any]]:
        payload = json.loads(self.fixture_path.read_text(encoding="utf-8"))
        posts = payload.get(subreddit, payload.get("posts", []))
        return posts[:limit]

    def fetch_post(self, subreddit: str, post_id: str) -> Dict[str, Any]:
        for post in self.list_subreddit_posts(subreddit, limit=10_000):
            if post.get("id") == post_id:
                return post
        raise KeyError(f"Post not found in fixture: {subreddit}/{post_id}")
