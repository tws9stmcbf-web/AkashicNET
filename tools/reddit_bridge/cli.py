#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

if __package__ is None or __package__ == "":
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from tools.reddit_bridge.bridge import build_records
from tools.reddit_bridge.clients import FixtureRedditReadOnlyClient
from tools.reddit_bridge.registry import registry_by_id, load_registry
from tools.reddit_bridge.storage import write_dedupe_csv, write_jsonl, write_lineage_csv


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Read-only AkashicNET Reddit Bridge")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("sources", help="List configured read-only Reddit sources")
    sub.add_parser("validate-registry", help="Validate the Reddit source registry")
    ingest = sub.add_parser("ingest", help="Build normalized records from a read-only fixture or API client")
    ingest.add_argument("--source", default="all", help="Source ID or 'all'")
    ingest.add_argument("--fixture", required=True, help="Local JSON fixture path for the MVP bridge")
    ingest.add_argument("--limit", type=int, default=25)
    ingest.add_argument("--dry-run", action="store_true", default=True)
    ingest.add_argument("--write-records", action="store_true", help="Write bridge outputs; still read-only with respect to Reddit")
    ingest.add_argument("--output-jsonl", default="references/community/reddit-bridge-records.jsonl")
    ingest.add_argument("--output-dedupe", default="references/community/reddit-bridge-dedupe-index.csv")
    ingest.add_argument("--output-lineage", default="references/community/reddit-bridge-lineage-index.csv")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.command == "sources":
        print(json.dumps([source.__dict__ for source in load_registry()], indent=2, ensure_ascii=False))
        return 0
    if args.command == "validate-registry":
        sources = load_registry()
        print(json.dumps({"valid": True, "sources": len(sources), "read_only": all(s.access_mode == "read_only" for s in sources)}, indent=2))
        return 0
    if args.command == "ingest":
        sources_by_id = registry_by_id()
        selected = list(sources_by_id.values()) if args.source == "all" else [sources_by_id[args.source]]
        client = FixtureRedditReadOnlyClient(args.fixture)
        records = []
        for source in selected:
            if not source.enabled:
                continue
            payloads = client.list_subreddit_posts(source.subreddit, source.default_listing, args.limit)
            records.extend(build_records(source, payloads))
        summary = {"mode": "dry_run", "read_only": True, "records": len(records), "duplicates": sum(1 for r in records if r.dedupe_status != "unique")}
        if args.write_records:
            write_jsonl(args.output_jsonl, records)
            write_dedupe_csv(args.output_dedupe, records)
            write_lineage_csv(args.output_lineage, records)
            summary["outputs"] = [args.output_jsonl, args.output_dedupe, args.output_lineage]
        print(json.dumps(summary, indent=2, ensure_ascii=False))
        return 0
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
