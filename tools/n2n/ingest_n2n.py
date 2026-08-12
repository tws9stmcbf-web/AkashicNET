#!/usr/bin/env python3
"""N2N ingestion prototype.

This is a provenance-first, dry-run prototype for curating a small batch of
public r/NeuronsToNirvana records into the Toolkit archive without copying
Reddit content wholesale.

The script is intentionally conservative:
- no large-scale scrape or mirror behaviour
- no writes to the main archive unless explicitly enabled
- dry-run mode is the default and recommended for this prototype
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Set, Tuple
from urllib.parse import urlparse

ALLOWED_CATEGORIES = {
    "research",
    "consciousness",
    "philosophy",
    "psychedelics",
    "wisdom",
    "lived experience",
    "frameworks",
    "art",
    "music",
    "humour",
    "stories",
    "nature",
    "community",
    "speculation",
}

ALLOWED_EVIDENCE = {
    "community_observation",
    "lived_experience",
    "creative_cultural_material",
    "speculation",
    "scientific_evidence",
}

# The repository already uses these labels in the canonical archive schema.
CATEGORY_CANONICAL_MAP = {
    "Research": "research",
    "Consciousness": "consciousness",
    "Philosophy": "philosophy",
    "Wisdom Traditions": "wisdom",
    "Psychedelics": "psychedelics",
    "Personal Experience": "lived experience",
    "Frameworks": "frameworks",
    "Art": "art",
    "Music": "music",
    "Humour": "humour",
    "Stories": "stories",
    "Nature / Ecology": "nature",
    "Community": "community",
    "Future / Speculation": "speculation",
    "Indigenous / Cultural Knowledge": "wisdom",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Prototype N2N ingestion tool")
    parser.add_argument(
        "--csv",
        default="references/community/n2n-pilot-index.csv",
        help="CSV file containing candidate public N2N archive rows.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=25,
        help="Number of candidate rows to process in this dry run.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Default behavior. Never writes to the canonical archive.",
    )
    parser.add_argument(
        "--write-records",
        action="store_true",
        help="Explicitly allowed write path for a future archive batch. Disabled by default.",
    )
    parser.add_argument(
        "--log",
        default="tools/n2n/dryrun/25_post_test.jsonl",
        help="Where to store the auditable import log for the dry-run.",
    )
    parser.add_argument(
        "--skip-existing",
        action="store_true",
        help="Skip rows already present in a local dedupe list.",
    )
    return parser.parse_args()


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def extract_post_id(reddit_url: str) -> Optional[str]:
    if not reddit_url:
        return None
    match = re.search(r"/comments/([A-Za-z0-9]+)", reddit_url)
    if match:
        return match.group(1)
    parsed = urlparse(reddit_url)
    if parsed.netloc.endswith("reddit.com"):
        parts = [p for p in parsed.path.split("/") if p]
        if len(parts) >= 2 and parts[0] == "r":
            return None
    return None


def normalize_url(value: str) -> Optional[str]:
    if not value:
        return None
    text = value.strip()
    if not text:
        return None
    if text.startswith("http://"):
        text = "https://" + text[7:]
    if not text.startswith("http"):
        text = "https://" + text
    return text


def canonicalize_record(row: Dict[str, str]) -> Dict[str, Any]:
    title = (row.get("title") or "").strip()
    reddit_url = normalize_url(row.get("reddit_url") or "")
    post_id = extract_post_id(reddit_url or "")
    author = (row.get("author") or "Unknown").strip()
    attribution_note = (row.get("attribution_note") or "").strip()
    date_value = (row.get("date") or "unknown").strip()
    source_type = (row.get("source_type") or "discussion").strip()
    category_raw = (row.get("category") or "").strip()
    category = CATEGORY_CANONICAL_MAP.get(category_raw, category_raw.lower() if category_raw else "research")
    if category not in ALLOWED_CATEGORIES:
        category = "research"
    evidence_status = (row.get("evidence_status") or "community_observation").strip()
    if evidence_status not in ALLOWED_EVIDENCE:
        evidence_status = "community_observation"
    short_summary = (row.get("short_summary") or "").strip()
    external_source_url = normalize_url(row.get("external_source_url") or row.get("external_source") or "")
    toolkit_framework = (row.get("toolkit_framework") or "").strip()
    research_question = (row.get("research_question_potential") or "").strip()
    visual_audio_art_flag = (row.get("visual_audio_art_flag") or "No").strip()
    provenance_status = (row.get("provenance_status") or "Link-only; attribution preserved.").strip()

    lived_experience_flag = (
        evidence_status == "lived_experience"
        or "personal" in source_type.lower()
        or "experience" in category.lower()
        or "lived" in category.lower()
        or any(k in short_summary.lower() for k in ["felt", "experience", "self", "shift", "altered", "integration"])
    )

    return {
        "title": title,
        "reddit_post_id": post_id,
        "reddit_url": reddit_url,
        "author": author,
        "attribution_note": attribution_note,
        "date": date_value,
        "source_type": source_type,
        "category": category,
        "evidence_status": evidence_status,
        "lived_experience_flag": bool(lived_experience_flag),
        "external_source_url": external_source_url,
        "toolkit_framework": toolkit_framework,
        "research_question_potential": research_question,
        "visual_audio_art_flag": visual_audio_art_flag,
        "provenance_status": provenance_status,
        "short_summary": short_summary or f"Public Reddit discussion classified under {category}.",
        "provenance_summary": "Canonical source remains Reddit; archive stores structured metadata and links only.",
        "retrieval_status": "dry_run_candidate",
    }


def read_csv_rows(csv_path: Path) -> List[Dict[str, str]]:
    with csv_path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def pick_batch(rows: Iterable[Dict[str, str]], limit: int) -> List[Dict[str, str]]:
    selected: List[Dict[str, str]] = []
    for row in rows:
        if row.get("reddit_url"):
            selected.append(row)
        if len(selected) >= limit:
            break
    return selected


def duplicates_for(rows: Iterable[Dict[str, Any]]) -> Set[str]:
    seen: Set[str] = set()
    for row in rows:
        post_id = row.get("reddit_post_id")
        url = row.get("reddit_url")
        if post_id:
            seen.add(post_id)
        if url:
            seen.add(url)
    return seen


def classify_issues(record: Dict[str, Any]) -> List[str]:
    issues: List[str] = []
    if record["category"] not in ALLOWED_CATEGORIES:
        issues.append("category_outside_allowed_taxonomy")
    if record["evidence_status"] not in ALLOWED_EVIDENCE:
        issues.append("evidence_status_unrecognized")
    if not record["short_summary"]:
        issues.append("missing_short_summary")
    if not record["reddit_url"]:
        issues.append("missing_canonical_url")
    if record["provenance_status"].lower().find("unknown") >= 0 or record["provenance_status"].lower().find("uncertain") >= 0:
        issues.append("uncertain_provenance")
    return issues


def provenance_issues(record: Dict[str, Any]) -> List[str]:
    issues: List[str] = []
    if not record["author"] or record["author"].lower() == "unknown":
        issues.append("author_not_publicly_attributed")
    if not record["attribution_note"]:
        issues.append("missing_attribution_note")
    if "deleted" in record["provenance_status"].lower() or "removed" in record["provenance_status"].lower():
        issues.append("deleted_or_removed_source")
    return issues


def write_jsonl(path: Path, rows: List[Dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")


def main() -> int:
    args = parse_args()
    csv_path = Path(args.csv)
    if not csv_path.exists():
        print(f"ERROR: CSV not found: {csv_path}", file=sys.stderr)
        return 2

    if args.write_records and not args.dry_run:
        print("INFO: write mode is intentionally disabled until the archive workflow is explicitly approved.", file=sys.stderr)
        return 3

    rows = read_csv_rows(csv_path)
    batch = pick_batch(rows, args.limit)
    canonical_batch = [canonicalize_record(r) for r in batch]
    seen: Set[str] = set()
    processed: List[Dict[str, Any]] = []
    classification_issues = 0
    provenance_issues_count = 0
    duplicates = 0
    unavailable = 0
    api_blocked = True

    for record in canonical_batch:
        post_key = record["reddit_post_id"] or record["reddit_url"]
        if post_key in seen:
            duplicates += 1
            continue
        seen.add(post_key)

        record["retrieval_status"] = "dry_run_processed"
        record["import_log_timestamp"] = utc_now_iso()
        record["import_mode"] = "dry_run"
        record["api_access_state"] = "Public Reddit access blocked in this environment (HTTP 403)"
        record["classification_issues"] = classify_issues(record)
        record["provenance_issues"] = provenance_issues(record)
        classification_issues += len(record["classification_issues"])
        provenance_issues_count += len(record["provenance_issues"])
        if record["reddit_url"] is None:
            unavailable += 1
            record["retrieval_status"] = "unavailable"
        processed.append(record)

    summary = {
        "generator": "N2N ingestion prototype",
        "timestamp_utc": utc_now_iso(),
        "source_csv": str(csv_path),
        "mode": "dry_run",
        "posts_discovered": len(batch),
        "posts_successfully_processed": len(processed),
        "duplicates": duplicates,
        "unavailable_deleted_posts": unavailable,
        "classification_issues": classification_issues,
        "provenance_issues": provenance_issues_count,
        "api_access_limitations": [
            "Public Reddit JSON endpoint was blocked in this environment with HTTP 403.",
            "The prototype therefore uses a dry-run, curated record set rather than direct live scraping.",
            "A production deployment should operate with a Reddit API app and documented access model."
        ],
        "ready_to_scale": False,
        "notes": [
            "Canonical source remains Reddit.",
            "No additional posts were imported into the archive.",
            "Phase 3 is not marked complete."
        ],
        "sample_batch": processed,
    }

    if args.dry_run:
        log_path = Path(args.log)
        write_jsonl(log_path, processed)
        print(json.dumps(summary, ensure_ascii=False, indent=2))
        return 0

    print("Dry-run is the default and recommended mode for this prototype.", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
