#!/usr/bin/env python3
"""Read-only public Reddit frontier check for AkashicNET.

This intentionally avoids Reddit OAuth and stores only post identifiers and
canonical URLs.  It compares the live public ``new`` page with the historical
URI index and review-only manual batches, then stops once a consecutive known
boundary is established.
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
import urllib.error
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from typing import Iterable


DEFAULT_URL = "https://www.reddit.com/r/NeuronsToNirvana/new/"
DEFAULT_USER_AGENT = "AkashicNET-public-frontier/1.0 (metadata-only integrity check)"
POST_ID_RE = re.compile(r"^[a-z0-9]+$", re.IGNORECASE)
COMMENTS_RE = re.compile(
    r"https?://(?:www\.|old\.|new\.)?reddit\.com/r/([^/]+)/comments/([a-z0-9]+)/?",
    re.IGNORECASE,
)


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def canonical_url(subreddit: str, post_id: str) -> str:
    return f"https://www.reddit.com/r/{subreddit}/comments/{post_id.lower()}/"


@dataclass(frozen=True)
class PostRef:
    subreddit: str
    post_id: str

    @property
    def url(self) -> str:
        return canonical_url(self.subreddit, self.post_id)


class PublicListingParser(HTMLParser):
    def __init__(self, subreddit: str) -> None:
        super().__init__(convert_charrefs=True)
        self.subreddit = subreddit
        self.posts: list[PostRef] = []
        self._seen: set[str] = set()

    def _add(self, subreddit: str, post_id: str) -> None:
        if subreddit.casefold() != self.subreddit.casefold():
            return
        post_id = post_id.lower()
        if not POST_ID_RE.fullmatch(post_id) or post_id in self._seen:
            return
        self._seen.add(post_id)
        self.posts.append(PostRef(self.subreddit, post_id))

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = {key: value or "" for key, value in attrs}
        if tag.casefold() == "shreddit-post":
            fullname = values.get("id", "")
            permalink = values.get("permalink", "")
            if fullname.startswith("t3_"):
                self._add(self.subreddit, fullname[3:])
            match = COMMENTS_RE.search("https://www.reddit.com" + permalink)
            if match:
                self._add(match.group(1), match.group(2))
        if tag.casefold() == "a":
            href = values.get("href", "")
            if href.startswith("/"):
                href = "https://www.reddit.com" + href
            match = COMMENTS_RE.search(href)
            if match:
                self._add(match.group(1), match.group(2))


def parse_listing(html: str, subreddit: str) -> list[PostRef]:
    parser = PublicListingParser(subreddit)
    parser.feed(html)
    return parser.posts


def fetch_listing(url: str, user_agent: str, timeout: int) -> str:
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": user_agent,
            "Accept": "text/html,application/xhtml+xml",
            "Accept-Language": "en-US,en;q=0.8",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            content_type = response.headers.get("content-type", "")
            if response.status != 200:
                raise RuntimeError(f"public Reddit listing returned HTTP {response.status}")
            if "html" not in content_type.casefold():
                raise RuntimeError(f"unexpected Reddit content type: {content_type or 'missing'}")
            return response.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as exc:
        raise RuntimeError(f"public Reddit listing returned HTTP {exc.code}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"public Reddit listing connection failed: {exc.reason}") from exc


def load_known_ids(paths: Iterable[Path]) -> set[str]:
    known: set[str] = set()
    for path in paths:
        if not path.exists():
            continue
        with path.open("r", encoding="utf-8", newline="") as handle:
            for row in csv.reader(handle):
                for value in row:
                    value = value.strip()
                    match = COMMENTS_RE.search(value)
                    if match:
                        known.add(match.group(2).lower())
                if len(row) >= 3 and POST_ID_RE.fullmatch(row[2].strip()):
                    known.add(row[2].strip().lower())
    return known


def classify_frontier(posts: list[PostRef], known: set[str], min_boundary: int) -> dict:
    new_posts: list[PostRef] = []
    boundary: list[PostRef] = []
    for post in posts:
        if post.post_id in known:
            boundary.append(post)
            if len(boundary) >= min_boundary:
                break
        else:
            new_posts.extend(boundary)
            boundary = []
            new_posts.append(post)

    reached = len(boundary) >= min_boundary
    return {
        "boundary_reached": reached,
        "boundary_count": len(boundary),
        "boundary_first_id": boundary[0].post_id if boundary else None,
        "new_candidates": [
            {"reddit_post_id": post.post_id, "canonical_url": post.url, "disposition": "HOLD"}
            for post in new_posts
        ],
    }


def write_report(path: Path, report: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_summary(path: Path, report: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    candidates = report.get("new_candidates", [])
    lines = [
        "# Reddit public frontier checkpoint",
        "",
        f"- Status: **{report['status']}**",
        f"- Public rows observed: **{report.get('rows_observed', 0)}**",
        f"- New HOLD candidates: **{len(candidates)}**",
        f"- Consecutive known boundary: **{report.get('boundary_count', 0)}**",
        "- Canonical imports: **0**",
        "- Usernames, bodies and comments stored: **none**",
    ]
    if candidates:
        lines.extend(["", "## Review-only candidates", ""])
        lines.extend(f"- `{item['reddit_post_id']}` — {item['canonical_url']}" for item in candidates)
    if report.get("error"):
        lines.extend(["", f"Error: {report['error']}"])
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--subreddit", default="NeuronsToNirvana")
    parser.add_argument("--url", default=DEFAULT_URL)
    parser.add_argument("--known", action="append", type=Path, default=[])
    parser.add_argument("--known-glob", action="append", default=[])
    parser.add_argument("--min-boundary", type=int, default=5)
    parser.add_argument("--timeout", type=int, default=30)
    parser.add_argument("--user-agent", default=DEFAULT_USER_AGENT)
    parser.add_argument("--json-out", type=Path, required=True)
    parser.add_argument("--summary-out", type=Path, required=True)
    return parser


def main(argv: Iterable[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    known_paths = list(args.known)
    for pattern in args.known_glob:
        known_paths.extend(sorted(Path().glob(pattern)))

    report = {
        "schema_version": "akashicnet.reddit.public-frontier.v1",
        "observed_at": utc_now_iso(),
        "source": args.url,
        "metadata_only": True,
        "canonical_imports": 0,
        "status": "ERROR",
        "rows_observed": 0,
        "boundary_count": 0,
        "new_candidates": [],
    }
    try:
        if args.min_boundary <= 0:
            raise RuntimeError("--min-boundary must be positive")
        html = fetch_listing(args.url, args.user_agent, args.timeout)
        posts = parse_listing(html, args.subreddit)
        if not posts:
            raise RuntimeError("no public subreddit post identifiers found; refusing empty success")
        known = load_known_ids(known_paths)
        if not known:
            raise RuntimeError("known-record set is empty; refusing unbounded classification")
        result = classify_frontier(posts, known, args.min_boundary)
        report.update(result)
        report["rows_observed"] = len(posts)
        report["known_ids_loaded"] = len(known)
        report["status"] = "PASS" if result["boundary_reached"] else "INCOMPLETE_BOUNDARY"
        if not result["boundary_reached"]:
            report["error"] = "validated consecutive known-record boundary was not reached"
    except RuntimeError as exc:
        report["error"] = str(exc)

    write_report(args.json_out, report)
    write_summary(args.summary_out, report)
    print(json.dumps(report, sort_keys=True))
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
