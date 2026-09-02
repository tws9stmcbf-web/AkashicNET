#!/usr/bin/env python3
"""Build real, typed, public-safe endpoint records without creating graph edges."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMMUNITY = ROOT / "references/community"
OUTPUT = COMMUNITY / "public-safe-semantic-endpoint-registry-v0.1.9.json"
VERSION = "0.1.9"
TYPES = {"TOPIC", "PUBLICATION", "FRAMEWORK", "QUESTION", "SOURCE_RECORD", "EVIDENCE_RECORD"}
BOUNDARIES = {
    "automated_truth_inference_allowed": False,
    "automated_acceptance_allowed": False,
    "rights_promotion_allowed": False,
    "scientific_evidence_promotion_allowed": False,
    "canonical_identity_promotion_allowed": False,
    "circular_confidence_allowed": False,
    "private_drive_metadata_allowed": False,
}


def digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def norm(value: str) -> str:
    return " ".join(re.findall(r"[a-z0-9]+", value.casefold()))


def slug(value: str) -> str:
    return norm(value).replace(" ", "-")


def endpoint(endpoint_id, endpoint_type, label, assertion_class, evidence_status, identity_state, artifact_id, record_id, independence_key):
    return {
        "endpoint_id": endpoint_id,
        "endpoint_type": endpoint_type,
        "label": label,
        "assertion_class": assertion_class,
        "evidence_status": evidence_status,
        "identity_state": identity_state,
        "provenance": {
            "artifact_id": artifact_id,
            "record_id": record_id,
            "independence_key": independence_key,
            "public_safe": True,
        },
    }


def parse_drive(text: str):
    rows = []
    for line in text.splitlines():
        if not line.startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if len(cells) == 4 and re.fullmatch(r"[A-Z0-9-]+", cells[0]) and cells[0] != "family_id":
            rows.append((cells[0], cells[1]))
    return rows


def build_registry(topics, frameworks, publications, questions, evidence_records, artifacts):
    endpoints = []
    for key, label in sorted(topics.items()):
        endpoints.append(endpoint(f"endpoint:topic:{slug(key)}", "TOPIC", label, "CURATED_PUBLIC_LABEL", "NOT_APPLICABLE", "DISTINCT", "artifact:topic-census:0.7.5", key, "source:topic-census:public-metadata-v0.7.5"))
    for label in sorted(frameworks, key=str.casefold):
        endpoints.append(endpoint(f"endpoint:framework:{slug(label)}", "FRAMEWORK", label, "ASSERTED_SOURCE_METADATA", "NOT_APPLICABLE", "UNRESOLVED", "artifact:reddit-n2n-test-batch-25:public", f"framework:{label}", "source:reddit-index:n2n-test-batch-25"))
    for family_id, title in sorted(publications):
        endpoints.append(endpoint(f"endpoint:drive-publication:{family_id.casefold()}", "PUBLICATION", title, "CURATED_PUBLIC_LABEL", "UNASSESSED", "UNRESOLVED", "artifact:drive-knowledge-graph-seed:0.1", family_id, "source:drive-public-seed:stage-b-v0.1"))
    for qid, question, record in sorted(questions):
        endpoints.append(endpoint(f"endpoint:question:{qid.casefold()}", "QUESTION", question, "CURATED_PUBLIC_LABEL", "NOT_APPLICABLE", "DISTINCT", f"artifact:big-question:{qid.casefold()}:public-synthesis", record, f"source:big-question:{qid.casefold()}"))
    for source_id, title, artifact_id, independence_key in sorted(evidence_records):
        endpoints.append(endpoint(f"endpoint:evidence:{slug(source_id)}", "EVIDENCE_RECORD", title, "CURATED_PUBLIC_LABEL", "SOURCE_CLASSIFICATION_ONLY", "UNRESOLVED", artifact_id, source_id, independence_key))
    endpoints.sort(key=lambda item: item["endpoint_id"])
    counts = {kind: sum(e["endpoint_type"] == kind for e in endpoints) for kind in sorted(TYPES)}
    return {
        "schema_version": VERSION,
        "mode": "ENDPOINT_REGISTRY_ONLY",
        "boundaries": dict(BOUNDARIES),
        "source_artifacts": artifacts,
        "endpoints": endpoints,
        "edges": [],
        "summary": {"endpoint_count": len(endpoints), "counts_by_type": counts, "accepted_edges": 0},
    }


def load_real_inputs():
    from scripts import topic_census_v075 as census

    topic_sources = census.load_ontology() + census.load_wikispine() + census.load_n2n_categories()
    topics = {}
    for label in topic_sources:
        topics.setdefault(census.norm(label), label)
    if len(topics) != 68:
        raise ValueError(f"topic census drift: expected 68, got {len(topics)}")

    reddit_path = COMMUNITY / "n2n-test-batch-25.csv"
    reddit_raw = reddit_path.read_bytes()
    rows = list(csv.DictReader(reddit_raw.decode("utf-8-sig").splitlines()))
    frameworks = {row.get("toolkit_framework", "").strip() for row in rows if row.get("toolkit_framework", "").strip()}

    drive_path = COMMUNITY / "knowledge-graph-seed-v0.1.md"
    drive_raw = drive_path.read_bytes()
    publications = parse_drive(drive_raw.decode())

    architecture_path = ROOT / "references/big-questions/architecture-v0.1.json"
    architecture_raw = architecture_path.read_bytes()
    architecture = json.loads(architecture_raw)
    questions = []
    evidence = {}
    artifact_rows = []
    for qid, config in sorted(architecture["questions"].items()):
        synthesis_rel = f"references/big-questions/{qid}/public-synthesis-v0.1.json"
        synthesis_path = ROOT / synthesis_rel
        synthesis_raw = synthesis_path.read_bytes()
        synthesis = json.loads(synthesis_raw)
        questions.append((qid, synthesis["question"], synthesis_rel))
        artifact_rows.append({"artifact_id": f"artifact:big-question:{qid.casefold()}:public-synthesis", "repository_record": synthesis_rel, "sha256": digest(synthesis_raw), "public_safe": True})
        for rel in config["evidence_batches"]:
            if "review-candidates" in rel:
                continue
            raw = (ROOT / rel).read_bytes()
            batch = json.loads(raw)
            batch_id = batch["batch_id"]
            artifact_id = f"artifact:big-question-evidence:{qid.casefold()}:{slug(batch_id)}"
            artifact_rows.append({"artifact_id": artifact_id, "repository_record": rel, "sha256": digest(raw), "public_safe": True})
            for source in batch.get("sources", []):
                source_id = source["source_id"]
                record = (source_id, source["title"], artifact_id, f"source:evidence:{source_id.casefold()}")
                if source_id in evidence and evidence[source_id][1] != source["title"]:
                    raise ValueError(f"evidence title drift: {source_id}")
                evidence.setdefault(source_id, record)

    artifacts = [
        {"artifact_id": "artifact:topic-census:0.7.5", "repository_record": "scripts/topic_census_v075.py", "sha256": digest((ROOT / "scripts/topic_census_v075.py").read_bytes()), "public_safe": True},
        {"artifact_id": "artifact:reddit-n2n-test-batch-25:public", "repository_record": "references/community/n2n-test-batch-25.csv", "sha256": digest(reddit_raw), "public_safe": True},
        {"artifact_id": "artifact:drive-knowledge-graph-seed:0.1", "repository_record": "references/community/knowledge-graph-seed-v0.1.md", "sha256": digest(drive_raw), "public_safe": True},
        {"artifact_id": "artifact:big-questions:architecture:0.1", "repository_record": "references/big-questions/architecture-v0.1.json", "sha256": digest(architecture_raw), "public_safe": True},
    ] + artifact_rows
    return topics, frameworks, publications, questions, list(evidence.values()), sorted(artifacts, key=lambda item: item["artifact_id"])


def validate_registry(data):
    errors = []
    if data.get("schema_version") != VERSION or data.get("mode") != "ENDPOINT_REGISTRY_ONLY": errors.append("version or mode")
    if data.get("boundaries") != BOUNDARIES or any(data.get("boundaries", {}).values()): errors.append("unsafe boundaries")
    if data.get("edges") != []: errors.append("edges prohibited")
    endpoints = data.get("endpoints", [])
    ids = []
    required = {"endpoint_id", "endpoint_type", "label", "assertion_class", "evidence_status", "identity_state", "provenance"}
    for item in endpoints:
        ids.append(item.get("endpoint_id"))
        if set(item) != required or item.get("endpoint_type") not in TYPES: errors.append("endpoint shape or type")
        if not str(item.get("endpoint_id", "")).startswith("endpoint:"): errors.append("endpoint id")
        provenance = item.get("provenance", {})
        if set(provenance) != {"artifact_id", "record_id", "independence_key", "public_safe"} or provenance.get("public_safe") is not True: errors.append("provenance")
    if None in ids or len(ids) != len(set(ids)): errors.append("endpoint IDs")
    counts = {kind: sum(e.get("endpoint_type") == kind for e in endpoints) for kind in sorted(TYPES)}
    if data.get("summary") != {"endpoint_count": len(endpoints), "counts_by_type": counts, "accepted_edges": 0}: errors.append("summary")
    serialized = json.dumps(data)
    if any(key in serialized for key in ('"drive_id"', '"filename"', '"private_path"', "/My Drive/")): errors.append("private metadata")
    return sorted(set(errors))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=OUTPUT)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    data = build_registry(*load_real_inputs())
    errors = validate_registry(data)
    if errors:
        print("\n".join(f"ERROR: {error}" for error in errors))
        return 1
    rendered = json.dumps(data, indent=2, ensure_ascii=False) + "\n"
    if args.check:
        if not args.output.exists() or args.output.read_text() != rendered:
            print("ERROR: semantic endpoint registry is stale")
            return 1
    else:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered)
    print(json.dumps(data["summary"], sort_keys=True))
    print("AKASHICNET PUBLIC-SAFE SEMANTIC ENDPOINT REGISTRY v0.1.9 PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
