#!/usr/bin/env python3
"""Fail-closed validator for public-safe cross-source edge provenance v0.1."""
from __future__ import annotations

from datetime import datetime
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_FIXTURE = ROOT / "references" / "community" / "cross-source-edge-provenance-fixtures-v0.1.json"
SHA256 = re.compile(r"^[a-f0-9]{64}$")
CLASSES = {"ASSERTED", "DIRECT_METADATA", "INFERRED_CANDIDATE", "HUMAN_ADJUDICATED", "REJECTED_HOLD"}
REVIEW_STATES = {"PROVISIONAL", "REVIEW_REQUIRED", "HOLD", "REJECTED", "ACCEPTED"}
POLICY_KEYS = (
    "truth_inference_allowed",
    "rights_promotion_allowed",
    "scientific_evidence_promotion_allowed",
    "confidence_from_representation_count_allowed",
    "circular_confidence_allowed",
)


def _nonempty(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _valid_timestamp(value: object) -> bool:
    if not isinstance(value, str):
        return False
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return False
    return parsed.tzinfo is not None


def validate(data: dict) -> list[str]:
    errors: list[str] = []
    if not isinstance(data, dict):
        return ["root must be an object"]
    if data.get("schema_version") != "0.1":
        errors.append("schema_version must equal 0.1")

    policy = data.get("policy")
    if not isinstance(policy, dict):
        errors.append("policy must be an object")
        policy = {}
    for key in POLICY_KEYS:
        if policy.get(key) is not False:
            errors.append(f"policy must remain false: {key}")

    artifacts = data.get("artifacts")
    if not isinstance(artifacts, list) or not artifacts:
        errors.append("artifacts must be a non-empty array")
        artifacts = []
    artifact_by_id: dict[str, dict] = {}
    for artifact in artifacts:
        if not isinstance(artifact, dict):
            errors.append("artifact must be an object")
            continue
        aid = artifact.get("artifact_id")
        if not _nonempty(aid) or aid in artifact_by_id:
            errors.append(f"missing or duplicate artifact_id: {aid!r}")
            continue
        artifact_by_id[aid] = artifact
        if not _nonempty(artifact.get("version")):
            errors.append(f"artifact lacks version: {aid}")
        if not SHA256.fullmatch(str(artifact.get("sha256", ""))):
            errors.append(f"invalid artifact sha256: {aid}")
        if not _nonempty(artifact.get("source_domain")):
            errors.append(f"artifact lacks source_domain: {aid}")
        if not _nonempty(artifact.get("independence_key")):
            errors.append(f"artifact lacks independence_key: {aid}")
        if artifact.get("public_safe") is not True:
            errors.append(f"artifact is not explicitly public-safe: {aid}")

    edges = data.get("edges")
    if not isinstance(edges, list) or not edges:
        errors.append("edges must be a non-empty array")
        edges = []
    edge_by_id: dict[str, dict] = {}
    for edge in edges:
        if not isinstance(edge, dict):
            errors.append("edge must be an object")
            continue
        eid = edge.get("edge_id")
        if not _nonempty(eid) or eid in edge_by_id:
            errors.append(f"missing or duplicate edge_id: {eid!r}")
            continue
        edge_by_id[eid] = edge

    for eid, edge in edge_by_id.items():
        assertion_class = edge.get("assertion_class")
        if assertion_class not in CLASSES:
            errors.append(f"unknown assertion_class on {eid}: {assertion_class!r}")
        if not _nonempty(edge.get("relationship")):
            errors.append(f"missing relationship on {eid}")
        if not _valid_timestamp(edge.get("observed_at")):
            errors.append(f"invalid observed_at timestamp on {eid}")
        if edge.get("review_state") not in REVIEW_STATES:
            errors.append(f"unknown review_state on {eid}: {edge.get('review_state')!r}")
        if not isinstance(edge.get("accepted_edge"), bool):
            errors.append(f"accepted_edge must be boolean on {eid}")

        for endpoint in ("source", "target"):
            ref = edge.get(endpoint)
            if not isinstance(ref, dict) or ref.get("artifact_id") not in artifact_by_id or not _nonempty(ref.get("record_id")):
                errors.append(f"unresolvable {endpoint} reference on {eid}")

        confidence_ids = edge.get("confidence_source_artifact_ids")
        if not isinstance(confidence_ids, list) or not confidence_ids:
            errors.append(f"confidence sources must be a non-empty array on {eid}")
            confidence_ids = []
        if len(confidence_ids) != len(set(confidence_ids)):
            errors.append(f"duplicate confidence artifact on {eid}")
        independence_keys: list[str] = []
        for aid in confidence_ids:
            artifact = artifact_by_id.get(aid)
            if artifact is None:
                errors.append(f"unknown confidence artifact on {eid}: {aid}")
                continue
            independence_keys.append(artifact.get("independence_key"))
        if len(independence_keys) != len(set(independence_keys)):
            errors.append(f"duplicate independence_key in confidence sources on {eid}")

        if edge.get("not_truth_claim") is not True:
            errors.append(f"truth boundary missing on {eid}")
        if edge.get("not_scientific_evidence") is not True:
            errors.append(f"scientific-evidence boundary missing on {eid}")
        if edge.get("not_rights_clearance") is not True:
            errors.append(f"rights boundary missing on {eid}")
        if "representation_count" in edge:
            errors.append(f"representation_count cannot contribute to edge confidence: {eid}")

        parents = edge.get("parent_edge_ids")
        if not isinstance(parents, list):
            errors.append(f"parent_edge_ids must be an array on {eid}")
            parents = []
        if len(parents) != len(set(parents)):
            errors.append(f"duplicate parent edge on {eid}")
        if eid in parents:
            errors.append(f"self-parent cycle on {eid}")
        for parent in parents:
            if parent not in edge_by_id:
                errors.append(f"unknown parent edge on {eid}: {parent}")

        generator = edge.get("generator")
        if assertion_class == "INFERRED_CANDIDATE":
            if not isinstance(generator, dict):
                errors.append(f"inferred candidate lacks generator provenance: {eid}")
            else:
                if not _nonempty(generator.get("name")) or not _nonempty(generator.get("version")):
                    errors.append(f"invalid generator identity on {eid}")
                if not SHA256.fullmatch(str(generator.get("parameters_digest", ""))):
                    errors.append(f"invalid generator parameters_digest on {eid}")

        adjudication_ref = edge.get("adjudication_ref")
        if adjudication_ref is not None:
            if not isinstance(adjudication_ref, dict) or adjudication_ref.get("artifact_id") not in artifact_by_id or not _nonempty(adjudication_ref.get("record_id")):
                errors.append(f"unresolvable adjudication reference on {eid}")
        if assertion_class in {"HUMAN_ADJUDICATED", "REJECTED_HOLD"}:
            if not parents or adjudication_ref is None:
                errors.append(f"adjudicated edge lacks candidate lineage or decision reference: {eid}")
        if edge.get("accepted_edge") is True:
            if assertion_class != "HUMAN_ADJUDICATED" or edge.get("review_state") != "ACCEPTED" or adjudication_ref is None or not parents:
                errors.append(f"edge promoted without explicit accepted adjudication: {eid}")

        source = edge.get("source", {}) if isinstance(edge.get("source"), dict) else {}
        target = edge.get("target", {}) if isinstance(edge.get("target"), dict) else {}
        reverse = (target.get("artifact_id"), target.get("record_id"), source.get("artifact_id"), source.get("record_id"))
        for other_id, other in edge_by_id.items():
            if other_id == eid:
                continue
            os = other.get("source", {}) if isinstance(other.get("source"), dict) else {}
            ot = other.get("target", {}) if isinstance(other.get("target"), dict) else {}
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
        parents = edge_by_id[eid].get("parent_edge_ids", [])
        if isinstance(parents, list):
            for parent in parents:
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
        "accepted_edge_count": sum(e.get("accepted_edge") is True for e in data.get("edges", []) if isinstance(e, dict)),
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
