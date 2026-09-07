#!/usr/bin/env python3
"""Fail-closed validator for the v0.16 Knowledge Graph Beta review fixture."""
import json
import re
from pathlib import Path

from scripts.build_knowledge_graph_beta_fixture_v016 import (
    BOUNDARIES,
    OUTPUT,
    SOURCE_SPECS,
    build,
    load_governed_sources,
)

NODE_TYPES = {"QUESTION", "MODEL", "SOURCE", "CLAIM", "NOTICE"}
RELATIONSHIPS = {
    "HAS_MODEL",
    "SUPPORTS_MODEL_CANDIDATE",
    "COMPETES_WITH_CANDIDATE",
    "CORRECTS",
}
PROVENANCE_KEYS = {
    "artifact_id",
    "repository_path",
    "sha256",
    "record_locator",
    "independence_key",
    "derivation_method",
    "public_safe",
}
FORBIDDEN_KEYS = {
    "drive_id",
    "drive_file_id",
    "drive_object_id",
    "file_id",
    "filename",
    "file_name",
    "path",
    "parent_id",
    "parent_path",
    "parents",
    "private_path",
    "object_hash",
}
FORBIDDEN_MARKERS = ("AKM-", "/My Drive/", "drive.google.com/open?id=")
ID = re.compile(r"^(node|edge):[A-Za-z0-9.:-]+$")
SHA256 = re.compile(r"^[0-9a-f]{64}$")


def resolve_pointer(document, pointer):
    if not isinstance(pointer, str) or not pointer.startswith("/") or pointer == "/":
        raise ValueError("invalid record locator")
    current = document
    for raw_part in pointer[1:].split("/"):
        part = raw_part.replace("~1", "/").replace("~0", "~")
        if isinstance(current, list):
            current = current[int(part)]
        elif isinstance(current, dict):
            current = current[part]
        else:
            raise ValueError("record locator traverses scalar")
    return current


