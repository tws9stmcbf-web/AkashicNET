#!/usr/bin/env python3
"""Audit a historical Reddit URI CSV without fetching Reddit content."""

from __future__ import annotations

import argparse
import csv
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from urllib.parse import urlparse

POST_RE = re.compile(r"^/r/([^/]+)/comments/([A-Za-z0-9]+)(?:/([^/,]+))?/?$")
ROOT_RE = re.compile(r"^/r/([^/]+)/?$")
REDDIT_HOSTS = {"reddit.com", "www.reddit.com", "old.reddit.com", "new.reddit.com", "m.reddit.com"}


def split_annotation(value: str) -> tuple[str, str | None]:
    text = value.strip().strip('"')
    marker = text.find(",")
    if marker == -1:
        return text, None
    return text[:marker], text[marker + 1 :].strip() or None


def canonicalise(value: str) -> dict:
    raw_url, annotation = split_annotation(value)
    if raw_url.startswith("http://"):
        raw_url = "https://" + raw_url[7:]
    if not raw_url.startswith("http"):
        raw_url = "https://" + raw_url.lstrip("/")

    parsed = urlparse(raw_url)
    if parsed.netloc.lower() not in REDDIT_HOSTS:
        return {"status": "malformed", "reason": "unsupported_host", "raw": value}

    path = re.sub(r"/+", "/", parsed.path)
    root = ROOT_RE.match(path)
    if root:
        subreddit = root.group(1)
        return {
            "status": "non_post_subreddit",
            "subreddit": subreddit,
            "canonical_url": f"https://www.reddit.com/r/{subreddit}/",
            "annotation": annotation,
            "raw": value,
        }

    match = POST_RE.match(path)
    if not match:
        return {"status": "malformed", "reason": "not_reddit_post_path", "raw": value, "annotation": annotation}

    subreddit, post_id, slug = match.groups()
    canonical = f"https://www.reddit.com/r/{subreddit}/comments/{post_id}/"
    if slug:
        canonical += f"{slug}/"
    return {
        "status": "annotation_derived" if annotation else "candidate",
        "subreddit": subreddit,
        "post_id": post_id.lower(),
        "canonical_url": canonical,
        "annotation": annotation,
        "raw": value,
    }


def audit(path: Path) -> dict:
    records: list[dict] = []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.reader(handle)
        header = next(reader, None)
        for row_number, row in enumerate(reader, start=2):
            if not row:
                continue
            result = canonicalise(row[0])
            result["row"] = row_number
            records.append(result)

    status_counts = Counter(r["status"] for r in records)
    post_records = [r for r in records if r["status"] in {"candidate", "annotation_derived"}]
    id_counts = Counter((r["subreddit"].casefold(), r["post_id"]) for r in post_records)
    url_counts = Counter(r["canonical_url"] for r in post_records)
    unique_ids = len(id_counts)
    unique_urls = len(url_counts)

    display_names: dict[str, str] = {}
    unique_ids_by_subreddit: dict[str, set[str]] = defaultdict(set)
    for record in post_records:
        folded = record["subreddit"].casefold()
        display_names.setdefault(folded, record["subreddit"])
        unique_ids_by_subreddit[folded].add(record["post_id"])

    unique_post_ids_by_subreddit = {
        display_names[key]: len(values)
        for key, values in sorted(unique_ids_by_subreddit.items(), key=lambda item: display_names[item[0]].casefold())
    }

    return {
        "schema": "akashicnet.reddit.corpus-census.v0.2",
        "input": str(path),
        "header": header,
        "total_rows": len(records),
        "status_counts": dict(sorted(status_counts.items())),
        "post_rows": len(post_records),
        "unique_post_ids": unique_ids,
        "unique_canonical_urls": unique_urls,
        "duplicate_post_id_rows": sum(count - 1 for count in id_counts.values() if count > 1),
        "duplicate_canonical_url_rows": sum(count - 1 for count in url_counts.values() if count > 1),
        "subreddits": dict(sorted(Counter(r["subreddit"] for r in post_records).items())),
        "unique_post_ids_by_subreddit": unique_post_ids_by_subreddit,
        "notes": [
            "candidate means structurally valid only; it is not proof that the Reddit post exists",
            "annotation_derived rows contain comma-suffixed historical labels and are not independent Reddit posts",
            "unique counts are structural archive counts, not Reddit API verification",
            "no usernames, post bodies, or comments are fetched or stored",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv_path", type=Path)
    parser.add_argument("--json-out", type=Path)
    args = parser.parse_args()
    report = audit(args.csv_path)
    text = json.dumps(report, indent=2, sort_keys=True)
    print(text)
    if args.json_out:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(text + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
