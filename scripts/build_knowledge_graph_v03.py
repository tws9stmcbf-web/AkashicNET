#!/usr/bin/env python3
"""Overlay Stage-B canonical families onto AkashicNET knowledge graph v0.2.

This never collapses Drive provenance nodes. It adds canonical-family nodes and
explicit relationships from the mapped collection/folder nodes to those family
nodes. Unresolved Stage-B relations remain provisional.
"""
from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from datetime import date
from pathlib import Path

DEFAULT_BASE = Path("data/knowledge-graph-v0.2.json")
DEFAULT_OVERLAY = Path("references/community/drive-canonical-resolution-stage-b-graph-overlay.csv")
DEFAULT_OUTPUT = Path("data/knowledge-graph-v0.3.json")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--base", default=str(DEFAULT_BASE))
    p.add_argument("--overlay", default=str(DEFAULT_OVERLAY))
    p.add_argument("--output", default=str(DEFAULT_OUTPUT))
    p.add_argument("--expected-drive-nodes", type=int, default=195)
    p.add_argument("--expected-family-nodes", type=int, default=14)
    p.add_argument("--expected-advanced-families", type=int, default=13)
    p.add_argument("--expected-unresolved-families", type=int, default=1)
    a = p.parse_args()

    graph = json.loads(Path(a.base).read_text(encoding="utf-8"))
    if not graph.get("integrity", {}).get("release_integrity_pass"):
        raise SystemExit("base graph integrity did not pass")

    path_to_drive = {
        n.get("collection_path"): n["node_id"]
        for n in graph["nodes"]
        if n.get("node_type") == "drive_object" and n.get("collection_path")
    }

    families = defaultdict(list)
    with Path(a.overlay).open("r", encoding="utf-8-sig", newline="") as fh:
        for row in csv.DictReader(fh):
            families[row["family_id"]].append(row)

    missing_paths = []
    canonical_nodes = []
    canonical_edges = []
    unresolved = 0
    advanced = 0

    for family_id, rows in sorted(families.items()):
        first = rows[0]
        review_states = {r["review_state"] for r in rows}
        is_unresolved = "provisional" in review_states or any(
            r["stage_b_disposition"] == "CROSS_COLLECTION_RELATION_UNRESOLVED" for r in rows
        )
        unresolved += int(is_unresolved)
        advanced += int(not is_unresolved)
        node_id = f"canonical_family:{family_id}"
        canonical_nodes.append({
            "node_id": node_id,
            "node_type": "canonical_family",
            "family_id": family_id,
            "label": first["logical_work"],
            "stage_b_disposition": first["stage_b_disposition"],
            "confidence": first["confidence"].lower(),
            "review_state": "provisional" if is_unresolved else "accepted",
            "rights_status": "UNKNOWN_UNVERIFIED",
            "provenance": "Stage-B metadata-only canonical resolution",
        })
        for row in rows:
            source = path_to_drive.get(row["collection_path"])
            if not source:
                missing_paths.append(row["collection_path"])
                continue
            canonical_edges.append({
                "edge_id": f"stage_b:{family_id}:{source}",
                "source": source,
                "target": node_id,
                "relationship": "MEMBER_OF_CANONICAL_FAMILY" if not is_unresolved else "CANDIDATE_MEMBER_OF_CANONICAL_FAMILY",
                "stage_b_disposition": row["stage_b_disposition"],
                "confidence": row["confidence"].lower(),
                "basis": row["evidence_basis"],
                "review_state": row["review_state"],
            })

    graph["schema_version"] = "0.3"
    graph["generated_on"] = str(date.today())
    graph["nodes"].extend(canonical_nodes)
    graph["edges"].extend(canonical_edges)

    node_ids = [n["node_id"] for n in graph["nodes"]]
    node_set = set(node_ids)
    orphan_edges = [e for e in graph["edges"] if e["source"] not in node_set or e["target"] not in node_set]
    drive_nodes = sum(1 for n in graph["nodes"] if n.get("node_type") == "drive_object")
    family_nodes = len(canonical_nodes)

    semantic_pass = (
        drive_nodes == a.expected_drive_nodes
        and family_nodes == a.expected_family_nodes
        and advanced == a.expected_advanced_families
        and unresolved == a.expected_unresolved_families
        and not missing_paths
        and len(node_ids) == len(node_set)
        and not orphan_edges
    )

    graph["canonical_stage_b"] = {
        "family_nodes": family_nodes,
        "advanced_families": advanced,
        "unresolved_families": unresolved,
        "canonical_edges": len(canonical_edges),
        "missing_collection_paths": sorted(set(missing_paths)),
        "policy": "preserve physical Drive provenance; do not infer byte identity without hashes",
    }
    graph["integrity"]["stage_b_semantic_integrity_pass"] = semantic_pass
    graph["integrity"]["release_integrity_pass"] = bool(graph["integrity"].get("release_integrity_pass")) and semantic_pass

    out = Path(a.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"drive_nodes={drive_nodes}")
    print(f"family_nodes={family_nodes}")
    print(f"advanced_families={advanced}")
    print(f"unresolved_families={unresolved}")
    print(f"canonical_edges={len(canonical_edges)}")
    print(f"missing_collection_paths={len(set(missing_paths))}")
    print(f"stage_b_semantic_integrity_pass={semantic_pass}")
    return 0 if semantic_pass else 2


if __name__ == "__main__":
    raise SystemExit(main())
