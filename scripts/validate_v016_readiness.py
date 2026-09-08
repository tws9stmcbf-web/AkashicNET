#!/usr/bin/env python3
"""Minimal composed readiness gate for v0.16 Knowledge Graph Beta."""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "references/big-questions/BQ001/knowledge-graph-beta-fixture-v0.16.json"
SCHEMA = ROOT / "schemas/knowledge-graph-beta-v0.16.schema.json"
VALIDATOR = ROOT / "scripts/validate_knowledge_graph_beta_v016.py"
TESTS = ROOT / "tests/test_knowledge_graph_beta_v016.py"

V014 = "7b6cfd89de570c4b945d574dad570c37825645fe"
V015_RELEASE = "ea46629558ff57970f6efd2485a7e9a288dc55f2"
V015_SEAL = "5ba6989aade68461c8f3953c4a82cc0e158b0730"

for path in (FIXTURE, SCHEMA, VALIDATOR, TESTS):
    if not path.is_file():
        raise SystemExit(f"FAIL: missing governed v0.16 artifact: {path.relative_to(ROOT)}")

data = json.loads(FIXTURE.read_text())

if data.get("schema_version") != "0.16.0-beta.1":
    raise SystemExit("FAIL: wrong v0.16 schema version")
if data.get("mode") != "REVIEW_FIXTURE_ONLY":
    raise SystemExit("FAIL: v0.16 fixture escaped review-only mode")
if data.get("question_id") != "BQ001" or data.get("question_status") != "UNRESOLVED":
    raise SystemExit("FAIL: BQ001 must remain unresolved")

locks = data.get("baseline_locks", {})
expected_locks = {
    "v0.14": V014,
    "v0.15_release": V015_RELEASE,
    "v0.15_seal": V015_SEAL,
}
if locks != expected_locks:
    raise SystemExit("FAIL: sealed baseline lock drift")

boundaries = data.get("boundaries", {})
if not isinstance(boundaries, dict) or any(boundaries.values()):
    raise SystemExit("FAIL: a permanent v0.16 promotion boundary became enabled")

edges = data.get("edges", [])
if not edges:
    raise SystemExit("FAIL: missing graph relationships")
if any(edge.get("accepted_edge") is not False for edge in edges):
    raise SystemExit("FAIL: accepted graph edge present")

inferred = [e for e in edges if e.get("assertion_class") == "INFERRED_CANDIDATE"]
if not inferred:
    raise SystemExit("FAIL: no inferred review fixture exercised")
if any(e.get("review_state") != "REVIEW_REQUIRED" for e in inferred):
    raise SystemExit("FAIL: inferred relationship escaped review-required state")

relationship_types = {e.get("relationship_type") for e in edges}
for required in {"COMPETES_WITH_CANDIDATE", "CORRECTS"}:
    if required not in relationship_types:
        raise SystemExit(f"FAIL: missing conflict/correction fixture: {required}")

for edge in edges:
    independence = edge.get("evidence_independence_keys")
    parents = edge.get("parent_edge_ids")
    if not isinstance(independence, list) or not independence:
        raise SystemExit("FAIL: edge missing evidence independence keys")
    if not isinstance(parents, list):
        raise SystemExit("FAIL: edge ancestry is not explicit")

summary = data.get("summary", {})
if summary.get("accepted_edge_count") != 0:
    raise SystemExit("FAIL: summary reports accepted edges")
if summary.get("unresolved_question_count") != 1:
    raise SystemExit("FAIL: BQ001 unresolved summary drift")

commands = [
    [sys.executable, "scripts/validate_knowledge_graph_beta_v016.py"],
    [sys.executable, "-m", "unittest", "tests.test_knowledge_graph_beta_v016"],
]
for command in commands:
    result = subprocess.run(command, cwd=ROOT)
    if result.returncode != 0:
        raise SystemExit(f"FAIL: readiness dependency failed: {' '.join(command[1:])}")

print("PASS: v0.16 Knowledge Graph Beta minimal readiness gate")
print("PASS: provenance, ancestry, independence, conflict/correction and review-only boundaries remain fail-closed")
