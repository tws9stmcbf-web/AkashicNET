from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Iterable

from .models import RedditPostRecord


def write_jsonl(path: str | Path, records: Iterable[RedditPostRecord]) -> None:
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record.to_dict(), ensure_ascii=False) + "\n")


def write_dedupe_csv(path: str | Path, records: Iterable[RedditPostRecord]) -> None:
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    fields = ["dedupe_key", "reddit_post_id", "canonical_reddit_url", "subreddit", "content_fingerprint", "duplicate_of", "dedupe_status", "retrieved_at_utc"]
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for record in records:
            writer.writerow({field: getattr(record, field) for field in fields})


def write_lineage_csv(path: str | Path, records: Iterable[RedditPostRecord]) -> None:
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    fields = ["reddit_post_id", "subreddit", "canonical_reddit_url", "crosspost_parent_id", "crosspost_root_id", "lineage_status", "crosspost_chain"]
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for record in records:
            writer.writerow({field: getattr(record, field) for field in fields})
