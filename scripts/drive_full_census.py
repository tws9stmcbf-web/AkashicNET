#!/usr/bin/env python3
"""Build a fresh recursive, pagination-complete census from the 66 AkashicNET Drive roots.

This intentionally does not trust historical direct-object counts. It uses the Google
Drive v3 API with the read-only GOOGLE_DRIVE_ACCESS_TOKEN and follows every
nextPageToken for every discovered folder.
"""

from __future__ import annotations

import csv
import json
import os
import sys
import urllib.parse
import urllib.request
from collections import deque
from pathlib import Path

ROOT_CENSUS = Path("references/community/drive-metadata-root-census.csv")
FOLDER_OUT = Path("references/community/drive-live-full-folder-census.csv")
OBJECT_OUT = Path("references/community/drive-live-full-object-census.csv")
SUMMARY_OUT = Path("references/community/drive-live-full-census-summary.json")
FOLDER_MIME = "application/vnd.google-apps.folder"
EXPECTED_ROOTS = 66


def api_list(token: str, parent_id: str):
    page_token = None
    pages = 0
    items = []
    while True:
        params = {
            "q": f"'{parent_id}' in parents and trashed = false",
            "fields": "nextPageToken,files(id,name,mimeType,size,createdTime,modifiedTime,parents)",
            "pageSize": "1000",
            "supportsAllDrives": "true",
            "includeItemsFromAllDrives": "true",
        }
        if page_token:
            params["pageToken"] = page_token
        url = "https://www.googleapis.com/drive/v3/files?" + urllib.parse.urlencode(params)
        req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
        with urllib.request.urlopen(req, timeout=60) as resp:
            data = json.load(resp)
        pages += 1
        items.extend(data.get("files", []))
        page_token = data.get("nextPageToken")
        if not page_token:
            return items, pages


def load_roots():
    with ROOT_CENSUS.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != EXPECTED_ROOTS:
        raise RuntimeError(f"expected {EXPECTED_ROOTS} roots, found {len(rows)}")
    ids = [r["drive_id"] for r in rows]
    if len(ids) != len(set(ids)):
        raise RuntimeError("duplicate root Drive IDs")
    return rows


def main():
    token = os.environ.get("GOOGLE_DRIVE_ACCESS_TOKEN")
    if not token:
        print("GOOGLE_DRIVE_ACCESS_TOKEN is required", file=sys.stderr)
        return 2

    roots = load_roots()
    folder_rows = []
    object_rows = []
    globally_seen_folders = set()
    globally_seen_objects = set()
    folder_occurrences = 0
    object_occurrences = 0

    for root in roots:
        root_id = root["drive_id"]
        root_title = root["root_title"]
        queue = deque([(root_id, root_title, 0)])
        seen_in_root = set()

        while queue:
            folder_id, path, depth = queue.popleft()
            if folder_id in seen_in_root:
                continue
            seen_in_root.add(folder_id)
            globally_seen_folders.add(folder_id)
            folder_occurrences += 1

            try:
                items, pages = api_list(token, folder_id)
            except Exception as exc:
                # Never persist HTTP exception text because authentication payloads may be sensitive.
                folder_rows.append({
                    "root_title": root_title,
                    "collection_path": path,
                    "depth": depth,
                    "drive_id": folder_id,
                    "direct_documents": "",
                    "direct_child_folders": "",
                    "direct_objects": "",
                    "page_count": "",
                    "pagination_exhausted": False,
                    "status": "ERROR",
                })
                print(f"folder_error root={root_title!r} path={path!r} type={type(exc).__name__}", file=sys.stderr)
                continue

            child_folders = [i for i in items if i.get("mimeType") == FOLDER_MIME]
            docs = [i for i in items if i.get("mimeType") != FOLDER_MIME]
            folder_rows.append({
                "root_title": root_title,
                "collection_path": path,
                "depth": depth,
                "drive_id": folder_id,
                "direct_documents": len(docs),
                "direct_child_folders": len(child_folders),
                "direct_objects": len(items),
                "page_count": pages,
                "pagination_exhausted": True,
                "status": "PASS",
            })

            for item in docs:
                object_occurrences += 1
                globally_seen_objects.add(item["id"])
                object_rows.append({
                    "root_title": root_title,
                    "parent_path": path,
                    "parent_drive_id": folder_id,
                    "drive_id": item["id"],
                    "name": item.get("name", ""),
                    "mime_type": item.get("mimeType", ""),
                    "size": item.get("size", ""),
                    "created_time": item.get("createdTime", ""),
                    "modified_time": item.get("modifiedTime", ""),
                })

            for child in child_folders:
                child_path = f"{path}/{child.get('name','')}"
                queue.append((child["id"], child_path, depth + 1))

    FOLDER_OUT.parent.mkdir(parents=True, exist_ok=True)
    folder_fields = [
        "root_title", "collection_path", "depth", "drive_id",
        "direct_documents", "direct_child_folders", "direct_objects",
        "page_count", "pagination_exhausted", "status",
    ]
    with FOLDER_OUT.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=folder_fields)
        w.writeheader()
        w.writerows(folder_rows)

    object_fields = [
        "root_title", "parent_path", "parent_drive_id", "drive_id", "name",
        "mime_type", "size", "created_time", "modified_time",
    ]
    with OBJECT_OUT.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=object_fields)
        w.writeheader()
        w.writerows(object_rows)

    errors = sum(r["status"] != "PASS" for r in folder_rows)
    summary = {
        "root_count": len(roots),
        "folder_occurrences": folder_occurrences,
        "unique_folder_ids": len(globally_seen_folders),
        "document_occurrences": object_occurrences,
        "unique_document_object_ids": len(globally_seen_objects),
        "folder_errors": errors,
        "all_pagination_exhausted": errors == 0 and all(r["pagination_exhausted"] for r in folder_rows),
        "status": "PASS" if errors == 0 else "FAIL",
    }
    SUMMARY_OUT.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(summary, sort_keys=True))
    return 0 if errors == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
