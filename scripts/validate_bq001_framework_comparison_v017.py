#!/usr/bin/env python3
"""Validate the bounded BQ001 v0.17 framework comparison packet."""

from __future__ import annotations

import json
import re
import subprocess
import unicodedata
from urllib.parse import unquote
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
PACKET = ROOT / "references/big-questions/BQ001/framework-comparison-v0.17-slice1.json"
SCHEMA = ROOT / "schemas/bq001-framework-comparison-v0.17-slice1.schema.json"
INPUT_COMMIT = "ac30ecebdc2af6a2dea9c0c8fc00a5f33763fa44"
EXPECTED_IDENTITY = {
    "question_id": "BQ001",
    "packet_id": "BQ001-FRAMEWORK-COMPARISON-V017-SLICE1",
    "version": "0.1.0",
    "mode": "REVIEW_ONLY",
    "question_status": "UNRESOLVED",
    "accepted_edges": 0,
    "input_commit": INPUT_COMMIT,
}
EXPECTED_ANCHORS = {
    "references/big-questions/BQ001/framework-inventory-v0.17-slice1.json": "c2330c292840d95f80f5faad35f548fe5bb16094",
    "references/big-questions/BQ001/spec-v0.1.json": "b35b2397c8ab5341db313ec73c3e45b2bcdf4a5c",
    "references/big-questions/BQ001/public-synthesis-v0.1.json": "b5e793a0ea7d8756f395b9bd49c50ad01a1c79d8",
    "references/big-questions/BQ001/evidence-batch1-v0.1.json": "fc795ea3f224a33e969db6170c9a840dc03ef242",
    "references/big-questions/BQ001/evidence-batch2-v0.1.json": "894ee42a3a2c1b8cf09f8026fac9b03dc74bf5f9",
    "references/big-questions/BQ001/evidence-batch3-v0.1.json": "44ab4a1bb7dc941a52c9d7529e719ed7e91cc3f5",
    "references/big-questions/BQ001/evidence-batch4-v0.1.json": "4d3f4bebc8605290abc62fa1eaa735912d44c60f",
    "references/big-questions/BQ001/evidence-batch5-v0.1.json": "473a64435784412e783b4d6bf590f44859fca006",
}
EXPECTED_OPERATIONAL_BOUNDARIES = {
    "analytics_activation_allowed": False,
    "multimedia_generation_allowed": False,
    "private_drive_material_allowed": False,
    "reddit_live_access": "HOLD",
    "website_publication_allowed": False,
}
EXPECTED_PROMOTION_GUARDS = {
    "accepted_edge_creation_allowed": False,
    "evidence_promotion_allowed": False,
    "framework_count_is_vote": False,
    "ranking_allowed": False,
    "rights_promotion_allowed": False,
    "scientific_evidence_promotion_allowed": False,
    "shared_source_counts_as_independent_confirmation": False,
    "source_count_upgrades_evidence": False,
    "truth_inference_allowed": False,
}
TOP_KEYS = {
    "accepted_edges", "comparison_rows", "correction_records", "counter_inferences",
    "input_anchors", "input_commit", "mode", "operational_boundaries", "packet_id",
    "promotion_guards", "question_id", "question_status", "research_gaps",
    "shared_ancestry_groups", "version",
}
ROW_KEYS = {
    "boundary", "canonical_name", "category", "comparison_state", "counter_evidence_state",
    "evidence_role", "independence_state", "inventory_item_id", "linked_record_ids",
    "relation_to_bq001",
}
ANCHOR_KEYS = {"git_blob_sha", "path"}
CORRECTION_KEYS = {"claim_id", "evidence_label_changed", "related_notice_doi", "result"}
ANCESTRY_KEYS = {"claim_id", "inventory_item_ids", "rule", "source_id"}
FORBIDDEN_KEYS = {"answer", "confidence", "conclusion", "probability", "rank", "score", "synthesis", "winner"}
PRIVATE_METADATA_KEYS = {
    "driveid", "drivefileid", "driveobjectid", "fileid", "objectid",
    "filename", "filepath", "privatepath", "parentid", "objecthash",
    "objectsha256", "md5checksum", "sha256checksum", "privatedriveid",
}
PRIVATE_MARKERS = ("drive.google.com", "docs.google.com", "drive.usercontent.google.com", "docs.googleusercontent.com")
PRIVATE_PATH_MARKERS = ("/my drive/", "akm-", "file://", "gdrive://")
# Same ignored ranges as the reviewed inventory validator at INPUT_COMMIT.
UTS46_IGNORED_RANGES = (
    (0x00AD, 0x00AD), (0x034F, 0x034F), (0x115F, 0x1160),
    (0x17B4, 0x17B5), (0x180B, 0x180F), (0x200B, 0x200B),
    (0x2060, 0x2064), (0x206A, 0x206F), (0x3164, 0x3164),
    (0xFE00, 0xFE0F), (0xFEFF, 0xFEFF), (0xFFA0, 0xFFA0),
    (0x1BCA0, 0x1BCA3), (0x1D173, 0x1D17A), (0xE0100, 0xE01EF),
)


