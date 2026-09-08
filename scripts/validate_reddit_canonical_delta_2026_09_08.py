#!/usr/bin/env python3
"""Validate the manually verified Reddit canonical delta dated 2026-09-08.

This is a metadata-only, additive companion to the sealed
``reddit-canonical-delta-import-2026-09-02.json`` artifact. It does not call
Reddit, does not use credentials, does not enable ``REDDIT_API_APPROVED``,
and does not crawl or paginate. It independently checks the 10 manually
supplied candidate records against the canonical index (``reddit-uri-index.csv``
and the sealed 2026-09-02 delta) and against an explicit allow-list of fields,
then emits a checkpoint describing exactly what was already present, accepted,
rejected, or held.
"""
from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DELTA_PATH = ROOT / "references" / "community" / "reddit-canonical-delta-import-2026-09-08.json"
PRIOR_DELTA_PATH = ROOT / "references" / "community" / "reddit-canonical-delta-import-2026-09-02.json"
URI_INDEX_PATH = ROOT / "references" / "community" / "reddit-uri-index.csv"
CHECKPOINT_PATH = ROOT / "references" / "community" / "reddit-canonical-delta-import-2026-09-08-audit.json"

ALLOWED_RECORD_FIELDS = {
    "reddit_post_id",
    "canonical_url",
    "subreddit",
    "title",
    "created_utc",
    "availability_status",
    "retrieved_at_utc",
    "provenance",
    "import_status",
}

FORBIDDEN_FIELDS = {
    "author", "username", "user", "body", "selftext", "comments", "comment_count",
    "score", "upvote_ratio", "num_comments", "ups", "downs", "flair",
    "link_flair_text", "link_flair_template_id", "topic", "topics", "category",
    "categories", "moderation", "stickied", "locked", "is_self",
}


def load_canonical_post_ids() -> set[str]:
    post_ids: set[str] = set()
    with URI_INDEX_PATH.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.reader(handle)
        next(reader, None)
        for row in reader:
            if not row:
                continue
            raw = row[0]
            match = raw.split("/comments/", 1)
            if len(match) == 2:
                post_id = match[1].split("/", 1)[0].split(",", 1)[0]
                if post_id:
                    post_ids.add(post_id.lower())
    prior_delta = json.loads(PRIOR_DELTA_PATH.read_text(encoding="utf-8"))
    for record in prior_delta["records"]:
        post_ids.add(record["reddit_post_id"].lower())
    return post_ids


def normalize_permalink(url: str) -> str:
    # Strip any slug/query/fragment down to the bare /r/<sub>/comments/<id>/ form.
    parts = [p for p in url.split("/") if p]
    idx = parts.index("comments")
    subreddit = parts[idx - 1]
    post_id = parts[idx + 1]
    return f"https://www.reddit.com/r/{subreddit}/comments/{post_id}/"


def main() -> int:
    delta = json.loads(DELTA_PATH.read_text(encoding="utf-8"))
    records = delta["records"]

    if delta["schema"] != "akashicnet.reddit.canonical-delta-import.v0.2":
        raise SystemExit(f"unexpected schema: {delta['schema']}")
    if delta.get("gates", {}).get("reddit_api_called") is not False:
        raise SystemExit("reddit_api_called gate must be false")
    if delta.get("gates", {}).get("crawled_or_paginated") is not False:
        raise SystemExit("crawled_or_paginated gate must be false")
    if delta.get("gates", {}).get("public_count_promoted") is not False:
        raise SystemExit("public_count_promoted gate must be false")
    if delta.get("scope", {}).get("coverage") != "partial_manual":
        raise SystemExit("coverage must be marked partial_manual")

    canonical_post_ids = load_canonical_post_ids()

    already_present: list[str] = []
    accepted: list[str] = []
    rejected: list[str] = []
    held: list[str] = []

    seen_ids: set[str] = set()
    seen_urls: set[str] = set()
    observed_fields: set[str] = set()

    for record in records:
        fields = set(record)
        observed_fields |= fields
        post_id = record["reddit_post_id"]
        canonical_url = record["canonical_url"]

        invalid_fields = fields - ALLOWED_RECORD_FIELDS
        forbidden_present = fields & FORBIDDEN_FIELDS
        if invalid_fields or forbidden_present:
            rejected.append(post_id)
            continue
        if normalize_permalink(canonical_url) != canonical_url:
            rejected.append(post_id)
            continue
        if post_id in seen_ids or canonical_url in seen_urls:
            rejected.append(post_id)
            continue
        seen_ids.add(post_id)
        seen_urls.add(canonical_url)

        if post_id in canonical_post_ids:
            already_present.append(post_id)
            continue

        if record.get("import_status") == "ACCEPTED_PENDING_COUNT_MERGE":
            accepted.append(post_id)
        else:
            held.append(post_id)

    if observed_fields - ALLOWED_RECORD_FIELDS:
        raise SystemExit(f"unexpected fields present: {sorted(observed_fields - ALLOWED_RECORD_FIELDS)}")

    status_counts = Counter(record["availability_status"] for record in records)

    result = {
        "schema": "akashicnet.reddit.canonical-delta-import-2026-09-08.audit.v0.1",
        "source": "references/community/reddit-canonical-delta-import-2026-09-08.json",
        "status": "REDDIT_MANUAL_DELTA_2026_09_08_AUDITED",
        "candidates_reviewed": len(records),
        "already_present": sorted(already_present),
        "accepted": sorted(accepted),
        "rejected": sorted(rejected),
        "held": sorted(held),
        "unique_reddit_post_ids": len(seen_ids),
        "unique_canonical_urls": len(seen_urls),
        "availability_status_counts": dict(sorted(status_counts.items())),
        "record_fields": sorted(observed_fields),
        "coverage": "partial_manual",
        "public_count_promoted": False,
        "guardrails": {
            "reddit_api_called": False,
            "reddit_api_approved_enabled": False,
            "credentials_used": False,
            "crawled_or_paginated": False,
            "truth_inference": False,
            "rights_promotion": False,
            "scientific_evidence_promotion": False,
        },
    }

    if len(records) != 10:
        raise SystemExit("expected exactly 10 candidate records")
    if already_present or rejected or held:
        raise SystemExit(
            "unexpected disposition: "
            f"already_present={already_present} rejected={rejected} held={held}"
        )
    if len(accepted) != 10:
        raise SystemExit(f"expected all 10 candidates accepted, got {len(accepted)}")

    if CHECKPOINT_PATH.exists():
        checkpoint = json.loads(CHECKPOINT_PATH.read_text(encoding="utf-8"))
        if result != checkpoint:
            raise SystemExit("generated audit differs from checked-in checkpoint")

    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
