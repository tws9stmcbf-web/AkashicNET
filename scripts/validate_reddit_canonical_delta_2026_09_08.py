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

REQUIRED_FALSE_GATES = {
    "reddit_api_called",
    "reddit_api_verification",
    "credentials_used",
    "reddit_api_approved_enabled",
    "crawled_or_paginated",
    "permanent_availability_verified",
    "authorship_verified",
    "rights_promoted",
    "scientific_evidence_promoted",
    "truth_inference",
    "public_count_promoted",
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


def validate_record(record: dict[str, object]) -> tuple[str, str]:
    fields = set(record)
    if fields != ALLOWED_RECORD_FIELDS:
        missing = sorted(ALLOWED_RECORD_FIELDS - fields)
        unexpected = sorted(fields - ALLOWED_RECORD_FIELDS)
        raise ValueError(
            f"record fields must exactly match allow-list: missing={missing} "
            f"unexpected={unexpected}"
        )

    post_id = str(record["reddit_post_id"])
    canonical_url = str(record["canonical_url"])
    try:
        normalized_url = normalize_permalink(canonical_url)
    except (ValueError, IndexError) as exc:
        raise ValueError("invalid Reddit permalink") from exc
    if normalized_url != canonical_url:
        raise ValueError("Reddit permalink must be canonical")

    url_post_id = canonical_url.split("/comments/", 1)[1].split("/", 1)[0]
    if url_post_id != post_id:
        raise ValueError("Reddit permalink post ID does not match reddit_post_id")

    return post_id, canonical_url


def main() -> int:
    delta = json.loads(DELTA_PATH.read_text(encoding="utf-8"))
    records = delta["records"]

    if delta["schema"] != "akashicnet.reddit.canonical-delta-import.v0.2":
        raise SystemExit(f"unexpected schema: {delta['schema']}")
    gates = delta.get("gates", {})
    for gate in sorted(REQUIRED_FALSE_GATES):
        if gates.get(gate) is not False:
            raise SystemExit(f"{gate} gate must be false")
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
        try:
            post_id, canonical_url = validate_record(record)
        except ValueError:
            rejected.append(str(record.get("reddit_post_id", "<missing>")))
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