def normalize_private_text(text: str) -> str:
    for _ in range(32):
        normalized = unquote(unicodedata.normalize("NFKC", text)).casefold()
        normalized = normalized.replace("\\", "/").translate(str.maketrans({
            "。": ".", "．": ".", "｡": ".", "\t": None, "\n": None, "\r": None,
        }))
        normalized = "".join(c for c in normalized if not any(
            start <= ord(c) <= end for start, end in UTS46_IGNORED_RANGES
        ))
        if normalized == text:
            return normalized
        text = normalized
    raise ValueError("privacy encoding did not stabilize")


def reject_constant(value: str) -> None:
    raise ValueError(f"non-finite JSON constant rejected: {value}")


def reject_duplicate_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key rejected: {key}")
        result[key] = value
    return result


def load_json(source: Path | bytes | str) -> Any:
    if isinstance(source, Path):
        text = source.read_text(encoding="utf-8")
    elif isinstance(source, bytes):
        text = source.decode("utf-8")
    else:
        text = source
    return json.loads(text, object_pairs_hook=reject_duplicate_pairs, parse_constant=reject_constant)


def assert_exact_keys(value: dict[str, Any], expected: set[str], label: str) -> None:
    if set(value) != expected:
        raise ValueError(f"{label} exact allowed-key set drift")


def scan_safety(value: Any) -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            normalized_key = re.sub(r"[^a-z0-9]", "", normalize_private_text(key))
            if normalized_key in FORBIDDEN_KEYS:
                raise ValueError(f"adjudicative key rejected: {key}")
            if normalized_key in PRIVATE_METADATA_KEYS:
                raise ValueError(f"private metadata key rejected: {key}")
            scan_safety(key)
            scan_safety(child)
    elif isinstance(value, list):
        for child in value:
            scan_safety(child)
    elif isinstance(value, str):
        folded = normalize_private_text(value)
        if any(marker in folded for marker in PRIVATE_MARKERS):
            raise ValueError("private Drive/Docs marker rejected")
        if any(marker in folded for marker in PRIVATE_PATH_MARKERS):
            raise ValueError("private path marker rejected")


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def validate_anchors(packet: dict[str, Any], *, verify_git: bool = True) -> None:
    anchors = {entry["path"]: entry["git_blob_sha"] for entry in packet["input_anchors"]}
    if anchors != EXPECTED_ANCHORS or len(packet["input_anchors"]) != len(EXPECTED_ANCHORS):
        raise ValueError("input anchor mapping drift")
    if packet["input_commit"] != INPUT_COMMIT:
        raise ValueError("input commit drift")
    if not verify_git:
        return
    git("merge-base", "--is-ancestor", INPUT_COMMIT, "HEAD")
    for path, expected_blob in EXPECTED_ANCHORS.items():
        inherited = git("ls-tree", INPUT_COMMIT, "--", path).split()
        if len(inherited) < 3 or inherited[2] != expected_blob:
            raise ValueError(f"inherited blob mismatch: {path}")
        if git("hash-object", path) != expected_blob:
            raise ValueError(f"governed input modified after pin: {path}")


def expected_comparison_state(item: dict[str, Any]) -> str:
    if item["category"] == "UMBRELLA_MODEL":
        return "MODEL_CONTRACT_ONLY_NOT_ADJUDICATED"
    if item["category"] == "CONSCIOUSNESS_THEORY":
        return "LIVING_BRAIN_TESTED_NOT_ADJUDICATED_FOR_BQ001"
    return "INTERPRETIVE_FRAMEWORK_NOT_EMPIRICAL_ADJUDICATION"


def expected_counter_state(item: dict[str, Any]) -> str:
    if item["category"] == "UMBRELLA_MODEL":
        return "PACKET_LEVEL_COUNTER_INFERENCES_PRESERVED"
    if item["category"] == "CONSCIOUSNESS_THEORY":
        return "SHARED_ADVERSARIAL_RESULT_CHALLENGED_PREDICTIONS_NOT_A_BQ001_COUNTERCLAIM"
    return "NO_FRAMEWORK_SPECIFIC_COUNTERCLAIM_IN_PINNED_INVENTORY"


