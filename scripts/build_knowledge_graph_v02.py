#!/usr/bin/env python3
"""Build AkashicNET graph expansion v0.2 from the reconciled Drive census.

Default execution uses the exact 195-node Library Mapping boundary:

  66 root nodes
+121 persisted descendant census nodes
+  7 Gospels descendants recovered in validation batch 0010
+  1 Niels Bohr reconciliation node from validation batch 0011
=195 unique Drive folder nodes

Validation batches also carry corrected observations for already-known nodes. Rows
are deduplicated by immutable Drive ID; later reconciliation observations win for
the current-state view while every observation is preserved as provenance.

Usage:
  python scripts/build_knowledge_graph_v02.py

Optional custom usage:
  python scripts/build_knowledge_graph_v02.py \
    --input path/to/census.csv --input path/to/overlay.csv \
    --output data/knowledge-graph-v0.2.json \
    --expected-drive-nodes 195
"""

from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from datetime import date
from pathlib import Path
from typing import Any, Dict, List

DEFAULT_INPUTS = [
    Path("references/community/drive-metadata-root-census.csv"),
    Path("references/community/drive-metadata-descendant-census.csv"),
    Path("references/community/drive-validation-descendant-batch-0010.csv"),
    Path("references/community/drive-validation-descendant-batch-0011.csv"),
]
DEFAULT_OUTPUT = Path("data/knowledge-graph-v0.2.json")
DEFAULT_EXPECTED = 195


def read_rows(paths: List[Path]) -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for path in paths:
        if not path.exists():
            raise FileNotFoundError(path)
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


def parse_int(value: str) -> int | None:
    value = value.strip()
    return int(value) if value.isdigit() else None


def normalise_row(row: Dict[str, str]) -> Dict[str, Any] | None:
    drive_id = pick(row, "drive_id", "id", "record_id")
    if not drive_id:
        return None

    # Root census uses root_title; descendant/validation files use collection_path.
    root_title = pick(row, "root_title")
    collection_path = pick(row, "collection_path", "path", "title", "root_title")
    parent_root = pick(row, "parent_root", "root", "collection") or root_title

    direct_documents = pick(
        row,
        "observed_direct_documents",
        "direct_documents",
    )
    child_folders = pick(
        row,
        "observed_child_folders",
        "child_folders",
        "direct_folders",
    )

    status = pick(
        row,
        "validation_status",
        "count_status",
        "document_count_status",
    )

    node_state = pick(row, "node_state")
    if root_title and not node_state:
        node_state = "ROOT"

    return {
        "drive_id": drive_id,
        "collection_path": collection_path,
        "parent_root": parent_root,
        "direct_documents": parse_int(direct_documents),
        "child_folders": parse_int(child_folders),
        "count_status": status,
        "node_state": node_state,
        "technical_exclusions_known": pick(row, "technical_exclusions_known", "known_direct_technical_exclusions"),
        "notes": pick(row, "notes"),
        "source_file": row["_source_file"],
    }


