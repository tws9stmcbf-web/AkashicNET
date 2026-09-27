#!/usr/bin/env python3
"""Prepare deterministic exact-term semantic link candidates for human review only."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = ROOT / "references/community/public-safe-semantic-endpoint-registry-v0.1.9.json"
DEFAULT_OUTPUT = ROOT / "references/community/semantic-link-candidates-v0.2.0.json"
V021_OUTPUT = ROOT / "references/community/semantic-link-candidates-v0.2.1.json"
VERSION = "0.2.0"
RELATIONSHIP = "LABEL_CONTAINS_EXACT_TOPIC_TERM"
SOURCE_TYPES = {"PUBLICATION", "FRAMEWORK", "QUESTION", "EVIDENCE_RECORD"}
MAX_CANDIDATES = 25
MIN_SINGLE_TOKEN_LENGTH = 4

BOUNDARIES = {
    "automated_truth_inference_allowed": False,
    "automated_acceptance_allowed": False,
    "rights_promotion_allowed": False,
    "scientific_evidence_promotion_allowed": False,
    "canonical_identity_promotion_allowed": False,
    "circular_confidence_allowed": False,
    "graph_derived_signals_allowed": False,
    "transitive_inference_allowed": False,
    "representation_count_signal_allowed": False,
    "private_drive_metadata_allowed": False,
}


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def tokens(value: str) -> list[str]:
    return re.findall(r"[a-z0-9]+", value.casefold())


def exact_positions(haystack: list[str], needle: list[str]) -> list[int]:
    return [index for index in range(len(haystack) - len(needle) + 1) if haystack[index:index + len(needle)] == needle]


def eligible_topic(label: str) -> bool:
    parts = tokens(label)
    return bool(parts) and (len(parts) > 1 or len(parts[0]) >= MIN_SINGLE_TOKEN_LENGTH)


def endpoint_ref(endpoint: dict) -> dict:
    return {
        "endpoint_id": endpoint["endpoint_id"],
        "endpoint_type": endpoint["endpoint_type"],
        "label": endpoint["label"],
        "provenance": dict(endpoint["provenance"]),
    }


def candidate_id(source_id: str, target_id: str, normalized_topic: str) -> str:
    raw = json.dumps(
        {"source": source_id, "target": target_id, "relationship": RELATIONSHIP, "topic": normalized_topic},
        sort_keys=True,
        separators=(",", ":"),
    ).encode()
    return f"candidate:semantic:{sha256(raw)[:20]}"


def build_packet(registry_raw: bytes, version: str = VERSION) -> dict:
    if version not in {"0.2.0", "0.2.1"}:
        raise ValueError("unsupported candidate packet version")
    registry = json.loads(registry_raw)
    registry_sha = sha256(registry_raw)
    endpoints = registry.get("endpoints", [])
    topics = sorted((e for e in endpoints if e.get("endpoint_type") == "TOPIC"), key=lambda e: e["endpoint_id"])
    sources = sorted((e for e in endpoints if e.get("endpoint_type") in SOURCE_TYPES), key=lambda e: e["endpoint_id"])
    candidates = []
    for source in sources:
        source_tokens = tokens(source["label"])
        for topic in topics:
            topic_tokens = tokens(topic["label"])
            if not eligible_topic(topic["label"]):
                continue
            positions = exact_positions(source_tokens, topic_tokens)
            if not positions:
                continue
            if source["provenance"]["artifact_id"] == topic["provenance"]["artifact_id"]:
                continue
            normalized_topic = " ".join(topic_tokens)
            start = positions[0]
            candidates.append({
                "candidate_id": candidate_id(source["endpoint_id"], topic["endpoint_id"], normalized_topic),
                "relationship": RELATIONSHIP,
                "assertion_class": "INFERRED_CANDIDATE",
                "review_state": "REVIEW_REQUIRED",
                "accepted_edge": False,
                "source_endpoint": endpoint_ref(source),
                "target_topic": endpoint_ref(topic),
                "anchor_evidence": {
                    "anchor_type": "EXACT_WHOLE_TERM",
                    "normalized_topic": normalized_topic,
                    "source_token_start": start,
                    "source_token_end_exclusive": start + len(topic_tokens),
                    "registry_sha256": registry_sha,
                },
                "signal_controls": {
                    "graph_derived": False,
                    "transitive_inference": False,
                    "representation_count_used": False,
                    "confidence_aggregation": False,
                },
                "not_truth_claim": True,
                "not_scientific_evidence": True,
                "not_rights_clearance": True,
                "not_canonical_identity": True,
            })
    candidates.sort(key=lambda item: item["candidate_id"])
    if len(candidates) > MAX_CANDIDATES:
        raise ValueError(f"review volume exceeds fail-closed cap: {len(candidates)} > {MAX_CANDIDATES}")
    counts = {kind: sum(c["source_endpoint"]["endpoint_type"] == kind for c in candidates) for kind in sorted(SOURCE_TYPES)}
    return {
        "schema_version": version,
        "mode": "REVIEW_PACKET_ONLY",
        "relationship_semantics": "The source public label contains the target topic label as an exact normalized token sequence; this does not assert broader aboutness.",
        "boundaries": dict(BOUNDARIES),
        "input": {
            "artifact_id": "artifact:public-safe-semantic-endpoint-registry:0.1.9",
            "repository_record": "references/community/public-safe-semantic-endpoint-registry-v0.1.9.json",
            "sha256": registry_sha,
            "public_safe": True,
        },
        "generation_policy": {
            "method": "EXACT_NORMALIZED_TOKEN_SEQUENCE",
            "minimum_single_token_length": MIN_SINGLE_TOKEN_LENGTH,
            "eligible_source_types": sorted(SOURCE_TYPES),
            "target_type": "TOPIC",
            "maximum_candidates": MAX_CANDIDATES,
            "overflow_behavior": "FAIL_CLOSED",
        },
        "proposed_candidates": candidates,
        "accepted_edges": [],
        "summary": {
            "candidate_count": len(candidates),
            "counts_by_source_type": counts,
            "accepted_edges": 0,
            "human_review_required": True,
        },
    }


def validate_packet(packet: dict, version: str = VERSION) -> list[str]:
    errors = []
    if packet.get("schema_version") != version or packet.get("mode") != "REVIEW_PACKET_ONLY": errors.append("version or mode")
    if packet.get("boundaries") != BOUNDARIES or any(packet.get("boundaries", {}).values()): errors.append("unsafe boundaries")
    if packet.get("accepted_edges") != []: errors.append("accepted edges prohibited")
    input_row = packet.get("input", {})
    if input_row.get("public_safe") is not True or not re.fullmatch(r"[a-f0-9]{64}", str(input_row.get("sha256", ""))): errors.append("input provenance")
    expected_policy = {
        "method": "EXACT_NORMALIZED_TOKEN_SEQUENCE", "minimum_single_token_length": MIN_SINGLE_TOKEN_LENGTH,
        "eligible_source_types": sorted(SOURCE_TYPES), "target_type": "TOPIC",
        "maximum_candidates": MAX_CANDIDATES, "overflow_behavior": "FAIL_CLOSED",
    }
    if packet.get("generation_policy") != expected_policy: errors.append("generation policy")
    candidates = packet.get("proposed_candidates")
    if not isinstance(candidates, list): errors.append("candidate list"); candidates = []
    if len(candidates) > MAX_CANDIDATES: errors.append("review cap")
    ids, pairs = [], []
    for candidate in candidates:
        ids.append(candidate.get("candidate_id"))
        source, target = candidate.get("source_endpoint", {}), candidate.get("target_topic", {})
        pairs.append((source.get("endpoint_id"), target.get("endpoint_id")))
        anchor = candidate.get("anchor_evidence", {})
        controls = candidate.get("signal_controls", {})
        if candidate.get("relationship") != RELATIONSHIP or candidate.get("assertion_class") != "INFERRED_CANDIDATE": errors.append("candidate semantics")
        if candidate.get("review_state") != "REVIEW_REQUIRED" or candidate.get("accepted_edge") is not False: errors.append("review gate")
        if source.get("endpoint_type") not in SOURCE_TYPES or target.get("endpoint_type") != "TOPIC": errors.append("endpoint types")
        for ref in (source, target):
            provenance = ref.get("provenance", {})
            if provenance.get("public_safe") is not True or not provenance.get("artifact_id") or not provenance.get("record_id") or not provenance.get("independence_key"): errors.append("endpoint provenance")
        if source.get("provenance", {}).get("artifact_id") == target.get("provenance", {}).get("artifact_id"): errors.append("same-artifact candidate")
        source_tokens, topic_tokens = tokens(source.get("label", "")), tokens(target.get("label", ""))
        start, end = anchor.get("source_token_start"), anchor.get("source_token_end_exclusive")
        if anchor.get("anchor_type") != "EXACT_WHOLE_TERM" or anchor.get("normalized_topic") != " ".join(topic_tokens): errors.append("anchor semantics")
        if not isinstance(start, int) or not isinstance(end, int) or source_tokens[start:end] != topic_tokens or not eligible_topic(target.get("label", "")): errors.append("anchor position")
        if anchor.get("registry_sha256") != input_row.get("sha256"): errors.append("anchor lineage")
        expected_id = candidate_id(source.get("endpoint_id", ""), target.get("endpoint_id", ""), " ".join(topic_tokens))
        if candidate.get("candidate_id") != expected_id: errors.append("candidate id")
        if controls != {"graph_derived": False, "transitive_inference": False, "representation_count_used": False, "confidence_aggregation": False}: errors.append("derived signal")
        for key in ("not_truth_claim", "not_scientific_evidence", "not_rights_clearance", "not_canonical_identity"):
            if candidate.get(key) is not True: errors.append("boundary markers")
    if None in ids or len(ids) != len(set(ids)) or len(pairs) != len(set(pairs)): errors.append("candidate uniqueness")
    counts = {kind: sum(c.get("source_endpoint", {}).get("endpoint_type") == kind for c in candidates) for kind in sorted(SOURCE_TYPES)}
    if packet.get("summary") != {"candidate_count": len(candidates), "counts_by_source_type": counts, "accepted_edges": 0, "human_review_required": True}: errors.append("summary")
    serialized = json.dumps(packet)
    if any(key in serialized for key in ('"drive_id"', '"filename"', '"private_path"', "/My Drive/")): errors.append("private metadata")
    return sorted(set(errors))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--version", choices=("0.2.0", "0.2.1"), default=VERSION)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    output = args.output or (V021_OUTPUT if args.version == "0.2.1" else DEFAULT_OUTPUT)
    packet = build_packet(args.input.read_bytes(), args.version)
    errors = validate_packet(packet, args.version)
    if errors:
        print("\n".join(f"ERROR: {error}" for error in errors))
        return 1
    rendered = json.dumps(packet, indent=2, ensure_ascii=False) + "\n"
    if args.check:
        if not output.exists() or output.read_text(encoding="utf-8") != rendered:
            print("ERROR: semantic link candidate packet is stale")
            return 1
    else:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(rendered, encoding="utf-8")
    print(json.dumps(packet["summary"], sort_keys=True))
    print(f"AKASHICNET SEMANTIC LINK CANDIDATES v{args.version} PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
