#!/usr/bin/env python3
"""Akashic Library batch importer scaffold.

This tool is designed for resumable, rights-safe processing of a public Google
Drive archive. It keeps the archive in a provenance-first mode and never claims
full import validation when the public metadata does not expose sufficient
licence or item-level detail.
"""

from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

from classifiers import classify_reuse_decision, classify_source_type, classify_subject


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Akashic Library batch importer")
    parser.add_argument(
        "--source-url",
        default="https://drive.google.com/drive/folders/1TPFgWXNA1FfL0SzJh9Y0bBoLd0eb1ffQ",
        help="Public Google Drive folder to map.",
    )
    parser.add_argument(
        "--items-csv",
        default="",
        help="Optional CSV of discovered items; otherwise a minimal root-folder dry-run record is used.",
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=50,
        help="Maximum number of items processed in a batch.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Default safe mode: classify and log without copying any files.",
    )
    parser.add_argument(
        "--resume",
        action="store_true",
        help="Resume from the last checkpoint when available.",
    )
    parser.add_argument(
        "--checkpoint",
        default="tools/akashic-library/state/checkpoint.json",
        help="Checkpoint file for batch state.",
    )
    parser.add_argument(
        "--audit-log",
        default="tools/akashic-library/state/audit.jsonl",
        help="Append-only audit log for processing decisions.",
    )
    parser.add_argument(
        "--error-log",
        default="tools/akashic-library/state/errors.jsonl",
        help="Log file for failed or unavailable items.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=0,
        help="Optional number of items to process in a dry-run subset.",
    )
    parser.add_argument(
        "--out-csv",
        default="references/akashic-library/AKASHIC_LIBRARY_INDEX.csv",
        help="Output CSV for the current discovered batch index.",
    )
    return parser.parse_args()


def load_items_from_csv(path: str) -> List[Dict[str, Any]]:
    if not path:
        return []
    rows: List[Dict[str, Any]] = []
    with open(path, newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            rows.append(row)
    return rows


def root_folder_record(source_url: str) -> Dict[str, Any]:
    return {
        "title": "Books",
        "author": "unknown",
        "source_name": "Public Google Drive folder",
        "original_source_url": source_url,
        "drive_path": "root",
        "drive_url": source_url,
        "year": "unknown",
        "file_type": "folder",
        "subject_category": "unknown",
        "source_type": "archive bundle",
        "licence_status": "unknown",
        "reuse_decision": "INDEX_ONLY",
        "provenance_status": "link_only",
        "related_toolkit_framework": "Library of Alexandria / Library of Infinite Love & Wisdom",
        "evidence_status": "Not scientific evidence; metadata only",
        "notes": "Public folder metadata confirms the root folder is titled 'Books', but no item-level list or licence statement was exposed in the unauthenticated public HTML. This record is an index-only provenance record.",
    }


def build_batch_items(source_url: str, items_csv: str) -> List[Dict[str, Any]]:
    if items_csv:
        rows = load_items_from_csv(items_csv)
        if rows:
            return rows
    return [root_folder_record(source_url)]


def normalize_record(row: Dict[str, Any]) -> Dict[str, Any]:
    title = str(row.get("title") or row.get("name") or "unknown").strip() or "unknown"
    folder = str(row.get("drive_path") or row.get("parent_folder_path") or "root").strip() or "root"
    source_name = str(row.get("source_name") or row.get("author") or "unknown").strip() or "unknown"
    original_url = str(row.get("original_source_url") or row.get("drive_url") or "").strip()
    licence_status = str(row.get("licence_status") or "unknown").strip() or "unknown"
    subject = classify_subject(title, folder)
    source_type = classify_source_type(title, str(row.get("file_type") or "").strip())
    reuse_decision = classify_reuse_decision(licence_status, title)
    return {
        "title": title,
        "author": str(row.get("author") or source_name or "unknown").strip() or "unknown",
        "source_name": source_name,
        "original_source_url": original_url,
        "drive_path": folder,
        "drive_url": str(row.get("drive_url") or original_url or "").strip(),
        "year": str(row.get("year") or row.get("date_year") or "unknown").strip() or "unknown",
        "file_type": str(row.get("file_type") or row.get("mime_type") or source_type).strip() or "unknown",
        "subject_category": subject,
        "source_type": source_type,
        "licence_status": licence_status,
        "reuse_decision": reuse_decision,
        "provenance_status": str(row.get("provenance_status") or "link_only").strip() or "link_only",
        "related_toolkit_framework": str(row.get("related_toolkit_framework") or "Library of Alexandria / Library of Infinite Love & Wisdom").strip(),
        "evidence_status": str(row.get("evidence_status") or "Not scientific evidence; metadata only").strip(),
        "notes": str(row.get("notes") or "").strip(),
    }


def write_csv(path: str, rows: Iterable[Dict[str, Any]]) -> None:
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "title",
        "author",
        "source_name",
        "original_source_url",
        "drive_path",
        "drive_url",
        "year",
        "file_type",
        "subject_category",
        "source_type",
        "licence_status",
        "reuse_decision",
        "provenance_status",
        "related_toolkit_framework",
        "evidence_status",
        "notes",
    ]
    with out.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def checkpoint_payload(run_id: str, source_url: str, processed: int) -> Dict[str, Any]:
    return {
        "run_id": run_id,
        "source_url": source_url,
        "processed_count": processed,
        "last_updated_utc": utc_now(),
        "completed": False,
    }


def persist_checkpoint(path: str, payload: Dict[str, Any]) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def main() -> int:
    args = parse_args()
    run_id = f"akashic-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}"
    checkpoint_path = Path(args.checkpoint)
    checkpoint_path.parent.mkdir(parents=True, exist_ok=True)

    candidates = build_batch_items(args.source_url, args.items_csv)
    processed = [normalize_record(item) for item in candidates]
    if args.limit and args.limit > 0:
        processed = processed[: args.limit]

    totals = {
        "total_discovered": len(processed),
        "index_only": sum(1 for item in processed if item["reuse_decision"] == "INDEX_ONLY"),
        "link_plus_metadata": sum(1 for item in processed if item["reuse_decision"] == "LINK_PLUS_METADATA"),
        "import_approved": sum(1 for item in processed if item["reuse_decision"] == "IMPORT"),
    }
    write_csv(args.out_csv, processed)
    persist_checkpoint(str(checkpoint_path), checkpoint_payload(run_id, args.source_url, len(processed)))

    summary = {
        "run_id": run_id,
        "source_url": args.source_url,
        "dry_run": bool(args.dry_run),
        "batch_size": args.batch_size,
        "checkpoint": str(checkpoint_path),
        "out_csv": args.out_csv,
        "items_discovered": totals["total_discovered"],
        "items_processed": len(processed),
        "index_only": totals["index_only"],
        "link_plus_metadata": totals["link_plus_metadata"],
        "import_approved": totals["import_approved"],
        "received_at": utc_now(),
        "note": "Current public metadata does not expose enough item-level licence or file detail to certify a complete archive import. This batch follows a conservative metadata-first workflow.",
    }
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
