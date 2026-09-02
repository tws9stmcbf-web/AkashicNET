#!/usr/bin/env python3
"""Fail-closed validation for cross-source review batch v0.1.1."""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.validate_cross_source_edge_provenance_v01 import validate as validate_contract

BATCH = ROOT / "references/community/cross-source-review-batch-v0.1.1.json"
REDDIT = ROOT / "references/community/n2n-test-batch-25.csv"
DRIVE_SEED = ROOT / "references/community/knowledge-graph-seed-v0.1.md"

REDDIT_ARTIFACT = "artifact:reddit-n2n-test-batch-25:2026-09-02"
DRIVE_ARTIFACT = "artifact:drive-knowledge-graph-seed:0.1"
EXPECTED_EDGES = 3
FORBIDDEN_KEYS = {
    "drive_id",
    "drive_object_id",
    "file_id",
    "filename",
    "path",
    "parent_path",
    "private_path",
    "object_hash",
}
FORBIDDEN_VALUES = ("/My Drive/", "drive.google.com/open?id=", "AKM-")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def walk(value: Any):
    if isinstance(value, dict):
        for key, item in value.items():
            yield key, item
            yield from walk(item)
    elif isinstance(value, list):
        for item in value:
            yield from walk(item)


def validate_batch(data: dict) -> list[str]:
    errors = list(validate_contract(data))
    artifacts = {a.get("artifact_id"): a for a in data.get("artifacts", []) if isinstance(a, dict)}
    expected_hashes = {
        REDDIT_ARTIFACT: sha256(REDDIT),
        DRIVE_ARTIFACT: sha256(DRIVE_SEED),
    }
    if set(artifacts) != set(expected_hashes):
        errors.append("batch must cite exactly the approved Reddit and Drive public-safe inputs")
    for artifact_id, expected in expected_hashes.items():
        if artifacts.get(artifact_id, {}).get("sha256") != expected:
            errors.append(f"source digest mismatch: {artifact_id}")

    edges = data.get("edges", [])
    if len(edges) != EXPECTED_EDGES:
        errors.append(f"batch must contain exactly {EXPECTED_EDGES} edges")
    edge_ids = {e.get("edge_id") for e in edges if isinstance(e, dict)}
    if len(edge_ids) != len(edges):
        errors.append("edge IDs must be unique")

    reddit_text = REDDIT.read_text(encoding="utf-8")
    drive_text = DRIVE_SEED.read_text(encoding="utf-8")
    for edge in edges:
        if not isinstance(edge, dict):
            continue
        edge_id = edge.get("edge_id", "<unknown>")
        required = {
            "assertion_class": "INFERRED_CANDIDATE",
            "review_state": "REVIEW_REQUIRED",
            "accepted_edge": False,
            "not_truth_claim": True,
            "not_scientific_evidence": True,
            "not_rights_clearance": True,
        }
        for key, expected in required.items():
            if edge.get(key) != expected:
                errors.append(f"{edge_id}: {key} must be {expected!r}")
        if edge.get("parent_edge_ids") != []:
            errors.append(f"{edge_id}: first-pass candidate must have no graph-derived parents")
        if edge.get("confidence_source_artifact_ids") != [REDDIT_ARTIFACT, DRIVE_ARTIFACT]:
            errors.append(f"{edge_id}: confidence sources must cite both inputs once in fixed order")
        source = edge.get("source", {})
        target = edge.get("target", {})
        if source.get("artifact_id") != REDDIT_ARTIFACT or source.get("record_id") not in reddit_text:
            errors.append(f"{edge_id}: unresolved Reddit source record")
        if target.get("artifact_id") != DRIVE_ARTIFACT or target.get("record_id") not in drive_text:
            errors.append(f"{edge_id}: unresolved Drive public-family target")
        if "adjudication_ref" in edge:
            errors.append(f"{edge_id}: candidate batch cannot embed adjudication")

    for key, value in walk(data):
        if str(key).lower() in FORBIDDEN_KEYS:
            errors.append(f"private-boundary key prohibited: {key}")
        if isinstance(value, str) and any(marker in value for marker in FORBIDDEN_VALUES):
            errors.append("private-boundary value prohibited")

    policy = data.get("policy", {})
    if any(policy.get(key) is not False for key in (
        "truth_inference_allowed",
        "rights_promotion_allowed",
        "scientific_evidence_promotion_allowed",
        "confidence_from_representation_count_allowed",
        "circular_confidence_allowed",
    )):
        errors.append("all non-promotion policy switches must remain false")
    return sorted(set(errors))


def main() -> int:
    data = json.loads(BATCH.read_text(encoding="utf-8"))
    errors = validate_batch(data)
    summary = {
        "candidate_count": len(data.get("edges", [])),
        "accepted_edge_count": sum(e.get("accepted_edge") is True for e in data.get("edges", [])),
        "source_artifact_count": len(data.get("artifacts", [])),
        "truth_inference_allowed": False,
        "circular_confidence_allowed": False,
    }
    print(json.dumps(summary, sort_keys=True))
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("AKASHICNET CROSS-SOURCE REVIEW BATCH v0.1.1 PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
