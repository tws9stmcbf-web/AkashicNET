#!/usr/bin/env python3
"""Audit Google Drive folder pagination and terminality against AkashicNET census files.

Requires an OAuth access token in GOOGLE_DRIVE_ACCESS_TOKEN with read-only Drive scope.
Outputs a CSV suitable for the PAGINATION_AND_TERMINALITY_AUDIT validation gate.
"""

from __future__ import annotations

import csv
import json
import os
import sys
import urllib.parse
import urllib.request
from pathlib import Path

ROOT_CENSUS = Path("references/community/drive-traversal-ledger.csv")
DESC_CENSUS = Path("references/community/drive-metadata-descendant-census.csv")
OUT = Path("references/community/drive-pagination-terminality-audit.csv")
FOLDER_MIME = "application/vnd.google-apps.folder"


def load_nodes():
    nodes = []
    with ROOT_CENSUS.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            nodes.append({
                "scope": "root",
                "path": row["root_title"],
                "drive_id": row["drive_id"],
                "expected_state": row["traversal_state"],
                "expected_documents": "",
                "expected_child_folders": "",
            })
    with DESC_CENSUS.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            nodes.append({
                "scope": "descendant",
                "path": row["collection_path"],
                "drive_id": row["drive_id"],
                "expected_state": row["node_state"],
                "expected_documents": row["direct_documents"],
                "expected_child_folders": row["child_folders"],
            })
    return nodes


def list_all(token: str, parent_id: str):
    page_token = None
    pages = 0
    docs = 0
    folders = 0
    while True:
        q = f"'{parent_id}' in parents and trashed = false"
        params = {
            "q": q,
            "fields": "nextPageToken,files(id,name,mimeType)",
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
        for item in data.get("files", []):
            if item.get("mimeType") == FOLDER_MIME:
                folders += 1
            else:
                docs += 1
        page_token = data.get("nextPageToken")
        if not page_token:
            break
    return pages, docs, folders


def main():
    token = os.environ.get("GOOGLE_DRIVE_ACCESS_TOKEN")
    if not token:
        print("GOOGLE_DRIVE_ACCESS_TOKEN is required", file=sys.stderr)
        return 2

    rows = []
    failures = 0
    for node in load_nodes():
        try:
            pages, docs, folders = list_all(token, node["drive_id"])
            terminal = folders == 0
            expected_docs = node["expected_documents"]
            expected_folders = node["expected_child_folders"]
            counts_match = True
            if expected_docs != "":
                counts_match &= docs == int(expected_docs)
            if expected_folders != "":
                counts_match &= folders == int(expected_folders)
            state_ok = True
            if node["expected_state"] in {"TERMINAL_LEAF", "EMPTY_CONFIRMED"}:
                state_ok = terminal
            status = "PASS" if counts_match and state_ok else "FAIL"
            failures += status == "FAIL"
            rows.append({**node, "pages": pages, "observed_documents": docs,
                         "observed_child_folders": folders, "terminal": terminal,
                         "status": status, "error": ""})
        except Exception as exc:  # persist exceptions; never silently pass
            failures += 1
            rows.append({**node, "pages": "", "observed_documents": "",
                         "observed_child_folders": "", "terminal": "",
                         "status": "ERROR", "error": repr(exc)})

    OUT.parent.mkdir(parents=True, exist_ok=True)
    fields = list(rows[0].keys()) if rows else []
    with OUT.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)

    print(f"audited_nodes={len(rows)} failures={failures} output={OUT}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
