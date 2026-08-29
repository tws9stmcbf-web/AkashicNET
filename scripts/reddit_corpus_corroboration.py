#!/usr/bin/env python3
"""AkashicNET Reddit Corpus Corroboration Audit.

Cross-matches sequence-filtered historical Reddit candidates against an explicit
corroboration manifest. It does not perform network requests and does not promote
uncorroborated candidates to verified status.
"""
from __future__ import annotations

import argparse
import csv
import json
import re
from collections import Counter
from pathlib import Path
from urllib.parse import urlparse

POST_RE = re.compile(r"^/r/([^/]+)/comments/([0-9A-Za-z]+)/?(?:[^/]*)/?$", re.I)
SEED_SCHEMA_RE = re.compile(r"^akashicnet\.reddit\.corroboration-seed\.(v[0-9]+(?:\.[0-9]+)*)$")


def parse_candidate(raw: str):
    value = raw.strip()
    if "," in value:
        return None
    parsed = urlparse(value)
    if parsed.netloc.lower() not in {"reddit.com", "www.reddit.com", "old.reddit.com", "new.reddit.com", "m.reddit.com"}:
        return None
    match = POST_RE.match(parsed.path)
    if not match:
        return None
    subreddit, post_id = match.groups()
    return {"subreddit": subreddit, "post_id": post_id.lower(), "id_int": int(post_id, 36)}


def load_unique_candidates(path: Path):
    unique = {}
    with path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.reader(handle)
        next(reader, None)
        for row in reader:
            if not row:
                continue
            record = parse_candidate(row[0])
            if record:
                unique.setdefault(record["post_id"], record)
    return list(unique.values())


def sequence_suspects(records, min_run=4):
    ordered = sorted(records, key=lambda r: r["id_int"])
    runs, current = [], []
    for record in ordered:
        if current and record["id_int"] != current[-1]["id_int"] + 1:
            if len(current) >= min_run:
                runs.append(current)
            current = []
        current.append(record)
    if len(current) >= min_run:
        runs.append(current)
    return {r["post_id"] for run in runs for r in run}


def load_seed(path: Path):
    data = json.loads(path.read_text(encoding="utf-8"))
    result = {}
    for record in data.get("records", []):
        pid = str(record["post_id"]).lower()
        result[pid] = record
    return data, result


def report_schema(seed_doc):
    seed_schema = str(seed_doc.get("schema", ""))
    match = SEED_SCHEMA_RE.match(seed_schema)
    if not match:
        raise ValueError(f"unsupported corroboration seed schema: {seed_schema!r}")
    return f"akashicnet.reddit.corpus-corroboration.{match.group(1)}"


def audit(corpus_path: Path, seed_path: Path, min_run=4):
    records = load_unique_candidates(corpus_path)
    suspects = sequence_suspects(records, min_run=min_run)
    filtered = [r for r in records if r["post_id"] not in suspects]
    seed_doc, seed = load_seed(seed_path)

    corroborated = []
    uncorroborated = []
    seed_not_in_corpus = []
    by_id = {r["post_id"]: r for r in filtered}
    for record in filtered:
        if record["post_id"] in seed:
            corroborated.append(record)
        else:
            uncorroborated.append(record)
    for pid, evidence in seed.items():
        if pid not in by_id:
            seed_not_in_corpus.append(evidence)

    return {
        "schema": report_schema(seed_doc),
        "historical_unique_structural_candidates": len(records),
        "suspected_generated_by_sequence_filter": len(suspects),
        "candidate_pool_after_sequence_filter": len(filtered),
        "corroboration_seed_records": len(seed),
        "corroborated_candidates": len(corroborated),
        "uncorroborated_candidates": len(uncorroborated),
        "seed_records_not_in_historical_candidate_pool": len(seed_not_in_corpus),
        "corroborated_by_subreddit": dict(sorted(Counter(r["subreddit"] for r in corroborated).items())),
        "uncorroborated_by_subreddit": dict(sorted(Counter(r["subreddit"] for r in uncorroborated).items())),
        "seed_not_in_corpus": seed_not_in_corpus,
        "method": {
            "sequence_filter_min_run": min_run,
            "corroboration_source_type": seed_doc.get("source_type"),
            "promotion_rule": "candidate becomes corroborated only when its post_id appears in the explicit independent evidence seed",
        },
        "notes": [
            "corroborated is stronger than candidate but is not equivalent to current live verification",
            "uncorroborated means no match in this seed, not evidence of non-existence",
            "suspected generated is a provenance-anomaly classification, not proof of fabrication",
            "no usernames, post bodies, comments, or live Reddit API requests are used",
        ],
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("corpus", type=Path)
    parser.add_argument("seed", type=Path)
    parser.add_argument("--json-out", type=Path)
    parser.add_argument("--min-run", type=int, default=4)
    args = parser.parse_args()
    report = audit(args.corpus, args.seed, args.min_run)
    text = json.dumps(report, indent=2, sort_keys=True)
    print(text)
    if args.json_out:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(text + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
