from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List

from .canonicalize import fingerprint, normalize_reddit_url, post_identity
from .dedupe import dedupe_records
from .lineage import extract_crosspost_lineage
from .models import RedditPostRecord, RedditSource


def _created_iso(created_utc: Any) -> str | None:
    if created_utc in (None, ""):
        return None
    return datetime.fromtimestamp(float(created_utc), timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def record_from_api_payload(source: RedditSource, payload: Dict[str, Any], ingestion_run_id: str = "dry_run") -> RedditPostRecord:
    permalink = payload.get("permalink") or payload.get("url") or ""
    post_id, canonical_url = post_identity(permalink, source.subreddit)
    external_url = payload.get("url") or None
    if external_url:
        try:
            external_url = None if normalize_reddit_url(external_url, source.subreddit) == canonical_url else external_url
        except ValueError:
            pass
    title = (payload.get("title") or "").strip()
    author = (payload.get("author") or "unknown").strip() or "unknown"
    parent_id, root_id, chain, lineage_status = extract_crosspost_lineage(payload)
    content_basis = "|".join([
        title.lower().strip(),
        str(external_url or "").strip(),
        str(payload.get("selftext") or "").strip(),
        str(payload.get("created_utc") or ""),
    ])
    content_hash = fingerprint(content_basis)
    dedupe_key = f"reddit:{source.subreddit}:{post_id}"
    return RedditPostRecord(
        source="Reddit",
        source_id=source.source_id,
        subreddit=source.subreddit,
        reddit_post_id=post_id,
        reddit_url=canonical_url,
        canonical_reddit_url=canonical_url,
        title=title,
        author=author,
        created_utc=_created_iso(payload.get("created_utc")),
        lifecycle_status="deleted" if payload.get("removed_by_category") == "deleted" else "active",
        category="community",
        external_source_url=external_url,
        evidence_status=source.evidence_default,
        provenance_status=source.provenance_default,
        content_fingerprint=content_hash,
        url_fingerprint=fingerprint(canonical_url),
        dedupe_key=dedupe_key,
        crosspost_parent_id=parent_id,
        crosspost_root_id=root_id,
        crosspost_chain=chain,
        lineage_status=lineage_status,
        ingestion_run_id=ingestion_run_id,
    )


def build_records(source: RedditSource, payloads: Iterable[Dict[str, Any]], ingestion_run_id: str = "dry_run") -> List[RedditPostRecord]:
    records = [record_from_api_payload(source, payload, ingestion_run_id) for payload in payloads]
    return dedupe_records(records)