def accepted_status(status: str) -> bool:
    return status in {
        "EXACT",
        "COUNT_EXACT",
        "MATCH_EXACT",
        "MATCH_RECONCILED",
        "MATCH_CORRECTED_CHECKPOINT",
        "MATCH_CORRECTED_LIVE_STATE",
        "MATCH_RECONCILIATION_OVERLAY",
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

    roots = sorted({
        obs[-1]["parent_root"]
        for obs in observations.values()
        if obs[-1]["parent_root"]
    })
    collection_ids = {name: f"collection:{idx:03d}" for idx, name in enumerate(roots, 1)}

    for name in roots:
        nodes.append({
            "node_id": collection_ids[name],
            "node_type": "collection",
            "label": name,
        })

    for drive_id, obs in sorted(observations.items()):
        # Inputs are ordered oldest/base -> newest reconciliation overlay.
        chosen = obs[-1]
        signatures = {
            (
                x["collection_path"],
                x["parent_root"],
                x["direct_documents"],
                x["child_folders"],
                x["count_status"],
            )
            for x in obs
        }
        if len(signatures) > 1:
            conflicts.append({
                "drive_id": drive_id,
                "resolution": "latest_reconciliation_observation_selected",
                "observations": obs,
            })

        node_id = f"drive:{drive_id}"
        nodes.append({
            "node_id": node_id,
            "node_type": "drive_object",
            "drive_id": drive_id,
            "label": chosen["collection_path"] or drive_id,
            "collection_path": chosen["collection_path"],
            "parent_root": chosen["parent_root"],
            "direct_documents": chosen["direct_documents"],
            "child_folders": chosen["child_folders"],
            "count_status": chosen["count_status"],
            "node_state": chosen["node_state"],
            "technical_exclusions_known": chosen["technical_exclusions_known"],
            "notes": chosen["notes"],
            "rights_status": "UNKNOWN_UNVERIFIED",
            "review_state": "accepted" if accepted_status(chosen["count_status"]) else "provisional",
            "provenance_observations": obs,
        })

        root = chosen["parent_root"]
        if root in collection_ids:
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
    expected_match = expected_drive_nodes is None or actual == expected_drive_nodes

    # A hard release invariant: no duplicate Drive node IDs and no edge endpoints
    # referencing missing nodes.
    node_ids = {node["node_id"] for node in nodes}
    duplicate_node_ids = len(node_ids) != len(nodes)
    orphan_edges = [
        edge for edge in edges
        if edge["source"] not in node_ids or edge["target"] not in node_ids
    ]

    integrity = {
        "unique_drive_nodes": actual,
        "expected_drive_nodes": expected_drive_nodes,
        "expected_count_match": expected_match,
        "duplicate_node_ids": duplicate_node_ids,
        "orphan_edge_count": len(orphan_edges),
        "orphan_edges": orphan_edges,
        "reconciliation_conflict_count": len(conflicts),
        "reconciliation_conflicts": conflicts,
        "release_integrity_pass": expected_match and not duplicate_node_ids and not orphan_edges,
    }

    return {
        "schema_version": "0.2",
        "generated_on": str(date.today()),
        "milestone": "AKASHICNET-v0.5.0 — 100% LIBRARY MAPPING COMPLETE",
        "boundary": {
            "root_nodes": 66,
            "persisted_descendant_nodes": 121,
            "gospels_reconciliation_nodes": 7,
            "niels_bohr_reconciliation_nodes": 1,
            "expected_unique_drive_nodes": 195,
        },
        "policy": {
            "provenance_first": True,
            "content_hydration": False,
            "embeddings": False,
            "default_rights_status": "UNKNOWN_UNVERIFIED",
            "public_manifest_requires": "PUBLIC_VERIFIED",
            "catalogue_presence_is_not_endorsement": True,
        },
        "nodes": nodes,
        "edges": edges,
        "integrity": integrity,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input",
        action="append",
        help="Input census/reconciliation CSV; repeatable. Defaults to the four reconciled corpus inputs.",
    )
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    parser.add_argument("--expected-drive-nodes", type=int, default=DEFAULT_EXPECTED)
    args = parser.parse_args()

    paths = [Path(p) for p in args.input] if args.input else DEFAULT_INPUTS
    graph = build_graph(read_rows(paths), args.expected_drive_nodes)

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    integrity = graph["integrity"]
    print(f"unique_drive_nodes={integrity['unique_drive_nodes']}")
    print(f"expected_count_match={integrity['expected_count_match']}")
    print(f"duplicate_node_ids={integrity['duplicate_node_ids']}")
    print(f"orphan_edge_count={integrity['orphan_edge_count']}")
    print(f"release_integrity_pass={integrity['release_integrity_pass']}")

    return 0 if integrity["release_integrity_pass"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
