"""Explicit public metadata projection; never a loader for the private-local CLI.

Approval flags are assertions by the trusted snapshot publisher, not evidence
of permission. Unapproved rows disappear before joins, matching and ranking.
Only fields constructed below can enter the shared retrieval algorithms.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

from check_public_data_boundary import validate_entry
from retrieval_evidence_v01 import classification, edge_classification


class InvalidPublicSnapshot(ValueError):
    """Do not expose details, paths, rejected values, or record counts."""


def require(condition):
    if not condition:
        raise InvalidPublicSnapshot("Invalid public snapshot")


def text(value):
    require(isinstance(value, str) and bool(value.strip()) and len(value) <= 2048)
    require(not any(ord(c) < 32 for c in value))
    # Supplement the repository scanner: it deliberately allows some synthetic
    # and short object references that a runtime public interface must reject.
    require(not any(marker in value.casefold() for marker in (
        "drive.google.com", "docs.google.com", "drive:file:", "drive:folder:",
        "/my drive/", "file://", "/home/", "/users/", "akm-",
    )))
    return value


def identifier(value):
    value = text(value)
    require(bool(re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9:._-]{0,255}", value)))
    require(not value.lower().startswith(("sha256:", "manifestation:", "drive:")))
    return value


def strings(value, convert=text):
    require(isinstance(value, list) and bool(value))
    return [convert(item) for item in value]


def integer(value, minimum=0):
    require(type(value) is int and value >= minimum)
    return value


def approve(row, record_id):
    require(isinstance(row, dict))
    require(row.get("public_safe") is True and row.get("metadata_eligible") is True)
    provenance = row.get("provenance")
    require(isinstance(provenance, dict))
    require(set(provenance) == {"artifact_id", "record_id", "independence_key", "public_safe"})
    require(provenance["public_safe"] is True)
    for key in ("artifact_id", "record_id", "independence_key"):
        identifier(provenance[key])
    require(provenance["artifact_id"].startswith("artifact:"))
    require(provenance["independence_key"].startswith("source:"))
    require(provenance["record_id"] == record_id)
    for key in ("truth_inference_allowed", "rights_promotion_allowed",
                "scientific_evidence_promotion_allowed", "automated_acceptance_allowed"):
        require(key not in row or row[key] is False)
    return dict(provenance)


def project_node(row):
    node_id = identifier(row["node_id"])
    approve(row, node_id)
    require(row.get("node_type") in {"canonical_family", "canonical_candidate_family"})
    return {"node_id": node_id, "family_id": identifier(row.get("family_id", node_id)),
            "node_type": row["node_type"], "label": text(row["label"])}


def project_concept(row):
    node_id = identifier(row["node_id"])
    approve(row, node_id)
    return {"node_id": node_id, "label": text(row["label"]),
            "definition": text(row["definition"])}


def decision_fields(row):
    state = row.get("review_state")
    require(state in {"ACCEPTED", "HOLD", "REJECT", "REVIEW_REQUIRED", "PROVISIONAL"})
    require(row.get("accepted_edge") is (state == "ACCEPTED"))
    expected = "ACCEPT" if state == "ACCEPTED" else "HOLD" if state in {"REVIEW_REQUIRED", "PROVISIONAL"} else state
    result = {"review_state": state, "accepted_edge": row["accepted_edge"]}
    for key in ("v011_decision", "v020_decision", "v021_decision"):
        if key in row and row[key] is not None:
            require(row[key] == expected)
            result[key] = row[key]
    return result


def project_representation(row):
    review_id = identifier(row["review_id"])
    provenance = approve(row, review_id)
    result = {"original_source_ref": identifier(row["original_source_ref"]),
            "review_id": review_id, "provenance": provenance,
            **decision_fields(row)}
    if any(key in row for key in ("evidence_status", "evidence")):
        result["evidence_status"] = classification(row)
    return result


def project_edge(row, library=False):
    review_id = identifier(row["review_id"])
    provenance = approve(row, review_id)
    result = {"target_concept": identifier(row["target_concept"]),
              "review_id": review_id, "provenance": provenance,
              "relationship": text(row["relationship"]), **decision_fields(row)}
    require(result["relationship"] in {"ABOUT", "ABOUT_CANDIDATE"})
    require(result["relationship"] == ("ABOUT" if result["accepted_edge"] else "ABOUT_CANDIDATE"))
    if library:
        result["logical_family_id"] = identifier(row["logical_family_id"])
        result["basis_set"] = strings(row["basis_set"])
        terms = row.get("matched_terms", [])
        require(isinstance(terms, list))
        result["matched_terms"] = [text(x) for x in terms]
        reps = row["representation_sources"]
        require(isinstance(reps, list) and bool(reps))
        # Do not silently turn a partially private/ambiguous review into a
        # public assertion. Every representation must have its own approval.
        result["representation_sources"] = [project_representation(x) for x in reps]
        require(result["accepted_edge"] is any(x["accepted_edge"] for x in result["representation_sources"]))
        require(row["representation_count"] == len(reps) and type(row["representation_count"]) is int)
        result["representation_count"] = len(reps)
    else:
        # Public stable source reference, not a private file link or pathname.
        result["source_ref"] = identifier(row["source_ref"])
        result["basis"] = text(row["basis"])
    result["evidence_status"] = edge_classification(row) if library else classification(row)
    return result


def project_unit(row):
    unit_id = identifier(row["retrieval_unit_id"])
    # Never publish a raw digest/provider-derived legacy unit identifier.
    require(unit_id.startswith(("public:unit:", "synthetic:unit:")))
    approve(row, unit_id)
    require(row["collapse_basis"] in {"SHA256_MATCH_VERIFIED", "NOT_COLLAPSED_NO_HASH_IDENTITY"})
    require(type(row["deduplicated"]) is bool)
    rights = strings(row["rights_states"], identifier)
    # Metadata eligibility does not grant redistribution rights. The asserted
    # states are preserved verbatim, and no content or object links are exposed.
    return {"retrieval_unit_id": unit_id, "family_ids": strings(row["family_ids"], identifier),
            "labels": strings(row["labels"]), "collapse_basis": row["collapse_basis"],
            "deduplicated": row["deduplicated"],
            "physical_manifestation_count": integer(row["physical_manifestation_count"], 1),
            "evidence_status": classification(row),
            "rights_states": rights, "sha256": None, "manifestations": [],
            "not_truth_claim": True, "rights_promotion_allowed": False,
            "scientific_evidence_promotion_allowed": False}


def project_rows(rows, projector):
    require(isinstance(rows, list))
    projected = []
    for row in rows:
        try:
            require(isinstance(row, dict))
            projected.append(projector(row))
        except (InvalidPublicSnapshot, KeyError, TypeError):
            # Deliberately no rejection log or rejection count.
            continue
    return projected


def unique(rows, key):
    values = [row[key] for row in rows]
    require(len(values) == len(set(values)))
    return set(values)


def project_snapshot(snapshot):
    require(isinstance(snapshot, dict) and snapshot.get("schema_version") == "public-retrieval-snapshot/0.1")
    nodes = project_rows(snapshot["graph"]["nodes"], project_node)
    unique(nodes, "node_id")
    families = unique(nodes, "family_id")
    concepts = project_rows(snapshot["concept"]["concept_nodes"], project_concept)
    concept_ids = unique(concepts, "node_id")
    reddit = project_rows(snapshot["concept"]["reddit_edges"], project_edge)
    library = project_rows(snapshot["concept"]["library_edges"], lambda row: project_edge(row, True))
    units = project_rows(snapshot["dedup"]["retrieval_units"], project_unit)
    unique(units, "retrieval_unit_id")
    # A multi-family unit is not partly publishable: its labels describe the
    # entire unit. All referenced families must be independently approved.
    units = [row for row in units if set(row["family_ids"]) <= families]
    result = ({"nodes": nodes}, {
        "concept_nodes": concepts,
        "reddit_edges": [row for row in reddit if row["target_concept"] in concept_ids],
        "library_edges": [row for row in library if row["target_concept"] in concept_ids
                          and row["logical_family_id"] in families],
    }, {"retrieval_units": units})
    # Use the existing public-data scanner as an additional check, never
    # return its detailed findings through the query interface.
    require(not validate_entry("public-retrieval-snapshot.json", json.dumps(result)))
    return result


def load_snapshot(path: Path):
    # One read binds both routes to the same generation. No legacy defaults,
    # environment overrides, subprocess fallbacks, or auxiliary corpus reads.
    def reject_duplicates(pairs):
        result = {}
        for key, value in pairs:
            require(key not in result)
            result[key] = value
        return result

    def reject_constant(_):
        raise InvalidPublicSnapshot("Invalid public snapshot")

    snapshot = json.loads(path.read_bytes(), object_pairs_hook=reject_duplicates,
                          parse_constant=reject_constant)
    return project_snapshot(snapshot)
