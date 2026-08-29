#!/usr/bin/env python3
"""Audit Google Drive folder pagination and terminality against the authoritative AkashicNET census files.

Requires a read-only OAuth access token in GOOGLE_DRIVE_ACCESS_TOKEN.
Writes a 195-row CSV suitable for the PAGINATION_AND_TERMINALITY_AUDIT gate.
"""

from __future__ import annotations

import csv
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter
from pathlib import Path

ROOT_CENSUS = Path("references/community/drive-metadata-root-census.csv")
DESC_CENSUS = Path("references/community/drive-metadata-descendant-census.csv")
DESC_RECONCILIATION = Path("references/community/drive-metadata-final-reconciliation.csv")
OUT = Path("references/community/drive-pagination-terminality-audit.csv")
FOLDER_MIME = "application/vnd.google-apps.folder"
EXPECTED_NODE_COUNT = 195
EXPECTED_ROOT_COUNT = 66
EXPECTED_DESCENDANT_COUNT = 129


def normalise_descendant(row):
    return {
        "scope": "descendant",
        "path": row["collection_path"],
        "drive_id": row["drive_id"],
        "expected_state": row["node_state"],
        "expected_documents": row["direct_documents"],
        "expected_child_folders": row["child_folders"],
    }


def load_nodes():
    roots = []
    with ROOT_CENSUS.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            roots.append({
                "scope": "root",
                "path": row["root_title"],
                "drive_id": row["drive_id"],
                "expected_state": "COMPLETE" if int(row["direct_folders"]) else "TERMINAL_LEAF",
                "expected_documents": row["direct_documents"],
                "expected_child_folders": row["direct_folders"],
            })

    descendants_by_id = {}
    with DESC_CENSUS.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            node = normalise_descendant(row)
            descendants_by_id[node["drive_id"]] = node

    # Authoritative correction overlay: replaces corrected existing rows and adds
    # descendant nodes that were omitted from the historical base census.
    with DESC_RECONCILIATION.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            node = normalise_descendant(row)
            descendants_by_id[node["drive_id"]] = node

    descendants = list(descendants_by_id.values())
    if len(roots) != EXPECTED_ROOT_COUNT:
        raise RuntimeError(
            f"root denominator drift: expected {EXPECTED_ROOT_COUNT}, found {len(roots)}"
        )
    if len(descendants) != EXPECTED_DESCENDANT_COUNT:
        raise RuntimeError(
            f"descendant denominator drift after reconciliation: expected {EXPECTED_DESCENDANT_COUNT}, found {len(descendants)}"
        )

    nodes = roots + descendants
    ids = [n["drive_id"] for n in nodes]
    duplicates = sorted(k for k, v in Counter(ids).items() if v > 1)
    if len(nodes) != EXPECTED_NODE_COUNT:
        raise RuntimeError(f"frozen denominator drift: expected {EXPECTED_NODE_COUNT} nodes, found {len(nodes)}")
    if len(set(ids)) != EXPECTED_NODE_COUNT:
        raise RuntimeError(f"duplicate Drive IDs in audit denominator: {duplicates}")
    return nodes


def validate_token_shape(token: str) -> None:
    """Reject obvious non-token input without ever echoing the credential."""
    if any(ch in token for ch in ("\r", "\n")):
        raise RuntimeError("GOOGLE_DRIVE_ACCESS_TOKEN contains line breaks; paste only the access-token value")
    if token.startswith(("HTTP/", "Location:", "GET ")) or "oauthplayground" in token.lower():
        raise RuntimeError("GOOGLE_DRIVE_ACCESS_TOKEN is not an access-token value")
    if len(token.strip()) < 20:
        raise RuntimeError("GOOGLE_DRIVE_ACCESS_TOKEN is unexpectedly short")


def safe_error(exc: Exception) -> str:
    """Return a bounded credential-safe error class/message for persisted ledgers."""
    if isinstance(exc, urllib.error.HTTPError):
        return f"HTTPError(status={exc.code})"
    if isinstance(exc, urllib.error.URLError):
        return f"URLError(reason_type={type(exc.reason).__name__})"
    # urllib/http.client may include a malformed Authorization header in ValueError.
    if isinstance(exc, ValueError):
        return "ValueError(redacted)"
    text = str(exc)
    lowered = text.lower()
    if any(marker in lowered for marker in ("bearer ", "authorization", "oauth", "access_token", "code=")):
        return f"{type(exc).__name__}(redacted)"
    return f"{type(exc).__name__}({text[:240]})"


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
            return {
                "pages": pages,
                "observed_documents": docs,
                "observed_child_folders": folders,
                "pagination_exhausted": True,
                "final_next_page_token_absent": True,
            }


def main():
    token = os.environ.get("GOOGLE_DRIVE_ACCESS_TOKEN")
    if not token:
        print("GOOGLE_DRIVE_ACCESS_TOKEN is required", file=sys.stderr)
        return 2

    try:
        validate_token_shape(token)
    except Exception as exc:
        print(f"credential_error={safe_error(exc)}", file=sys.stderr)
        return 2

    try:
        nodes = load_nodes()
    except Exception as exc:
        print(f"denominator_error={safe_error(exc)}", file=sys.stderr)
        return 2

    rows = []
    failures = 0
    for node in nodes:
        try:
            observed = list_all(token, node["drive_id"])
            docs = observed["observed_documents"]
            folders = observed["observed_child_folders"]
            terminal = folders == 0
            counts_match = (
                docs == int(node["expected_documents"])
                and folders == int(node["expected_child_folders"])
            )
            state_ok = True
            if node["expected_state"] in {"TERMINAL_LEAF", "EMPTY_CONFIRMED"}:
                state_ok = terminal
            status = "PASS" if counts_match and state_ok and observed["pagination_exhausted"] else "FAIL"
            failures += status == "FAIL"
            rows.append({
                **node,
                **observed,
                "terminal_page_seen": observed["pagination_exhausted"],
                "terminal": terminal,
                "counts_match": counts_match,
                "state_ok": state_ok,
                "status": status,
                "error": "",
            })
        except Exception as exc:
            failures += 1
            rows.append({
                **node,
                "pages": "",
                "observed_documents": "",
                "observed_child_folders": "",
                "pagination_exhausted": False,
                "final_next_page_token_absent": False,
                "terminal_page_seen": False,
                "terminal": "",
                "counts_match": False,
                "state_ok": False,
                "status": "ERROR",
                "error": safe_error(exc),
            })

    OUT.parent.mkdir(parents=True, exist_ok=True)
    fields = list(rows[0].keys())
    with OUT.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)

    unique_ids = len({row["drive_id"] for row in rows})
    print(
        f"audited_nodes={len(rows)} unique_ids={unique_ids} failures={failures} output={OUT}"
    )
    return 0 if (len(rows) == EXPECTED_NODE_COUNT and unique_ids == EXPECTED_NODE_COUNT and failures == 0) else 1


if __name__ == "__main__":
    raise SystemExit(main())
