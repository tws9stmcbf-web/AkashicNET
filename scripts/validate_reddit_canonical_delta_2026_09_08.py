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
import hashlib
import json
import re
from datetime import datetime
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

REDDIT_POST_ID_RE = re.compile(r"^[0-9a-z]+$")
CREATED_UTC_RE = re.compile(
    r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z$"
)
RETRIEVED_AT_UTC_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
EXPECTED_SUBREDDIT = "NeuronsToNirvana"
# Historical public checkpoint declared by this manual delta, not live counts.
EXPECTED_PUBLIC_COUNTS = {"source_rows": 9502, "unified_index_records": 12159}
REQUIRED_TRUE_GATES = {
    "direct_public_accessibility_at_observation",
    "historical_index_absence",
    "unique_reddit_post_ids",
    "unique_canonical_urls",
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


def normalize_reddit_post_id(post_id: str) -> str:
    normalized = post_id.lower()
    if normalized.startswith("t3_"):
        normalized = normalized[3:]
    return normalized


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
                    post_ids.add(normalize_reddit_post_id(post_id))
    prior_delta = json.loads(PRIOR_DELTA_PATH.read_text(encoding="utf-8"))
    for record in prior_delta["records"]:
        post_ids.add(normalize_reddit_post_id(record["reddit_post_id"]))
    return post_ids


def permalink_identity(url: str) -> tuple[str, str]:
    parts = [p for p in url.split("/") if p]
    idx = parts.index("comments")
    return parts[idx - 1], parts[idx + 1]


def normalize_permalink(url: str) -> str:
    # Strip any slug/query/fragment down to the bare /r/<sub>/comments/<id>/ form.
    subreddit, post_id = permalink_identity(url)
    return f"https://www.reddit.com/r/{subreddit}/comments/{post_id}/"


def validate_record(
    record: dict[str, object], expected_subreddit: str
) -> tuple[str, str]:
    fields = set(record)
    if fields != ALLOWED_RECORD_FIELDS:
        missing = sorted(ALLOWED_RECORD_FIELDS - fields)
        unexpected = sorted(fields - ALLOWED_RECORD_FIELDS)
        raise ValueError(
            f"record fields must exactly match allow-list: missing={missing} "
            f"unexpected={unexpected}"
        )

    post_id = record["reddit_post_id"]
    if not isinstance(post_id, str) or not REDDIT_POST_ID_RE.fullmatch(post_id):
        raise ValueError("reddit_post_id must be a non-empty lowercase base-36 string")
    if normalize_reddit_post_id(post_id) != post_id:
        raise ValueError("reddit_post_id must be lowercase and unprefixed")

    canonical_url = record["canonical_url"]
    if not isinstance(canonical_url, str):
        raise ValueError("canonical_url must be a string")
    try:
        url_subreddit, url_post_id = permalink_identity(canonical_url)
        normalized_url = normalize_permalink(canonical_url)
    except (ValueError, IndexError) as exc:
        raise ValueError("invalid Reddit permalink") from exc
    if normalized_url != canonical_url:
        raise ValueError("Reddit permalink must be canonical")
    if url_post_id != post_id:
        raise ValueError("Reddit permalink post ID does not match reddit_post_id")

    record_subreddit = record["subreddit"]
    if not isinstance(record_subreddit, str):
        raise ValueError("record subreddit must be a string")
    if url_subreddit != record_subreddit:
        raise ValueError("Reddit permalink subreddit does not match record subreddit")
    if record_subreddit != expected_subreddit:
        raise ValueError("record subreddit does not match declared scope")
    if record_subreddit != EXPECTED_SUBREDDIT:
        raise ValueError(f"record subreddit must be {EXPECTED_SUBREDDIT}")

    title = record["title"]
    if not isinstance(title, str) or not title.strip():
        raise ValueError("title must be a non-empty string")

    created_utc = record["created_utc"]
    if not isinstance(created_utc, str) or not CREATED_UTC_RE.fullmatch(created_utc):
        raise ValueError("created_utc must be an ISO 8601 UTC timestamp with milliseconds")
    try:
        created_at = datetime.strptime(created_utc, "%Y-%m-%dT%H:%M:%S.%fZ")
    except ValueError as exc:
        raise ValueError("created_utc must be a valid UTC timestamp") from exc

    retrieved_at_utc = record["retrieved_at_utc"]
    if (
        not isinstance(retrieved_at_utc, str)
        or not RETRIEVED_AT_UTC_RE.fullmatch(retrieved_at_utc)
    ):
        raise ValueError("retrieved_at_utc must be an ISO 8601 date")
    try:
        retrieved_at = datetime.strptime(retrieved_at_utc, "%Y-%m-%d")
    except ValueError as exc:
        raise ValueError("retrieved_at_utc must be a valid date") from exc
    if created_at.date() > retrieved_at.date():
        raise ValueError("created_utc must not be later than retrieved_at_utc")

    fixed_values = {
        "availability_status": "publicly_accessible",
        "provenance": "manual_observation_of_public_subreddit_listing",
        "import_status": "ACCEPTED_PENDING_COUNT_MERGE",
    }
    for field, expected in fixed_values.items():
        if record[field] != expected:
            raise ValueError(f"{field} must be {expected!r}")

    return post_id, canonical_url


def validate_scope_counts(
    scope: dict[str, object],
    *,
    candidates_reviewed: int,
    already_present: int,
    accepted: int,
    rejected: int,
    held: int,
) -> None:
    expected = {
        "candidates_reviewed": candidates_reviewed,
        "already_present_in_canonical_index": already_present,
        "accepted_new_records": accepted,
        "rejected_records": rejected,
        "held_records": held,
    }
    for field, computed in expected.items():
        declared = scope.get(field)
        if type(declared) is not int or declared != computed:
            raise SystemExit(
                f"scope {field} must equal computed count {computed}, got {declared!r}"
            )


def validate_public_count_impact(impact: object) -> None:
    if not isinstance(impact, dict):
        raise SystemExit("public_count_impact must be an object")
    if set(impact) - {*EXPECTED_PUBLIC_COUNTS, "note"}:
        raise SystemExit("public_count_impact contains an unexpected count category")
    for metric, baseline in EXPECTED_PUBLIC_COUNTS.items():
        row = impact.get(metric)
        if not isinstance(row, dict) or set(row) != {"before", "after", "change"}:
            raise SystemExit(f"public_count_impact {metric} requires before/after/change")
        for field, expected in (("before", baseline), ("after", baseline), ("change", 0)):
            if type(row[field]) is not int or row[field] != expected:
                raise SystemExit(f"public_count_impact {metric}.{field} must equal {expected}")


def record_metadata_digest(record: dict[str, object]) -> str:
    """Bind validated metadata to its ID; this does not verify the observation."""
    payload = json.dumps(record, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def load_checkpoint() -> dict[str, object]:
    if not CHECKPOINT_PATH.is_file():
        raise SystemExit("required checked-in audit checkpoint is missing")
    return json.loads(CHECKPOINT_PATH.read_text(encoding="utf-8"))


def main() -> int:
    delta = json.loads(DELTA_PATH.read_text(encoding="utf-8"))
    records = delta["records"]

    if delta["schema"] != "akashicnet.reddit.canonical-delta-import.v0.2":
        raise SystemExit(f"unexpected schema: {delta['schema']}")
    gates = delta.get("gates", {})
    for gate in sorted(REQUIRED_FALSE_GATES):
        if gates.get(gate) is not False:
            raise SystemExit(f"{gate} gate must be false")
    for gate in sorted(REQUIRED_TRUE_GATES):
        if gates.get(gate) is not True:
            raise SystemExit(f"{gate} gate must be true")
    validate_public_count_impact(delta.get("public_count_impact"))
    scope = delta.get("scope", {})
    if scope.get("coverage") != "partial_manual":
        raise SystemExit("coverage must be marked partial_manual")
    expected_subreddit = scope.get("subreddit")
    if expected_subreddit != EXPECTED_SUBREDDIT:
        raise SystemExit(f"scope subreddit must be {EXPECTED_SUBREDDIT}")

    canonical_post_ids = load_canonical_post_ids()

    already_present: list[str] = []
    accepted: list[str] = []
    rejected: list[str] = []
    held: list[str] = []

    seen_ids: set[str] = set()
    seen_urls: set[str] = set()
    observed_fields: set[str] = set()
    record_metadata_sha256: dict[str, str] = {}

    for record in records:
        fields = set(record)
        observed_fields |= fields
        try:
            post_id, canonical_url = validate_record(record, expected_subreddit)
        except ValueError:
            rejected.append(str(record.get("reddit_post_id", "<missing>")))
            continue
        if post_id in seen_ids or canonical_url in seen_urls:
            rejected.append(post_id)
            continue
        seen_ids.add(post_id)
        seen_urls.add(canonical_url)
        record_metadata_sha256[post_id] = record_metadata_digest(record)

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
        "schema": "akashicnet.reddit.canonical-delta-import-2026-09-08.audit.v0.2",
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
        "record_metadata_sha256": dict(sorted(record_metadata_sha256.items())),
        "subreddit": EXPECTED_SUBREDDIT,
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

    validate_scope_counts(
        scope,
        candidates_reviewed=len(records),
        already_present=len(already_present),
        accepted=len(accepted),
        rejected=len(rejected),
        held=len(held),
    )

    if len(records) != 10:
        raise SystemExit("expected exactly 10 candidate records")
    if already_present or rejected or held:
        raise SystemExit(
            "unexpected disposition: "
            f"already_present={already_present} rejected={rejected} held={held}"
        )
    if len(accepted) != 10:
        raise SystemExit(f"expected all 10 candidates accepted, got {len(accepted)}")

    checkpoint = load_checkpoint()
    if result != checkpoint:
        raise SystemExit("generated audit differs from checked-in checkpoint")

    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
