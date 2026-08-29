#!/usr/bin/env python3
"""Build AkashicNET graph expansion v0.2 from census CSVs.

The builder is intentionally provenance-first. It creates collection nodes and
Drive-object nodes from one or more census CSV files and preserves unresolved
metadata rather than inventing canonical relationships.

Usage:
  python scripts/build_knowledge_graph_v02.py \
    --input references/community/drive-metadata-descendant-census.csv \
    --input <root-census.csv> \
    --output data/knowledge-graph-v0.2.json \
    --expected-drive-nodes 195

Additional reconciliation/overlay CSVs can be supplied with repeated --input.
Rows are deduplicated by Drive ID; conflicting metadata is retained in a
`provenance_observations` array and reported in `integrity.conflicts`.
"""

from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from datetime import date
from pathlib import Path
from typing import Dict, List, Any


def read_rows(paths: List[Path]) -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for path in paths:
        with path.open("r", encoding="utf-8-sig", newline="") as fh:
            for row in csv.DictReader(fh):
                row["_source_file"] = str(path)
                rows.append(row)
    return rows


def pick(row: Dict[str, str], *names: str) -> str:
    for name in names:
        value = row.get(name)
        if value not in (None, ""):
            return str(value)
    return ""


def normalise_row(row: Dict[str, str]) -> Dict[str, Any] | None:
    drive_id = pick(row, "drive_id", "id", "record_id")
    if not drive_id:
        return None
    path = pick(row, "collection_path", "path", "title")
    root = pick(row, "parent_root", "root", "collection")
    direct_documents = pick(row, "direct_documents", "observed_direct_documents")
    child_folders = pick(row, "child_folders", "observed_child_folders")
    return {
        "drive_id": drive_id,
        "collection_path": path,
        "parent_root": root,
        "direct_documents": int(direct_documents) if direct_documents.isdigit() else None,
        "child_folders": int(child_folders) if child_folders.isdigit() else None,
        "count_status": pick(row, "count_status", "validation_status"),
        "node_state": pick(row, "node_state"),
        "technical_exclusions_known": pick(row, "technical_exclusions_known"),
        "notes": pick(row, "notes"),
        "source_file": row["_source_file"],
    }


def build_graph(rows: List[Dict[str, str]], expected_drive_nodes: int | None) -> Dict[str, Any]:
    observations: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    for raw in rows:
        item = normalise_row(raw)
        if item:
            observations[item["drive_id"]].append(item)

    nodes: List[Dict[str, Any]] = []
    edges: List[Dict[str, Any]] = []
    conflicts: List[Dict[str, Any]] = []
    collection_ids: Dict[str, str] = {}

    for idx, path in enumerate(sorted({o[0]["parent_root"] for o in observations.values() if o[0]["parent_root"]}), 1):
        cid = f"collection:{idx:03d}"
        collection_ids[path] = cid
        nodes.append({"node_id": cid, "node_type": "collection", "label": path})

    for drive_id, obs in sorted(observations.items()):
        chosen = obs[-1]
        unique_signatures = {
            (x["collection_path"], x["parent_root"], x["direct_documents"], x["child_folders"], x["count_status"])
            for x in obs
        }
        if len(unique_signatures) > 1:
            conflicts.append({"drive_id": drive_id, "observations": obs})

        node_id = f"drive:{drive_id}"
        nodes.append({
            "node_id": node_id,
            "node_type": "drive_object",
            "drive_id": drive_id,
            "label": chosen["collection_path"] or drive_id,
            "collection_path": chosen["collection_path"],
            "direct_documents": chosen["direct_documents"],
            "child_folders": chosen["child_folders"],
            "count_status": chosen["count_status"],
            "node_state": chosen["node_state"],
            "technical_exclusions_known": chosen["technical_exclusions_known"],
            "notes": chosen["notes"],
            "rights_status": "UNKNOWN_UNVERIFIED",
            "review_state": "accepted" if chosen["count_status"] in {"EXACT", "MATCH_EXACT", "MATCH_RECONCILED", "MATCH_CORRECTED_LIVE_STATE", "MATCH_RECONCILIATION_OVERLAY"} else "provisional",
            "provenance_observations": obs,
        })
        root = chosen["parent_root"]
        if root and root in collection_ids:
            edges.append({
                "edge_id": f"contains:{collection_ids[root]}:{drive_id}",
                "source": collection_ids[root],
                "target": node_id,
                "relationship": "CONTAINS",
                "confidence": "high",
                "basis": "census_metadata",
                "review_state": "accepted",
            })

    actual = len(observations)
    integrity = {
        "unique_drive_nodes": actual,
        "expected_drive_nodes": expected_drive_nodes,
        "expected_count_match": expected_drive_nodes is None or actual == expected_drive_nodes,
        "conflict_count": len(conflicts),
        "conflicts": conflicts,
    }

    return {
        "schema_version": "0.2",
        "generated_on": str(date.today()),
        "policy": {
            "provenance_first": True,
            "content_hydration": False,
            "embeddings": False,
            "default_rights_status": "UNKNOWN_UNVERIFIED",
            "public_manifest_requires": "PUBLIC_VERIFIED",
        },
        "nodes": nodes,
        "edges": edges,
        "integrity": integrity,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", action="append", required=True, help="Input census/reconciliation CSV; repeatable")
    parser.add_argument("--output", required=True)
    parser.add_argument("--expected-drive-nodes", type=int, default=None)
    args = parser.parse_args()

    paths = [Path(p) for p in args.input]
    graph = build_graph(read_rows(paths), args.expected_drive_nodes)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    integrity = graph["integrity"]
    print(f"unique_drive_nodes={integrity['unique_drive_nodes']}")
    print(f"expected_count_match={integrity['expected_count_match']}")
    print(f"conflict_count={integrity['conflict_count']}")
    return 0 if integrity["expected_count_match"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