def validate_rows(packet: dict[str, Any], inventory: dict[str, Any], documents: list[dict[str, Any]]) -> None:
    source_items = {item["inventory_item_id"]: item for item in inventory["inventory"]}
    rows = {row["inventory_item_id"]: row for row in packet["comparison_rows"]}
    if len(rows) != 11 or set(rows) != set(source_items):
        raise ValueError("comparison row membership drift")
    claims = {claim["claim_id"]: claim for document in documents for claim in document.get("claims", [])}
    models = {model["model_id"] for document in documents for model in document.get("models", [])}
    for item_id, item in source_items.items():
        row = rows[item_id]
        assert_exact_keys(row, ROW_KEYS, f"comparison row {item_id}")
        projection = {
            "boundary": item["boundary"],
            "canonical_name": item["canonical_name"],
            "category": item["category"],
            "evidence_role": item["evidence_role"],
            "independence_state": item["independence_state"],
            "inventory_item_id": item_id,
            "linked_record_ids": item["represented_by"],
            "relation_to_bq001": item["relation_to_bq001"],
        }
        for key, expected in projection.items():
            if row[key] != expected:
                raise ValueError(f"inventory projection drift for {item_id}: {key}")
        if row["comparison_state"] != expected_comparison_state(item):
            raise ValueError(f"comparison state drift for {item_id}")
        if row["counter_evidence_state"] != expected_counter_state(item):
            raise ValueError(f"counter-evidence state drift for {item_id}")
        for record_id in row["linked_record_ids"]:
            if record_id.startswith("MODEL-") and record_id not in models:
                raise ValueError(f"missing model record: {record_id}")
            if record_id.startswith("CLAIM-"):
                claim = claims.get(record_id)
                if not claim:
                    raise ValueError(f"missing claim record: {record_id}")
                expected_label = {
                    "INTERPRETATION": "Interpretation",
                    "Established Evidence": "Established Evidence",
                }.get(row["evidence_role"])
                if expected_label is None or claim["evidence_label"] != expected_label:
                    raise ValueError(f"claim evidence-role drift: {record_id}")


def validate_correction(packet: dict[str, Any], batch2: dict[str, Any]) -> None:
    record = packet["correction_records"][0]
    assert_exact_keys(record, CORRECTION_KEYS, "correction record")
    claim = next(c for c in batch2["claims"] if c["claim_id"] == record["claim_id"])
    source = claim["correction_impact_assessment"]
    expected = {
        "claim_id": claim["claim_id"],
        "evidence_label_changed": source["evidence_label_changed"],
        "related_notice_doi": source["related_notice_doi"],
        "result": source["result"],
    }
    if record != expected:
        raise ValueError("correction record drift")


def validate(packet: dict[str, Any] | None = None, *, verify_git: bool = True) -> None:
    packet = packet if packet is not None else load_json(PACKET)
    schema = load_json(SCHEMA)
    scan_safety(packet)
    scan_safety(schema)
    for key, expected in EXPECTED_IDENTITY.items():
        if type(packet.get(key)) is not type(expected) or packet.get(key) != expected:
            raise ValueError(f"packet identity drift: {key}")
    Draft202012Validator.check_schema(schema)
    Draft202012Validator(schema).validate(packet)
    assert_exact_keys(packet, TOP_KEYS, "packet")
    assert_exact_keys(packet["operational_boundaries"], set(EXPECTED_OPERATIONAL_BOUNDARIES), "operational boundaries")
    assert_exact_keys(packet["promotion_guards"], set(EXPECTED_PROMOTION_GUARDS), "promotion guards")
    if packet["operational_boundaries"] != EXPECTED_OPERATIONAL_BOUNDARIES:
        raise ValueError("operational boundary mapping drift")
    if packet["promotion_guards"] != EXPECTED_PROMOTION_GUARDS:
        raise ValueError("promotion guard mapping drift")
    if packet["accepted_edges"] != 0 or packet["question_status"] != "UNRESOLVED" or packet["mode"] != "REVIEW_ONLY":
        raise ValueError("core review-only invariant drift")
    for anchor in packet["input_anchors"]:
        assert_exact_keys(anchor, ANCHOR_KEYS, "input anchor")
    for group in packet["shared_ancestry_groups"]:
        assert_exact_keys(group, ANCESTRY_KEYS, "shared ancestry group")
    validate_anchors(packet, verify_git=verify_git)

    inventory = load_json(ROOT / "references/big-questions/BQ001/framework-inventory-v0.17-slice1.json")
    spec = load_json(ROOT / "references/big-questions/BQ001/spec-v0.1.json")
    synthesis = load_json(ROOT / "references/big-questions/BQ001/public-synthesis-v0.1.json")
    batches = [load_json(ROOT / f"references/big-questions/BQ001/evidence-batch{i}-v0.1.json") for i in range(1, 6)]
    validate_rows(packet, inventory, [spec, *batches])
    if packet["counter_inferences"] != synthesis["counter_inferences"]:
        raise ValueError("counter-inference parity drift")
    if packet["research_gaps"] != synthesis["open_questions"]:
        raise ValueError("research-gap parity drift")
    validate_correction(packet, batches[1])
    expected_group = {
        "claim_id": "CLAIM-BQ001-COGITATE-2025-OBS-01",
        "inventory_item_ids": ["FW-BQ001-CONSCIOUSNESS-GNWT", "FW-BQ001-CONSCIOUSNESS-IIT"],
        "rule": "ONE_GOVERNED_SOURCE_NOT_TWO_INDEPENDENT_CONFIRMATIONS",
        "source_id": "SRC-BQ001-COGITATE-2025",
    }
    if packet["shared_ancestry_groups"] != [expected_group]:
        raise ValueError("shared-source ancestry drift")


def main() -> None:
    validate()
    print("BQ001 v0.17 framework comparison packet: PASS")


if __name__ == "__main__":
    main()
