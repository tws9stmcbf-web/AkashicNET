from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


@dataclass(frozen=True)
class RedditSource:
    source_id: str
    platform: str
    kind: str
    subreddit: str
    canonical_url: str
    enabled: bool = True
    access_mode: str = "read_only"
    default_listing: str = "new"
    classification_profile: str = "default"
    evidence_default: str = "community_observation"
    provenance_default: str = "link_only"
    safety_note: str = ""

    @classmethod
    def from_dict(cls, payload: Dict[str, Any]) -> "RedditSource":
        source = cls(**{k: v for k, v in payload.items() if k in cls.__dataclass_fields__})
        if source.platform != "reddit":
            raise ValueError(f"Unsupported platform for {source.source_id}: {source.platform}")
        if source.kind != "subreddit":
            raise ValueError(f"Unsupported source kind for {source.source_id}: {source.kind}")
        if source.access_mode != "read_only":
            raise ValueError(f"Reddit Bridge only supports read_only sources: {source.source_id}")
        return source


@dataclass
class RedditPostRecord:
    source: str
    source_id: str
    subreddit: str
    reddit_post_id: str
    reddit_url: str
    canonical_reddit_url: str
    title: str
    author: str = "unknown"
    attribution_note: str = "Original poster as listed on Reddit; no private information reproduced."
    created_utc: Optional[str] = None
    retrieved_at_utc: str = field(default_factory=utc_now_iso)
    lifecycle_status: str = "active"
    source_type: str = "reddit_post"
    category: str = "community"
    short_summary: str = "Metadata-only Reddit record; canonical source remains Reddit."
    external_source_url: Optional[str] = None
    toolkit_framework: str = ""
    research_question_potential: str = ""
    visual_audio_art_flag: str = "Unknown"
    evidence_status: str = "community_observation"
    provenance_status: str = "link_only"
    content_fingerprint: str = ""
    url_fingerprint: str = ""
    dedupe_key: str = ""
    dedupe_status: str = "unique"
    duplicate_of: Optional[str] = None
    crosspost_parent_id: Optional[str] = None
    crosspost_root_id: Optional[str] = None
    crosspost_chain: List[str] = field(default_factory=list)
    lineage_status: str = "none"
    ingestion_run_id: str = "dry_run"

    def to_dict(self) -> Dict[str, Any]:
        return dict(self.__dict__)
