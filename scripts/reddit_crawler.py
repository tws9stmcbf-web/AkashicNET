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


def normalize_post(
    child: dict[str, Any],
    retrieved_at: str,
    *,
    endpoint: str = "subreddit_listing",
) -> dict[str, Any]:
    """Historical ``akashicnet.reddit.post.v1`` schema — compatibility only.

    Sealed for backward compatibility with already-promoted v1 artifacts.
    No live crawl or reconciliation path calls this function; new API
    output must go through ``normalize_post_v2`` instead. Do not modify
    this function's output shape.
    """
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
            "endpoint": endpoint,
            "metadata_only": True,
        },
    }


_REMOVED_MARKERS = {"[deleted]", "[removed]"}


def normalize_post_v2(
    child: dict[str, Any],
    retrieved_at: str,
    *,
    endpoint: str = "subreddit_listing",
) -> dict[str, Any]:
    """Minimized schema for future API-derived records.

    Deliberately narrower than ``akashicnet.reddit.post.v1``: excludes
    engagement counters (score, num_comments, upvote_ratio) as well as post
    bodies, comments and usernames. Only fields justified by source
    identity, canonical linking, time, safety/routing, and provenance are
    retained. This function must never mutate or replace ``normalize_post``.
    """
    data = child.get("data", child)
    permalink = str(data.get("permalink") or "")
    return {
        "schema_version": "akashicnet.reddit.post.v2",
        "source": "reddit",
        "record_type": "post_metadata",
        "reddit_id": data.get("id"),
        "fullname": data.get("name"),
        "subreddit": data.get("subreddit"),
        "title": data.get("title"),
        "canonical_url": canonical_post_url(permalink) if permalink else None,
        "external_url": data.get("url_overridden_by_dest") or data.get("url"),
        "created_utc": data.get("created_utc"),
        "over_18": data.get("over_18"),
        "retrieved_at": retrieved_at,
        "provenance": {
            "api": "reddit-data-api",
            "endpoint": endpoint,
            "metadata_only": True,
        },
    }


def is_post_removed(data: dict[str, Any] | None) -> bool:
    """Best-effort detection that a post is deleted/removed upstream."""
    if not data:
        return True
    if data.get("removed_by_category"):
        return True
    if data.get("title") in _REMOVED_MARKERS:
        return True
    if data.get("is_self") and data.get("selftext") in _REMOVED_MARKERS:
        return True
    return False


def tombstone_record(
    reddit_id: str,
    checked_at: str,
    *,
    status: str = "removed",
    endpoint: str = "reconcile",
) -> dict[str, Any]:
    """Minimal non-content audit record for a deleted/unavailable post.

    Only ``reddit_id``, ``status`` and ``checked_at`` describe the post
    itself, plus ``source`` and a minimal reconciliation ``provenance``
    event. Every content field (title, canonical_url, external_url,
    subreddit, timestamps taken from the post, etc.) is dropped so that
    removed content is never retained after a validated refresh.
    """
    return {
        "schema_version": "akashicnet.reddit.post.v2",
        "source": "reddit",
        "record_type": "post_metadata_removed",
        "reddit_id": reddit_id,
        "status": status,
        "checked_at": checked_at,
        "provenance": {
            "api": "reddit-data-api",
            "endpoint": endpoint,
            "metadata_only": True,
        },
    }


def reconcile_post(client: Any, reddit_id: str) -> dict[str, Any]:
    """Refresh a single post and reconcile deletion state.

    If the API no longer returns the post, or marks it removed, the
    returned record is a minimal tombstone (see ``tombstone_record``)
    rather than a record retaining removed content.
    """
    normalized_id = normalize_post_id(reddit_id)
    payload, headers = client.get_json(
        "/api/info",
        params={"id": f"t3_{normalized_id}", "raw_json": 1},
    )
    # Reconciliation can issue one request per cached record. Honor Reddit's
    # response budget before the next record is requested. Offline tests
    # return no rate-limit headers, so they incur no delay.
    obey_rate_limit(headers, 0.0)
    children = payload.get("data", {}).get("children", [])
    checked_at = utc_now_iso()
    for child in children:
        data = child.get("data", child)
        if str(data.get("id") or "").lower() == normalized_id:
            if is_post_removed(data):
                return tombstone_record(normalized_id, checked_at, status="removed")
            return normalize_post_v2(child, checked_at, endpoint="reconcile")
    return tombstone_record(normalized_id, checked_at, status="unavailable")


