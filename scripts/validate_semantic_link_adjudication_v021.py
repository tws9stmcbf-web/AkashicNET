#!/usr/bin/env python3
"""Fail-closed validation for semantic-link human adjudication v0.2.1."""
from __future__ import annotations
import hashlib
import json
import sys
from pathlib import Path
from validate_cross_source_edge_provenance_v01 import validate as validate_provenance

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "references/community/semantic-link-adjudication-v0.2.1.json"
LEDGER = ROOT / "references/community/semantic-link-adjudication-v0.2.1.md"
PACKET = ROOT / "references/community/semantic-link-candidates-v0.2.0.json"
PACKET_SHA256 = "551bbe430be78226dc1005e99b28aeea2b21ac6cf98abd96917fa65d1c99da28"
EXPECTED_IDS = [
  "candidate:semantic:191f4ddea1a78d584166",
  "candidate:semantic:19c4d2c70c48b2d04cf2",
  "candidate:semantic:19ed7cfa6ce4b807d123",
  "candidate:semantic:2f8eb01ad4363504a3b6",
  "candidate:semantic:2fcd56322574a00eaec0",
  "candidate:semantic:303a33d87f51450a3896",
  "candidate:semantic:4e4c9bc1887135c87694",
  "candidate:semantic:854b34c6a3d870962d68",
  "candidate:semantic:a5b341fbd98fa340e86e",
  "candidate:semantic:a81be86e8a6e9e54db71",
  "candidate:semantic:aa46dbe9d8c846958d27",
  "candidate:semantic:c6743c1f49599d7a51d8",
  "candidate:semantic:f043c41f69968d5b6f41",
  "candidate:semantic:fca9643adce7a4831b3b"
]
FALSE_POLICY = {
    "truth_inference_allowed": False,
    "rights_promotion_allowed": False,
    "scientific_evidence_promotion_allowed": False,
    "confidence_from_representation_count_allowed": False,
    "circular_confidence_allowed": False,
}

def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def validate(data: dict) -> list[str]:
    errors = list(validate_provenance(data))
    packet = json.loads(PACKET.read_text(encoding="utf-8"))
    if sha256(PACKET) != PACKET_SHA256:
        errors.append("review packet digest changed")
    candidates = packet.get("proposed_candidates", [])
    if [c.get("candidate_id") for c in candidates] != EXPECTED_IDS:
        errors.append("candidate identity or order changed")
    if packet.get("accepted_edges") != [] or any(c.get("accepted_edge") is not False for c in candidates):
        errors.append("original proposal packet must remain review-only and unaccepted")
    if data.get("policy") != FALSE_POLICY:
        errors.append("safety policy changed")
    artifacts = {a.get("artifact_id"): a for a in data.get("artifacts", [])}
    ledger = artifacts.get("artifact:semantic-link-adjudication:0.2.1", {})
    if ledger.get("sha256") != sha256(LEDGER):
        errors.append("adjudication ledger digest mismatch")
    edges = data.get("edges", [])
    parents = {e.get("edge_id"): e for e in edges if e.get("assertion_class") == "INFERRED_CANDIDATE"}
    accepted = [e for e in edges if e.get("accepted_edge") is True]
    if len(parents) != 14 or len(accepted) != 14 or len(edges) != 28:
        errors.append("adjudication must preserve 14 parents and add exactly 14 accepted child edges")
    for candidate_id in EXPECTED_IDS:
        suffix = candidate_id.rsplit(":", 1)[-1]
        parent_id = f"edge:semantic-candidate:{suffix}"
        child_id = f"edge:semantic-accepted:{suffix}"
        parent = parents.get(parent_id)
        child = next((e for e in accepted if e.get("edge_id") == child_id), None)
        if not parent or not child:
            errors.append(f"missing adjudication lineage for {candidate_id}")
            continue
        if child.get("parent_edge_ids") != [parent_id]:
            errors.append(f"wrong parent lineage for {child_id}")
        if child.get("relationship") != "LABEL_CONTAINS_EXACT_TOPIC_TERM":
            errors.append(f"relationship broadened on {child_id}")
        if child.get("assertion_class") != "HUMAN_ADJUDICATED" or child.get("review_state") != "ACCEPTED":
            errors.append(f"invalid accepted state on {child_id}")
        if child.get("source") != parent.get("source") or child.get("target") != parent.get("target"):
            errors.append(f"endpoints changed on {child_id}")
        expected_ref = {"artifact_id": "artifact:semantic-link-adjudication:0.2.1", "record_id": f"decision:semantic:{suffix}"}
        if child.get("adjudication_ref") != expected_ref:
            errors.append(f"wrong adjudication reference on {child_id}")
    serialized = json.dumps(data)
    for forbidden in ('"drive_id"', '"filename"', '"private_path"', "/My Drive/"):
        if forbidden in serialized:
            errors.append("private Drive metadata prohibited")
    return sorted(set(errors))

def main() -> int:
    data = json.loads(ARTIFACT.read_text(encoding="utf-8"))
    errors = validate(data)
    if errors:
        for error in errors:
            print(f"FAIL: {error}", file=sys.stderr)
        return 1
    print("PASS: 14 human-adjudicated literal semantic links; proposal packet unchanged; all safety boundaries preserved")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
