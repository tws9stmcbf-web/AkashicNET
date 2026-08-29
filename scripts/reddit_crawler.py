#!/usr/bin/env python3
"""AkashicNET Reddit metadata crawler.

OAuth-only, restartable crawler for public Reddit post metadata. By default it
stores no post bodies, comments, or usernames. Output is JSONL suitable for
later normalization into the AkashicNET unified index.
"""
from __future__ import annotations

import argparse
import base64
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Iterator

API_BASE = "https://oauth.reddit.com"
TOKEN_URL = "https://www.reddit.com/api/v1/access_token"
DEFAULT_USER_AGENT = "AkashicNET-reddit-crawler/0.1 (research metadata indexer)"


class RedditAPIError(RuntimeError):
    pass


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def canonical_post_url(permalink: str) -> str:
    path = permalink.split("?", 1)[0].rstrip("/") + "/"
    return "https://www.reddit.com" + path


def normalize_post(child: dict[str, Any], retrieved_at: str) -> dict[str, Any]:
    data = child.get("data", child)
    permalink = str(data.get("permalink") or "")
    return {
        "schema_version": "akashicnet.reddit.post.v1",
        "source": "reddit",
        "record_type": "post_metadata",
        "reddit_id": data.get("id"),
        "fullname": data.get("name"),
        "subreddit": data.get("subreddit"),
        "title": data.get("title"),
        "canonical_url": canonical_post_url(permalink) if permalink else None,
        "external_url": data.get("url_overridden_by_dest") or data.get("url"),
        "created_utc": data.get("created_utc"),
        "score": data.get("score"),
        "num_comments": data.get("num_comments"),
        "upvote_ratio": data.get("upvote_ratio"),
        "over_18": data.get("over_18"),
        "stickied": data.get("stickied"),
        "locked": data.get("locked"),
        "is_self": data.get("is_self"),
        "retrieved_at": retrieved_at,
        "provenance": {
            "api": "reddit-data-api",
            "endpoint": "subreddit_listing",
            "metadata_only": True,
        },
    }


@dataclass
class OAuthClient:
    client_id: str
    client_secret: str
    user_agent: str = DEFAULT_USER_AGENT
    timeout: int = 30
    _token: str | None = None
    _token_expiry: float = 0.0

    def _request(self, request: urllib.request.Request) -> tuple[Any, dict[str, str]]:
        try:
            with urllib.request.urlopen(request, timeout=self.timeout) as response:
                raw = response.read().decode("utf-8")
                headers = {k.lower(): v for k, v in response.headers.items()}
                return json.loads(raw), headers
        except urllib.error.HTTPError as exc:
            body = exc.read().decode("utf-8", errors="replace")
            raise RedditAPIError(f"Reddit API HTTP {exc.code}: {body[:500]}") from exc
        except urllib.error.URLError as exc:
            raise RedditAPIError(f"Reddit API connection error: {exc.reason}") from exc

    def access_token(self) -> str:
        if self._token and time.time() < self._token_expiry - 60:
            return self._token

        credentials = base64.b64encode(
            f"{self.client_id}:{self.client_secret}".encode("utf-8")
        ).decode("ascii")
        body = urllib.parse.urlencode({"grant_type": "client_credentials"}).encode("ascii")
        request = urllib.request.Request(
            TOKEN_URL,
            data=body,
            method="POST",
            headers={
                "Authorization": f"Basic {credentials}",
                "User-Agent": self.user_agent,
                "Content-Type": "application/x-www-form-urlencoded",
            },
        )
        payload, _ = self._request(request)
        token = payload.get("access_token")
        if not token:
            raise RedditAPIError(f"OAuth token response did not contain access_token: {payload}")
        self._token = str(token)
        self._token_expiry = time.time() + float(payload.get("expires_in", 3600))
        return self._token

    def get_json(self, path: str, params: dict[str, Any] | None = None) -> tuple[Any, dict[str, str]]:
        query = urllib.parse.urlencode(params or {})
        url = API_BASE + path + ("?" + query if query else "")
        request = urllib.request.Request(
            url,
            headers={
                "Authorization": f"Bearer {self.access_token()}",
                "User-Agent": self.user_agent,
                "Accept": "application/json",
            },
        )
        return self._request(request)


def obey_rate_limit(headers: dict[str, str], minimum_delay: float) -> None:
    delay = max(0.0, minimum_delay)
    try:
        remaining = float(headers.get("x-ratelimit-remaining", "nan"))
        reset = float(headers.get("x-ratelimit-reset", "0"))
        if remaining <= 1 and reset > delay:
            delay = reset + 1.0
    except ValueError:
        pass
    if delay:
        time.sleep(delay)


