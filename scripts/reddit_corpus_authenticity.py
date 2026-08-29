#!/usr/bin/env python3
"""AkashicNET Historical Reddit Corpus Authenticity Audit v0.2.

This is a heuristic provenance audit, not a Reddit existence validator. It detects
patterns that are improbable in organically collected Reddit post IDs, especially
long runs of consecutive base-36 IDs. No Reddit API calls or user content are used.
"""
from __future__ import annotations

import argparse
import csv
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from urllib.parse import urlparse

POST_RE = re.compile(r"^/r/([^/]+)/comments/([0-9A-Za-z]+)/?(?:[^/]*)/?$", re.I)


def parse_candidate(raw: str):
    value = raw.strip()
    if "," in value:
        return None
    try:
        parsed = urlparse(value)
    except ValueError:
        return None
    if parsed.netloc.lower() not in {"reddit.com", "www.reddit.com", "old.reddit.com", "new.reddit.com", "m.reddit.com"}:
        return None
    match = POST_RE.match(parsed.path)
    if not match:
        return None
    subreddit, post_id = match.groups()
    return {"raw": value, "subreddit": subreddit, "post_id": post_id.lower(), "id_int": int(post_id, 36)}


def consecutive_runs(records, min_run=4):
    """Return maximal runs of unique IDs whose base-36 integer values increment by one."""
    by_id = {}
    for record in records:
        by_id.setdefault(record["post_id"], record)
    ordered = sorted(by_id.values(), key=lambda r: r["id_int"])
    runs = []
    current = []
    for record in ordered:
        if current and record["id_int"] != current[-1]["id_int"] + 1:
            if len(current) >= min_run:
                runs.append(current)
            current = []
        current.append(record)
    if len(current) >= min_run:
        runs.append(current)
    return runs


def audit(path: Path, min_run=4):
    rows = []
    with path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.reader(handle)
        next(reader, None)
        for row in reader:
            if row:
                candidate = parse_candidate(row[0])
                if candidate:
                    rows.append(candidate)

    unique = {}
    for record in rows:
        unique.setdefault(record["post_id"], record)
    records = list(unique.values())
    runs = consecutive_runs(records, min_run=min_run)
    suspect_ids = {record["post_id"] for run in runs for record in run}
    suspect_by_subreddit = Counter(r["subreddit"] for r in records if r["post_id"] in suspect_ids)
    remaining_by_subreddit = Counter(r["subreddit"] for r in records if r["post_id"] not in suspect_ids)

    run_lengths = Counter(len(run) for run in runs)
    longest = sorted(runs, key=len, reverse=True)[:20]
    report = {
        "schema": "akashicnet.reddit.corpus-authenticity.v0.2",
        "input": str(path),
        "method": {
            "signal": "maximal runs of consecutive base-36 Reddit post IDs",
            "minimum_run_length": min_run,
            "interpretation": "heuristic provenance anomaly only; not proof of fabrication or post non-existence",
        },
        "unique_structural_candidates": len(records),
        "suspected_generated_ids": len(suspect_ids),
        "remaining_candidates_after_sequence_filter": len(records) - len(suspect_ids),
        "sequence_runs": len(runs),
        "run_length_distribution": dict(sorted(run_lengths.items())),
        "suspected_by_subreddit": dict(sorted(suspect_by_subreddit.items())),
        "remaining_by_subreddit": dict(sorted(remaining_by_subreddit.items())),
        "longest_runs": [
            {
                "length": len(run),
                "first_id": run[0]["post_id"],
                "last_id": run[-1]["post_id"],
                "subreddits": dict(Counter(r["subreddit"] for r in run)),
            }
            for run in longest
        ],
        "notes": [
            "sequence-filtered records remain candidates, not verified Reddit posts",
            "suspected_generated means generated-looking by this narrow heuristic, not proven synthetic",
            "independent corroboration or authorised Reddit API checks are required for verified status",
            "no usernames, post bodies, comments, or Reddit API requests are used",
        ],
    }
    return report


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("--json-out", type=Path)
    parser.add_argument("--min-run", type=int, default=4)
    args = parser.parse_args()
    report = audit(args.input, args.min_run)
    text = json.dumps(report, indent=2, sort_keys=True)
    print(text)
    if args.json_out:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(text + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
