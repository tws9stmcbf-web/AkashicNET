from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, Optional

from .models import RedditPostRecord


@dataclass(frozen=True)
class DedupeDecision:
    status: str
    duplicate_of: Optional[str] = None


class DedupeIndex:
    def __init__(self) -> None:
        self.by_post_id: Dict[str, RedditPostRecord] = {}
        self.by_url: Dict[str, RedditPostRecord] = {}
        self.by_content: Dict[str, RedditPostRecord] = {}

    def check(self, record: RedditPostRecord) -> DedupeDecision:
        if record.reddit_post_id in self.by_post_id:
            return DedupeDecision("duplicate_exact_post_id", self.by_post_id[record.reddit_post_id].dedupe_key)
        if record.canonical_reddit_url in self.by_url:
            return DedupeDecision("duplicate_canonical_url", self.by_url[record.canonical_reddit_url].dedupe_key)
        if record.content_fingerprint and record.content_fingerprint in self.by_content:
            return DedupeDecision("duplicate_content_fingerprint", self.by_content[record.content_fingerprint].dedupe_key)
        return DedupeDecision("unique")

    def add(self, record: RedditPostRecord) -> DedupeDecision:
        decision = self.check(record)
        record.dedupe_status = decision.status
        record.duplicate_of = decision.duplicate_of
        if decision.status == "unique":
            self.by_post_id[record.reddit_post_id] = record
            self.by_url[record.canonical_reddit_url] = record
            if record.content_fingerprint:
                self.by_content[record.content_fingerprint] = record
        return decision


def dedupe_records(records: Iterable[RedditPostRecord]) -> list[RedditPostRecord]:
    index = DedupeIndex()
    output = []
    for record in records:
        index.add(record)
        output.append(record)
    return output