def iter_subreddit_posts(
    client: OAuthClient,
    subreddit: str,
    *,
    listing: str = "new",
    page_size: int = 100,
    max_posts: int | None = None,
    after: str | None = None,
    minimum_delay: float = 1.1,
) -> Iterator[tuple[dict[str, Any], str | None]]:
    emitted = 0
    cursor = after
    while True:
        remaining = None if max_posts is None else max_posts - emitted
        if remaining is not None and remaining <= 0:
            return
        limit = page_size if remaining is None else min(page_size, remaining)
        params: dict[str, Any] = {"limit": limit, "raw_json": 1}
        if cursor:
            params["after"] = cursor
        payload, headers = client.get_json(f"/r/{subreddit}/{listing}", params=params)
        data = payload.get("data", {})
        children = data.get("children", [])
        if not children:
            return
        retrieved_at = utc_now_iso()
        next_cursor = data.get("after")
        for child in children:
            yield normalize_post(child, retrieved_at), next_cursor
            emitted += 1
            if max_posts is not None and emitted >= max_posts:
                return
        if not next_cursor or next_cursor == cursor:
            return
        cursor = next_cursor
        obey_rate_limit(headers, minimum_delay)


def load_seen_ids(path: Path) -> set[str]:
    if not path.exists():
        return set()
    seen: set[str] = set()
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            try:
                record = json.loads(line)
            except json.JSONDecodeError:
                continue
            reddit_id = record.get("reddit_id")
            if reddit_id:
                seen.add(str(reddit_id))
    return seen


def read_checkpoint(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {}


def write_checkpoint(path: Path, *, subreddit: str, after: str | None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {"subreddit": subreddit, "after": after, "updated_at": utc_now_iso()}
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    tmp.replace(path)


def crawl_subreddit(
    client: OAuthClient,
    subreddit: str,
    output_path: Path,
    checkpoint_path: Path,
    *,
    listing: str,
    max_posts: int | None,
    minimum_delay: float,
) -> tuple[int, int]:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    seen = load_seen_ids(output_path)
    checkpoint = read_checkpoint(checkpoint_path)
    after = checkpoint.get("after") if checkpoint.get("subreddit") == subreddit else None
    written = 0
    skipped = 0

    with output_path.open("a", encoding="utf-8") as handle:
        for record, next_cursor in iter_subreddit_posts(
            client,
            subreddit,
            listing=listing,
            max_posts=max_posts,
            after=after,
            minimum_delay=minimum_delay,
        ):
            reddit_id = str(record.get("reddit_id") or "")
            if reddit_id and reddit_id in seen:
                skipped += 1
            else:
                handle.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")
                handle.flush()
                if reddit_id:
                    seen.add(reddit_id)
                written += 1
            write_checkpoint(checkpoint_path, subreddit=subreddit, after=next_cursor)

    return written, skipped


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("subreddit", help="Subreddit name without r/")
    parser.add_argument("--output", type=Path, default=Path("data/reddit/posts.jsonl"), help="Append-only JSONL output path")
    parser.add_argument("--checkpoint", type=Path, default=Path("data/reddit/checkpoint.json"), help="Pagination checkpoint path")
    parser.add_argument("--listing", choices=("new", "hot", "top", "controversial"), default="new")
    parser.add_argument("--max-posts", type=int, default=None, help="Maximum posts to inspect this run")
    parser.add_argument("--delay", type=float, default=1.1, help="Minimum seconds between listing requests")
    parser.add_argument("--user-agent", default=os.getenv("REDDIT_USER_AGENT", DEFAULT_USER_AGENT), help="Descriptive Reddit API User-Agent")
    return parser


def main(argv: Iterable[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    client_id = os.getenv("REDDIT_CLIENT_ID")
    client_secret = os.getenv("REDDIT_CLIENT_SECRET")
    if not client_id or not client_secret:
        print("Missing REDDIT_CLIENT_ID / REDDIT_CLIENT_SECRET. Create an approved Reddit API application and export its OAuth credentials.", file=sys.stderr)
        return 2
    if args.max_posts is not None and args.max_posts <= 0:
        print("--max-posts must be positive", file=sys.stderr)
        return 2
    if args.delay < 0:
        print("--delay must be non-negative", file=sys.stderr)
        return 2

    client = OAuthClient(client_id, client_secret, user_agent=args.user_agent)
    try:
        written, skipped = crawl_subreddit(
            client,
            args.subreddit,
            args.output,
            args.checkpoint,
            listing=args.listing,
            max_posts=args.max_posts,
            minimum_delay=args.delay,
        )
    except RedditAPIError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    print(f"Reddit crawl complete: wrote={written} duplicate_skips={skipped} output={args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
