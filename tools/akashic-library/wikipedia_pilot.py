#!/usr/bin/env python3
"""Build a small, metadata-only Wikipedia pilot for AkashicNET.

The pilot uses MediaWiki search results only. It does not mirror article text.
"""

import argparse
import csv
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote

import requests

API = "https://en.wikipedia.org/w/api.php"
USER_AGENT = (
    "AkashicNET/0.3 (research metadata importer; "
    "https://github.com/tws9stmcbf-web/AkashicNET)"
)

TOPICS = [
    "consciousness",
    "neuroscience",
    "meditation",
    "psychedelics",
    "panpsychism",
    "philosophy of mind",
    "quantum physics",
    "cosmology",
    "archaeology",
    "anthropology",
    "mycology",
    "artificial intelligence",
]

DEFAULT_OUT = Path("references/community/wikipedia-akashic-pilot.csv")
FIELDS = [
    "source",
    "page_id",
    "title",
    "topic_seed",
    "url",
    "retrieved_utc",
    "provenance_status",
    "content_policy",
]


def fetch_candidates(session: requests.Session, topic: str, limit: int) -> list[dict]:
    params = {
        "action": "query",
        "list": "search",
        "srsearch": topic,
        "srnamespace": 0,
        "srlimit": limit,
        "srprop": "size|wordcount|timestamp",
        "format": "json",
        "formatversion": 2,
        "maxlag": 5,
    }
    response = session.get(API, params=params, timeout=20)
    response.raise_for_status()
    return response.json()["query"]["search"]


def build_rows(target: int = 100, per_topic: int = 10, delay: float = 0.5) -> list[dict]:
    session = requests.Session()
    session.headers.update({"User-Agent": USER_AGENT})
    retrieved = datetime.now(timezone.utc).isoformat()
    rows: list[dict] = []
    seen: set[str] = set()

    for topic in TOPICS:
        for item in fetch_candidates(session, topic, per_topic):
            page_id = str(item["pageid"])
            if page_id in seen:
                continue
            seen.add(page_id)
            title = item["title"]
            rows.append(
                {
                    "source": "Wikipedia",
                    "page_id": page_id,
                    "title": title,
                    "topic_seed": topic,
                    "url": "https://en.wikipedia.org/wiki/" + quote(title.replace(" ", "_"), safe="()_,-"),
                    "retrieved_utc": retrieved,
                    "provenance_status": "source_metadata",
                    "content_policy": "metadata_only_no_article_text",
                }
            )
            if len(rows) >= target:
                return rows
        time.sleep(delay)
    return rows


def write_csv(rows: list[dict], output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", type=int, default=100)
    parser.add_argument("--per-topic", type=int, default=10)
    parser.add_argument("--delay", type=float, default=0.5)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUT)
    args = parser.parse_args()

    rows = build_rows(args.target, args.per_topic, args.delay)
    write_csv(rows, args.output)
    print(f"Created {args.output}")
    print(f"Records: {len(rows)}")
    print(f"Unique page IDs: {len({row['page_id'] for row in rows})}")


if __name__ == "__main__":
    main()
