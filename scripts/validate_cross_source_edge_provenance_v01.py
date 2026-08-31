#!/usr/bin/env python3
"""Fail-closed validator for public-safe cross-source edge provenance v0.1."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_FIXTURE = ROOT / "references" / "community" / "cross-source-edge-provenance-fixtures-v0.1.json"
SHA256 = re.compile(r"^[a-f0-9]{64}$")
CLASSES = {"ASSERTED", "DIRECT_METADATA", "INFERRED_CANDIDATE", "HUMAN_ADJUDICATED", "REJECTED_HOLD"}


def validate(data: dict) -> list[str]:
    errors: list[str] = []
    policy = data.get("policy", {})
    for key in (
        "truth_inference_allowed",
        "rights_promotion_allowed",
        "scientific_evidence_promotion_allowed",
        "confidence_from_representation_count_allowed",
        "circular_confidence_allowed",
    ):
        if policy.get(key) is not False:
            errors.append(f"policy must remain false: {key}")

    artifacts = data.get("artifacts", [])
    artifact_by_id: dict[str, dict] = {}
    for artifact in artifacts:
        aid = artifact.get("artifact_id")
        if not aid or aid in artifact_by_id:
            errors.append(f"missing or duplicate artifact_id: {aid!r}")
            continue
        artifact_by_id[aid] = artifact
        if not SHA256.fullmatch(str(artifact.get("sha256", ""))):
            errors.append(f"invalid artifact sha256: {aid}")
        if artifact.get("public_safe") is not True:
            errors.append(f"artifact is not explicitly public-safe: {aid}")
        if not artifact.get("independence_key"):
            errors.append(f"artifact lacks independence_key: {aid}")

    edges = data.get("edges", [])
    edge_by_id: dict[str, dict] = {}
    for edge in edges:
        eid = edge.get("edge_id")
        if not eid or eid in edge_by_id:
            errors.append(f"missing or duplicate edge_id: {eid!r}")
            continue
        edge_by_id[eid] = edge

    for eid, edge in edge_by_id.items():
        assertion_class = edge.get("assertion_class")
        if assertion_class not in CLASSES:
            errors.append(f"unknown assertion_class on {eid}: {assertion_class!r}")
        for endpoint in ("source", "target"):
            ref = edge.get(endpoint, {})
            if ref.get("artifact_id") not in artifact_by_id or not ref.get("record_id"):
                errors.append(f"unresolvable {endpoint} reference on {eid}")
        for aid in edge.get("confidence_source_artifact_ids", []):
            if aid not in artifact_by_id:
                errors.append(f"unknown confidence artifact on {eid}: {aid}")
        if edge.get("not_truth_claim") is not True:
            errors.append(f"truth boundary missing on {eid}")
        if edge.get("not_scientific_evidence") is not True:
            errors.append(f"scientific-evidence boundary missing on {eid}")
        if edge.get("not_rights_clearance") is not True:
            errors.append(f"rights boundary missing on {eid}")
        if "representation_count" in edge:
            errors.append(f"representation_count cannot contribute to edge confidence: {eid}")

        parents = edge.get("parent_edge_ids", [])
        if eid in parents:
            errors.append(f"self-parent cycle on {eid}")
        for parent in parents:
            if parent not in edge_by_id:
                errors.append(f"unknown parent edge on {eid}: {parent}")

        if assertion_class == "INFERRED_CANDIDATE" and not edge.get("generator"):
            errors.append(f"inferred candidate lacks generator provenance: {eid}")
        if assertion_class in {"HUMAN_ADJUDICATED", "REJECTED_HOLD"}:
            if not parents or not edge.get("adjudication_ref"):
                errors.append(f"adjudicated edge lacks candidate lineage or decision reference: {eid}")
        if edge.get("accepted_edge") is True:
            if assertion_class != "HUMAN_ADJUDICATED" or edge.get("review_state") != "ACCEPTED" or not edge.get("adjudication_ref"):
                errors.append(f"edge promoted without explicit accepted adjudication: {eid}")

        source = edge.get("source", {})
        target = edge.get("target", {})
        reverse = (target.get("artifact_id"), target.get("record_id"), source.get("artifact_id"), source.get("record_id"))
        for other_id, other in edge_by_id.items():
            if other_id == eid:
                continue
            os = other.get("source", {})
            ot = other.get("target", {})
            forward = (os.get("artifact_id"), os.get("record_id"), ot.get("artifact_id"), ot.get("record_id"))
            if forward == reverse and other_id in parents:
                errors.append(f"reverse-edge feedback loop: {eid} -> {other_id}")

    visiting: set[str] = set()
    visited: set[str] = set()

    def walk(eid: str) -> None:
        if eid in visiting:
            errors.append(f"cyclic edge lineage detected at {eid}")
            return
        if eid in visited or eid not in edge_by_id:
            return
        visiting.add(eid)
        for parent in edge_by_id[eid].get("parent_edge_ids", []):
            walk(parent)
        visiting.remove(eid)
        visited.add(eid)

    for eid in edge_by_id:
        walk(eid)
    return sorted(set(errors))


def main() -> int:
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_FIXTURE
    data = json.loads(path.read_text(encoding="utf-8"))
    errors = validate(data)
    summary = {
        "schema_version": data.get("schema_version"),
        "artifact_count": len(data.get("artifacts", [])),
        "edge_count": len(data.get("edges", [])),
        "accepted_edge_count": sum(e.get("accepted_edge") is True for e in data.get("edges", [])),
        "truth_inference_allowed": False,
        "rights_promotion_allowed": False,
        "scientific_evidence_promotion_allowed": False,
        "circular_confidence_allowed": False,
    }
    print(json.dumps(summary, sort_keys=True))
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("AKASHICNET CROSS-SOURCE EDGE PROVENANCE v0.1 PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