def walk(value):
    if isinstance(value, dict):
        for key, child in value.items():
            yield key
            yield from walk(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk(child)
    else:
        yield value


def has_parent_cycle(edges):
    parents = {edge.get("edge_id"): edge.get("parent_edge_ids", []) for edge in edges}
    visiting, visited = set(), set()

    def visit(edge_id):
        if edge_id in visiting:
            return True
        if edge_id in visited:
            return False
        visiting.add(edge_id)
        for parent in parents.get(edge_id, []):
            if parent in parents and visit(parent):
                return True
        visiting.remove(edge_id)
        visited.add(edge_id)
        return False

    return any(visit(edge_id) for edge_id in parents)


def validate(data):
    errors = []

    try:
        governed = load_governed_sources()
        expected = build(governed)
    except (OSError, ValueError, KeyError, IndexError, TypeError, json.JSONDecodeError):
        governed = {}
        expected = None
        errors.append("governed source structure")

    if expected is not None and data != expected:
        errors.append("deterministic artifact")

    if data.get("schema_version") != "0.16.0-beta.1" or data.get("mode") != "REVIEW_FIXTURE_ONLY" or data.get("issue") != 277:
        errors.append("version or mode")

    expected_locks = {
        "v0.14": "7b6cfd89de570c4b945d574dad570c37825645fe",
        "v0.15_release": "ea46629558ff57970f6efd2485a7e9a288dc55f2",
        "v0.15_seal": "5ba6989aade68461c8f3953c4a82cc0e158b0730",
    }
    if data.get("baseline_locks") != expected_locks:
        errors.append("sealed baseline locks")
    if data.get("question_id") != "BQ001" or data.get("question_status") != "UNRESOLVED":
        errors.append("question status")
    if data.get("boundaries") != BOUNDARIES or any(data.get("boundaries", {}).values()):
        errors.append("unsafe boundaries")

    declared = {}
    source_artifacts = data.get("source_artifacts")
    if not isinstance(source_artifacts, list):
        errors.append("source artifacts")
        source_artifacts = []
    for source in source_artifacts:
        if not isinstance(source, dict):
            errors.append("source artifacts")
            continue
        artifact_id = source.get("artifact_id")
        expected_source = SOURCE_SPECS.get(artifact_id)
        if artifact_id in declared or expected_source is None:
            errors.append("source artifacts")
            continue
        declared[artifact_id] = source
        actual_sha = governed.get(artifact_id, {}).get("sha256")
        if (
            set(source) != {"artifact_id", "repository_path", "sha256", "independence_key", "public_safe"}
            or source.get("repository_path") != expected_source["repository_path"]
            or source.get("sha256") != expected_source["sha256"]
            or actual_sha != expected_source["sha256"]
            or source.get("independence_key") != expected_source["independence_key"]
            or source.get("public_safe") is not True
            or not SHA256.fullmatch(str(source.get("sha256", "")))
        ):
            errors.append("source artifacts")
    if set(declared) != set(SOURCE_SPECS):
        errors.append("source artifacts")

    def check_provenance(provenance):
        if not isinstance(provenance, dict) or set(provenance) != PROVENANCE_KEYS:
            errors.append("provenance")
            return
        artifact_id = provenance.get("artifact_id")
        source = declared.get(artifact_id)
        spec = SOURCE_SPECS.get(artifact_id)
        if (
            source is None
            or spec is None
            or provenance.get("repository_path") != spec["repository_path"]
            or provenance.get("sha256") != spec["sha256"]
            or provenance.get("independence_key") != spec["independence_key"]
            or provenance.get("derivation_method") not in {"DIRECT_RECORD", "HUMAN_REVIEW_CANDIDATE"}
            or provenance.get("public_safe") is not True
        ):
            errors.append("provenance")
            return
        try:
            resolve_pointer(governed[artifact_id]["data"], provenance.get("record_locator"))
        except (KeyError, IndexError, ValueError, TypeError):
            errors.append("record locator")

    nodes = data.get("nodes")
    if not isinstance(nodes, list) or not nodes:
        errors.append("nodes")
        nodes = []
    node_ids = []
    for node in nodes:
        if not isinstance(node, dict):
            errors.append("nodes")
            continue
        node_id = node.get("node_id")
        node_ids.append(node_id)
        if not isinstance(node_id, str) or not ID.fullmatch(node_id) or node.get("node_type") not in NODE_TYPES or not isinstance(node.get("label"), str) or not node["label"]:
            errors.append("nodes")
        if node.get("node_type") == "QUESTION" and node.get("question_status") != "UNRESOLVED":
            errors.append("question node")
        if node.get("node_type") != "QUESTION" and "question_status" in node:
            errors.append("question node")
        check_provenance(node.get("provenance"))
    if None in node_ids or len(node_ids) != len(set(node_ids)):
        errors.append("node IDs")

    edges = data.get("edges")
    if not isinstance(edges, list) or not edges:
        errors.append("edges")
        edges = []
    edge_ids = []
    declared_independence = {spec["independence_key"] for spec in SOURCE_SPECS.values()}
    for edge in edges:
        if not isinstance(edge, dict):
            errors.append("edges")
            continue
        edge_id = edge.get("edge_id")
        edge_ids.append(edge_id)
        if not isinstance(edge_id, str) or not ID.fullmatch(edge_id) or edge.get("relationship_type") not in RELATIONSHIPS:
            errors.append("edges")
        if edge.get("source_node_id") not in node_ids or edge.get("target_node_id") not in node_ids:
            errors.append("edge endpoints")
        if edge.get("source_node_id") == edge.get("target_node_id"):
            errors.append("self edge")
        if edge.get("accepted_edge") is not False:
            errors.append("accepted edges prohibited")

        assertion = edge.get("assertion_class")
        if assertion == "INFERRED_CANDIDATE":
            if edge.get("review_state") != "REVIEW_REQUIRED" or edge.get("edge_state") not in {"REVIEW_ONLY", "REVIEW_ONLY_CONTRADICTION"} or edge.get("provenance", {}).get("derivation_method") != "HUMAN_REVIEW_CANDIDATE":
                errors.append("inferred review boundary")
        elif assertion == "DIRECT_SOURCE_METADATA":
            if edge.get("review_state") != "SOURCE_ASSERTED" or edge.get("provenance", {}).get("derivation_method") != "DIRECT_RECORD":
                errors.append("direct metadata boundary")
        else:
            errors.append("assertion class")

        if edge.get("relationship_type") == "CORRECTS" and edge.get("edge_state") != "CORRECTED_NOT_RETRACTED":
            errors.append("correction state")
        if edge.get("relationship_type") == "COMPETES_WITH_CANDIDATE" and edge.get("edge_state") != "REVIEW_ONLY_CONTRADICTION":
            errors.append("contradiction state")

        independence = edge.get("evidence_independence_keys")
        if not isinstance(independence, list) or not independence or len(independence) != len(set(independence)) or not set(independence).issubset(declared_independence):
            errors.append("evidence independence")
        parents = edge.get("parent_edge_ids")
        if not isinstance(parents, list) or len(parents) != len(set(parents)):
            errors.append("edge ancestry")
        check_provenance(edge.get("provenance"))

    if None in edge_ids or len(edge_ids) != len(set(edge_ids)):
        errors.append("edge IDs")
    if any(parent not in edge_ids for edge in edges if isinstance(edge, dict) for parent in edge.get("parent_edge_ids", [])):
        errors.append("edge ancestry")
    if has_parent_cycle(edges):
        errors.append("circular ancestry")

    expected_summary = {
        "node_count": len(nodes),
        "edge_count": len(edges),
        "accepted_edge_count": sum(edge.get("accepted_edge") is True for edge in edges if isinstance(edge, dict)),
        "inferred_candidate_count": sum(edge.get("assertion_class") == "INFERRED_CANDIDATE" for edge in edges if isinstance(edge, dict)),
        "unresolved_question_count": sum(node.get("node_type") == "QUESTION" and node.get("question_status") == "UNRESOLVED" for node in nodes if isinstance(node, dict)),
    }
    if data.get("summary") != expected_summary or expected_summary["accepted_edge_count"] != 0 or expected_summary["unresolved_question_count"] != 1:
        errors.append("summary")

    for value in walk(data):
        if isinstance(value, str) and (value.lower() in FORBIDDEN_KEYS or any(marker in value for marker in FORBIDDEN_MARKERS)):
            errors.append("private metadata")

    return sorted(set(errors))


def main():
    data = json.loads(OUTPUT.read_text())
    errors = validate(data)
    for error in errors:
        print("ERROR:", error)
    if not errors:
        print("AKASHICNET KNOWLEDGE GRAPH BETA v0.16 PASS")
        print(json.dumps(data["summary"], sort_keys=True))
    return bool(errors)


if __name__ == "__main__":
    raise SystemExit(main())