def reconcile_records(client: Any, records: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
    """Reconcile a batch of cached records, tombstoning deleted ones.

    Records that lack a ``reddit_id`` are passed through unchanged. Among
    existing tombstones (``post_metadata_removed``), only confirmed
    ``status == "removed"`` records are passed through unchanged; records
    left as ``status == "unavailable"`` are retried, since transient
    unavailability must not be permanently frozen as if it were confirmed
    removal.
    """
    reconciled: list[dict[str, Any]] = []
    for record in records:
        reddit_id = record.get("reddit_id")
        if not reddit_id:
            reconciled.append(record)
            continue
        if record.get("record_type") == "post_metadata_removed" and record.get("status") == "removed":
            reconciled.append(record)
            continue
        reconciled.append(reconcile_post(client, str(reddit_id)))
    return reconciled


def reconcile_file(client: Any, path: Path) -> tuple[int, int]:
    """Reconcile an existing JSONL artifact in place, atomically.

    Reads every record from ``path``, refreshes it via ``reconcile_records``,
    and only replaces the original file once reconciliation of the *entire*
    batch has completed without error. If any record's refresh raises (for
    example an API failure partway through), the exception propagates
    before anything is written and the original file is left completely
    untouched — there is no partial rewrite.
    """
    if not path.exists():
        raise FileNotFoundError(f"Reconciliation input not found: {path}")

    records: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            records.append(json.loads(line))

    reconciled = reconcile_records(client, records)

    tmp = path.with_suffix(path.suffix + ".reconcile.tmp")
    with tmp.open("w", encoding="utf-8") as handle:
        for record in reconciled:
            handle.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")
    tmp.replace(path)

    changed = sum(1 for record in reconciled if record.get("record_type") == "post_metadata_removed")
    return len(reconciled), changed


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


def normalize_post_id(value: str) -> str:
    post_id = value.strip().lower()
    if post_id.startswith("t3_"):
        post_id = post_id[3:]
    if not post_id or any(ch not in "0123456789abcdefghijklmnopqrstuvwxyz" for ch in post_id):
        raise ValueError("Reddit post ID must contain only base-36 characters")
    return post_id


def fetch_post(client: OAuthClient, post_id: str) -> dict[str, Any]:
    """Fetch exactly one post through /api/info.

    Emits the minimized ``akashicnet.reddit.post.v2`` schema so newly
    fetched API artifacts never carry engagement counters. ``normalize_post``
    (v1) is intentionally not called here; it is retained only as the
    untouched historical compatibility function.
    """
    normalized_id = normalize_post_id(post_id)
    payload, _ = client.get_json(
        "/api/info",
        params={"id": f"t3_{normalized_id}", "raw_json": 1},
    )
    children = payload.get("data", {}).get("children", [])
    retrieved_at = utc_now_iso()
    for child in children:
        data = child.get("data", child)
        if str(data.get("id") or "").lower() == normalized_id:
            if is_post_removed(data):
                return tombstone_record(normalized_id, retrieved_at, status="removed", endpoint="post_info")
            return normalize_post_v2(child, retrieved_at, endpoint="post_info")
    raise RedditAPIError(
        f"Reddit API did not return post {normalized_id}; availability remains indeterminate"
    )


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
            child_data = child.get("data", child)
            if is_post_removed(child_data):
                reddit_id = str(child_data.get("id") or "")
                yield tombstone_record(reddit_id, retrieved_at, status="removed", endpoint="subreddit_listing"), next_cursor
            else:
                yield normalize_post_v2(child, retrieved_at), next_cursor
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

    for record, next_cursor in iter_subreddit_posts(
        client,
        subreddit,
        listing=listing,
        max_posts=max_posts,
        after=after,
        minimum_delay=minimum_delay,
    ):
        reddit_id = str(record.get("reddit_id") or "")
        if record.get("record_type") == "post_metadata_removed" and reddit_id:
            # A removal refresh must supersede cached metadata instead of
            # disappearing behind the generic duplicate filter.
            replace_exact_post_record(record, output_path)
            seen.add(reddit_id)
            written += 1
        elif reddit_id and reddit_id in seen:
            skipped += 1
        else:
            with output_path.open("a", encoding="utf-8") as handle:
                handle.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")
            if reddit_id:
                seen.add(reddit_id)
            written += 1
        write_checkpoint(checkpoint_path, subreddit=subreddit, after=next_cursor)

    return written, skipped


def replace_exact_post_record(record: dict[str, Any], output_path: Path) -> str:
    """Store a single exact-fetch record, replacing any prior entry for its id.

    Used for exact ``--post-id`` fetches (as opposed to listing/reconcile
    batch appends). If ``output_path`` does not exist, or contains no prior
    record for this ``reddit_id``, the record is stored/appended normally
    ("written"/"appended"). If a prior record for this ``reddit_id`` is
    already present (content or an earlier tombstone), every such record is
    dropped and replaced by exactly one copy of ``record`` — this is how an
    exact removed-post refresh atomically supersedes stale cached content
    rather than being discarded as a duplicate.

    The whole file is parsed before anything is written; if any existing
    line fails to parse, the exception propagates and the original file is
    left completely untouched. The final replacement (when a prior record
    existed) is written to a sibling temp file and atomically renamed over
    the original, so a failure partway through writing never leaves a
    partially-updated artifact.
    """
    reddit_id = str(record.get("reddit_id") or "")
    if not reddit_id:
        raise ValueError("record is missing reddit_id")

    if not output_path.exists():
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with output_path.open("w", encoding="utf-8") as handle:
            handle.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")
        return "written"

    existing_records: list[dict[str, Any]] = []
    matched = False
    with output_path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            parsed = json.loads(line)
            if str(parsed.get("reddit_id") or "") == reddit_id:
                matched = True
                continue
            existing_records.append(parsed)

    if not matched:
        with output_path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")
        return "appended"

    existing_records.append(record)
    tmp = output_path.with_suffix(output_path.suffix + ".exactfetch.tmp")
    with tmp.open("w", encoding="utf-8") as handle:
        for existing_record in existing_records:
            handle.write(json.dumps(existing_record, ensure_ascii=False, sort_keys=True) + "\n")
    tmp.replace(output_path)
    return "replaced"


def crawl_post(
    client: OAuthClient,
    post_id: str,
    output_path: Path,
) -> tuple[int, int]:
    record = fetch_post(client, post_id)
    reddit_id = str(record.get("reddit_id") or "")

    if record.get("record_type") == "post_metadata_removed" and reddit_id:
        replace_exact_post_record(record, output_path)
        return 1, 0

    seen = load_seen_ids(output_path)
    if reddit_id and reddit_id in seen:
        return 0, 1

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")
    return 1, 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("subreddit", nargs="?", default=None, help="Subreddit name without r/ (omit when using --reconcile)")
    parser.add_argument("--output", type=Path, default=Path("data/reddit/posts.jsonl"), help="Append-only JSONL output path")
    parser.add_argument("--checkpoint", type=Path, default=Path("data/reddit/checkpoint.json"), help="Pagination checkpoint path")
    parser.add_argument("--listing", choices=("new", "hot", "top", "controversial"), default="new")
    parser.add_argument("--max-posts", type=int, default=None, help="Maximum posts to inspect this run")
    parser.add_argument("--post-id", help="Fetch exactly one Reddit post ID through /api/info (accepts optional t3_ prefix)")
    parser.add_argument("--delay", type=float, default=1.1, help="Minimum seconds between listing requests")
    parser.add_argument("--user-agent", default=os.getenv("REDDIT_USER_AGENT", DEFAULT_USER_AGENT), help="Descriptive Reddit API User-Agent")
    parser.add_argument(
        "--reconcile",
        type=Path,
        default=None,
        help="Path to an existing JSONL artifact to refresh/reconcile in place; atomically replaces the file only after a complete successful reconciliation",
    )
    return parser


def main(argv: Iterable[str] | None = None) -> int:
    # Fail-closed approval gate: this must run before credentials are read
    # and before any client/network path (crawl, exact-post fetch, or
    # reconciliation) can execute. The comparison is an exact string match
    # against "true"; repository secrets being configured is never
    # sufficient by itself to enable access.
    if os.getenv("REDDIT_API_APPROVED") != "true":
        print(
            "Reddit access is on HOLD: REDDIT_API_APPROVED must be set to the exact string "
            "'true' (only after explicit approval) before this crawler will read credentials "
            "or contact Reddit.",
            file=sys.stderr,
        )
        return 3

    args = build_parser().parse_args(argv)
    client_id = os.getenv("REDDIT_CLIENT_ID")
    client_secret = os.getenv("REDDIT_CLIENT_SECRET")
    if not client_id or not client_secret:
        print("Missing REDDIT_CLIENT_ID / REDDIT_CLIENT_SECRET. Create an approved Reddit API application and export its OAuth credentials.", file=sys.stderr)
        return 2

    if args.reconcile is None:
        if not args.subreddit:
            print("subreddit is required unless --reconcile is used", file=sys.stderr)
            return 2
        if args.max_posts is not None and args.max_posts <= 0:
            print("--max-posts must be positive", file=sys.stderr)
            return 2
        if args.delay < 0:
            print("--delay must be non-negative", file=sys.stderr)
            return 2
        if args.post_id:
            try:
                normalize_post_id(args.post_id)
            except ValueError as exc:
                print(str(exc), file=sys.stderr)
                return 2

    client = OAuthClient(client_id, client_secret, user_agent=args.user_agent)

    if args.reconcile is not None:
        try:
            total, changed = reconcile_file(client, args.reconcile)
        except (RedditAPIError, ValueError, FileNotFoundError) as exc:
            print(str(exc), file=sys.stderr)
            return 1
        print(f"Reddit reconciliation complete: total={total} removed_or_unavailable={changed} output={args.reconcile}")
        return 0

    try:
        if args.post_id:
            written, skipped = crawl_post(client, args.post_id, args.output)
            operation = "exact-post fetch"
        else:
            written, skipped = crawl_subreddit(
                client,
                args.subreddit,
                args.output,
                args.checkpoint,
                listing=args.listing,
                max_posts=args.max_posts,
                minimum_delay=args.delay,
            )
            operation = "crawl"
    except (RedditAPIError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        return 1

    print(f"Reddit {operation} complete: wrote={written} duplicate_skips={skipped} output={args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
