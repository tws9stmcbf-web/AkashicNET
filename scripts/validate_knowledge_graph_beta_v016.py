#!/usr/bin/env python3
"""Fail-closed validator for the v0.16 Knowledge Graph Beta review fixture."""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

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
RELATIONSHIP_CONTRACTS = {
    "HAS_MODEL": (
        "QUESTION",
        "MODEL",
        "ACTIVE",
        "DIRECT_SOURCE_METADATA",
        "SOURCE_ASSERTED",
        "DIRECT_RECORD",
    ),
    "SUPPORTS_MODEL_CANDIDATE": (
        "CLAIM",
        "MODEL",
        "REVIEW_ONLY",
        "INFERRED_CANDIDATE",
        "REVIEW_REQUIRED",
        "HUMAN_REVIEW_CANDIDATE",
    ),
    "COMPETES_WITH_CANDIDATE": (
        "MODEL",
        "MODEL",
        "REVIEW_ONLY_CONTRADICTION",
        "INFERRED_CANDIDATE",
        "REVIEW_REQUIRED",
        "HUMAN_REVIEW_CANDIDATE",
    ),
    "CORRECTS": (
        "NOTICE",
        "SOURCE",
        "CORRECTED_NOT_RETRACTED",
        "DIRECT_SOURCE_METADATA",
        "SOURCE_ASSERTED",
        "DIRECT_RECORD",
    ),
}
PARENT_EDGE_CONTRACTS = {
    ("COMPETES_WITH_CANDIDATE", "HAS_MODEL"): (
        "target_node_id",
        {"source_node_id", "target_node_id"},
        "artifact:bq001-spec:0.1",
        r"^/models/(?:0|[1-9][0-9]*)/model_id$",
    ),
}
PARENT_SOURCE_NODE_CONTRACTS = {
    ("COMPETES_WITH_CANDIDATE", "HAS_MODEL"): (
        "QUESTION",
        "BQ001",
        "artifact:bq001-spec:0.1",
        "/id",
    ),
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
NODE_ID = re.compile(r"^node:[A-Za-z0-9.:-]+$")
EDGE_ID = re.compile(r"^edge:[A-Za-z0-9.:-]+$")
SHA256 = re.compile(r"^[0-9a-f]{64}$")


def resolve_pointer(document, pointer):
    if not isinstance(pointer, str) or not pointer.startswith("/") or pointer == "/":
        raise ValueError("invalid record locator")
    current = document
    for raw_part in pointer[1:].split("/"):
        part = raw_part.replace("~1", "/").replace("~0", "~")
        if isinstance(current, list):
            if not re.fullmatch(r"(?:0|[1-9][0-9]*)", part):
                raise ValueError("invalid array index in record locator")
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
            return None
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
            return None
        try:
            return resolve_pointer(governed[artifact_id]["data"], provenance.get("record_locator"))
        except (KeyError, IndexError, ValueError, TypeError):
            errors.append("record locator")
            return None

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
        if not isinstance(node_id, str) or not NODE_ID.fullmatch(node_id) or node.get("node_type") not in NODE_TYPES or not isinstance(node.get("record_id"), str) or not node["record_id"] or not isinstance(node.get("label"), str) or not node["label"]:
            errors.append("nodes")
        if node.get("node_type") == "QUESTION" and node.get("question_status") != "UNRESOLVED":
            errors.append("question node")
        if node.get("node_type") != "QUESTION" and "question_status" in node:
            errors.append("question node")
        resolved_record = check_provenance(node.get("provenance"))
        if resolved_record is not None and resolved_record != node.get("record_id"):
            errors.append("record identity")
    if None in node_ids or len(node_ids) != len(set(node_ids)):
        errors.append("node IDs")
    nodes_by_id = {
        node.get("node_id"): node
        for node in nodes
        if isinstance(node, dict) and isinstance(node.get("node_id"), str)
    }

    edges = data.get("edges")
    if not isinstance(edges, list) or not edges:
        errors.append("edges")
        edges = []
    edge_ids = []
    edges_by_id = {
        edge.get("edge_id"): edge
        for edge in edges
        if isinstance(edge, dict) and isinstance(edge.get("edge_id"), str)
    }

    def traceable_independence_keys(edge_id, visiting=None):
        edge = edges_by_id.get(edge_id)
        if edge is None:
            return set()
        visiting = set() if visiting is None else visiting
        if edge_id in visiting:
            return set()
        visiting = visiting | {edge_id}
        provenance = edge.get("provenance")
        keys = {
            provenance.get("independence_key")
        } if isinstance(provenance, dict) and isinstance(provenance.get("independence_key"), str) else set()
        for parent_id in edge.get("parent_edge_ids", []):
            if isinstance(parent_id, str):
                keys.update(traceable_independence_keys(parent_id, visiting))
        return keys

    declared_independence = {spec["independence_key"] for spec in SOURCE_SPECS.values()}
    for edge in edges:
        if not isinstance(edge, dict):
            errors.append("edges")
            continue
        edge_id = edge.get("edge_id")
        edge_ids.append(edge_id)
        if not isinstance(edge_id, str) or not EDGE_ID.fullmatch(edge_id) or edge.get("relationship_type") not in RELATIONSHIPS:
            errors.append("edges")
        if edge.get("source_node_id") not in node_ids or edge.get("target_node_id") not in node_ids:
            errors.append("edge endpoints")
        if edge.get("source_node_id") == edge.get("target_node_id"):
            errors.append("self edge")
        if edge.get("accepted_edge") is not False:
            errors.append("accepted edges prohibited")

        raw_edge_provenance = edge.get("provenance")
        edge_provenance = (
            raw_edge_provenance
            if isinstance(raw_edge_provenance, dict)
            else {}
        )
        assertion = edge.get("assertion_class")
        if assertion == "INFERRED_CANDIDATE":
            if edge.get("review_state") != "REVIEW_REQUIRED" or edge.get("edge_state") not in {"REVIEW_ONLY", "REVIEW_ONLY_CONTRADICTION"} or edge_provenance.get("derivation_method") != "HUMAN_REVIEW_CANDIDATE":
                errors.append("inferred review boundary")
        elif assertion == "DIRECT_SOURCE_METADATA":
            if edge.get("review_state") != "SOURCE_ASSERTED" or edge_provenance.get("derivation_method") != "DIRECT_RECORD":
                errors.append("direct metadata boundary")
        else:
            errors.append("assertion class")

        relationship = edge.get("relationship_type")
        contract = RELATIONSHIP_CONTRACTS.get(relationship)
        source_node = nodes_by_id.get(edge.get("source_node_id"))
        target_node = nodes_by_id.get(edge.get("target_node_id"))
        if (
            relationship == "COMPETES_WITH_CANDIDATE"
            and isinstance(source_node, dict)
            and isinstance(target_node, dict)
            and source_node.get("record_id") == target_node.get("record_id")
        ):
            errors.append("semantic self edge")
        if contract is None or source_node is None or target_node is None:
            errors.append("relationship contract")
        else:
            (
                source_type,
                target_type,
                edge_state,
                assertion_class,
                review_state,
                derivation_method,
            ) = contract
            if (source_node.get("node_type"), target_node.get("node_type")) != (source_type, target_type):
                errors.append("relationship endpoint types")
            if edge.get("edge_state") != edge_state:
                errors.append("relationship state")
            if (
                edge.get("assertion_class") != assertion_class
                or edge.get("review_state") != review_state
                or edge_provenance.get("derivation_method") != derivation_method
            ):
                errors.append("relationship assertion contract")

        independence = edge.get("evidence_independence_keys")
        traceable_independence = traceable_independence_keys(edge_id)
        if (
            not isinstance(independence, list)
            or not independence
            or len(independence) != len(set(independence))
            or not set(independence).issubset(declared_independence)
            or set(independence) != traceable_independence
        ):
            errors.append("evidence independence")
        parents = edge.get("parent_edge_ids")
        if not isinstance(parents, list) or len(parents) != len(set(parents)):
            errors.append("edge ancestry")
        elif parents:
            if edge.get("assertion_class") != "INFERRED_CANDIDATE":
                errors.append("edge ancestry policy")
            child_endpoints = {edge.get("source_node_id"), edge.get("target_node_id")}
            for parent_id in parents:
                parent = edges_by_id.get(parent_id)
                if parent is None:
                    continue
                parent_endpoints = {parent.get("source_node_id"), parent.get("target_node_id")}
                parent_contract = PARENT_EDGE_CONTRACTS.get(
                    (edge.get("relationship_type"), parent.get("relationship_type"))
                )
                if parent_contract is None:
                    errors.append("edge ancestry policy")
                    continue
                (
                    parent_role,
                    child_roles,
                    required_artifact_id,
                    required_record_locator,
                ) = parent_contract
                source_contract = PARENT_SOURCE_NODE_CONTRACTS.get(
                    (edge.get("relationship_type"), parent.get("relationship_type"))
                )
                allowed_child_endpoints = {edge.get(role) for role in child_roles}
                raw_parent_provenance = parent.get("provenance")
                parent_provenance = (
                    raw_parent_provenance
                    if isinstance(raw_parent_provenance, dict)
                    else {}
                )
                parent_source_node = nodes_by_id.get(parent.get("source_node_id"))
                raw_parent_source_provenance = (
                    parent_source_node.get("provenance")
                    if isinstance(parent_source_node, dict)
                    else None
                )
                parent_source_provenance = (
                    raw_parent_source_provenance
                    if isinstance(raw_parent_source_provenance, dict)
                    else {}
                )
                if source_contract is None:
                    errors.append("edge ancestry policy")
                    continue
                (
                    required_source_type,
                    required_source_record_id,
                    required_source_artifact_id,
                    required_source_record_locator,
                ) = source_contract
                if (
                    parent.get("assertion_class") != "DIRECT_SOURCE_METADATA"
                    or child_endpoints.isdisjoint(parent_endpoints)
                    or parent.get(parent_role) not in allowed_child_endpoints
                    or (
                        edge.get("relationship_type") == "COMPETES_WITH_CANDIDATE"
                        and isinstance(source_node, dict)
                        and isinstance(target_node, dict)
                        and source_node.get("record_id") == target_node.get("record_id")
                    )
                    or parent_provenance.get("artifact_id") != required_artifact_id
                    or not re.fullmatch(
                        required_record_locator,
                        str(parent_provenance.get("record_locator", "")),
                    )
                    or parent_source_node is None
                    or parent_source_node.get("node_type") != required_source_type
                    or parent_source_node.get("record_id") != required_source_record_id
                    or parent_source_provenance.get("artifact_id") != required_source_artifact_id
                    or parent_source_provenance.get("record_locator") != required_source_record_locator
                ):
                    errors.append("edge ancestry policy")
        resolved_record = check_provenance(edge.get("provenance"))
        if resolved_record is not None and source_node is not None and target_node is not None:
            if relationship in {"HAS_MODEL", "SUPPORTS_MODEL_CANDIDATE"}:
                if resolved_record != target_node.get("record_id"):
                    errors.append("record identity")
            elif relationship == "CORRECTS":
                if resolved_record != source_node.get("record_id"):
                    errors.append("record identity")
            elif relationship == "COMPETES_WITH_CANDIDATE":
                model_ids = {
                    model.get("model_id")
                    for model in resolved_record
                    if isinstance(model, dict)
                } if isinstance(resolved_record, list) else set()
                if not {source_node.get("record_id"), target_node.get("record_id")}.issubset(model_ids):
                    errors.append("record identity")

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
