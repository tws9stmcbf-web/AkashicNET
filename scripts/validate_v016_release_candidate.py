#!/usr/bin/env python3
"""Fail-closed composite validator for the unreleased v0.16 candidate."""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "manifests/v0.16-release-candidate.json"
SHA40 = re.compile(r"^[0-9a-f]{40}$")
EXPECTED_BASE_COMMIT = "779be69acd564a09aada6212083d0fb3c0b599bf"

EXPECTED_BASELINES = {
    "v0.14": "7b6cfd89de570c4b945d574dad570c37825645fe",
    "v0.15_release": "ea46629558ff57970f6efd2485a7e9a288dc55f2",
    "v0.15_seal": "5ba6989aade68461c8f3953c4a82cc0e158b0730",
}
EXPECTED_GATES = {
    "typed_graph_contract",
    "provenance_on_write",
    "referential_integrity",
    "epistemic_labels",
    "review_only_inference",
    "evidence_independence",
    "claim_evidence_alignment",
    "corrections_and_conflict",
    "bq001_question_graph",
    "fail_closed_verification",
}
EXPECTED_ROLES = {
    "GRAPH_FIXTURE": 1,
    "GRAPH_SCHEMA": 1,
    "GRAPH_VALIDATOR": 1,
    "GRAPH_MUTATION_TESTS": 1,
    "GRAPH_READINESS_GATE": 1,
    "SOURCE_STATUS_SCHEMA": 1,
    "OBSERVED_SOURCE_STATUS_FIXTURE": 2,
    "SYNTHETIC_VALIDATOR_ONLY_FIXTURE": 1,
    "SOURCE_STATUS_VALIDATOR": 1,
    "SOURCE_STATUS_MUTATION_TESTS": 1,
}
EXPECTED_ARTIFACTS = {
    "references/big-questions/BQ001/knowledge-graph-beta-fixture-v0.16.json": "GRAPH_FIXTURE",
    "schemas/knowledge-graph-beta-v0.16.schema.json": "GRAPH_SCHEMA",
    "scripts/validate_knowledge_graph_beta_v016.py": "GRAPH_VALIDATOR",
    "tests/test_knowledge_graph_beta_v016.py": "GRAPH_MUTATION_TESTS",
    "scripts/validate_v016_readiness.py": "GRAPH_READINESS_GATE",
    "schemas/source-status-v0.16.schema.json": "SOURCE_STATUS_SCHEMA",
    "references/source-status-fixture-v0.16.json": "OBSERVED_SOURCE_STATUS_FIXTURE",
    "references/source-status-fixture-v0.16-slice2.json": "OBSERVED_SOURCE_STATUS_FIXTURE",
    "references/source-status-fixture-v0.16-synthetic.json": "SYNTHETIC_VALIDATOR_ONLY_FIXTURE",
    "scripts/validate_source_status_v016.py": "SOURCE_STATUS_VALIDATOR",
    "tests/test_source_status_v016.py": "SOURCE_STATUS_MUTATION_TESTS",
}

EXPECTED_BOUNDARIES = {
    "truth",
    "scientific_evidence",
    "rights",
    "identity",
    "safety_efficacy",
    "private_data",
    "edge_acceptance",
    "website_publication",
}


def git_blob_sha(path: str) -> str:
    result = subprocess.run(
        ["git", "rev-parse", f"HEAD:{path}"],
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
    )
    return result.stdout.strip()


def discovered_source_status_fixture_paths() -> set[str]:
    return {
        str(path.relative_to(ROOT))
        for path in (ROOT / "references").glob("source-status-fixture-v0.16*.json")
    }


def validate_repository_binding() -> list[str]:
    """Bind the immutable candidate anchor and exact CI head to Git history."""
    errors: list[str] = []
    try:
        head = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=ROOT,
            check=True,
            text=True,
            capture_output=True,
        ).stdout.strip()
        expected_head = os.environ.get("CANDIDATE_HEAD_SHA", "").strip()
        if expected_head and head != expected_head:
            errors.append("exact candidate head checkout")
        for ref, error in (
            ("HEAD", "candidate base is not an ancestor of head"),
            ("origin/main", "candidate base is not an ancestor of main"),
        ):
            result = subprocess.run(
                ["git", "merge-base", "--is-ancestor", EXPECTED_BASE_COMMIT, ref],
                cwd=ROOT,
                check=False,
                text=True,
                capture_output=True,
            )
            if result.returncode != 0:
                errors.append(error)
    except subprocess.CalledProcessError:
        errors.append("candidate repository binding")
    return errors


def validate_manifest(data: dict) -> list[str]:
    errors: list[str] = []

    if data.get("schema_version") != "0.16.0-beta.1":
        errors.append("schema version")
    if data.get("artifact_status") != "UNRELEASED_REVIEW_CANDIDATE":
        errors.append("candidate status")
    if data.get("issue") != 277:
        errors.append("issue binding")
    if data.get("candidate_base_commit") != EXPECTED_BASE_COMMIT:
        errors.append("candidate base commit")
    if data.get("exact_head_ci_required") is not True:
        errors.append("exact-head requirement")
    if data.get("release_decision") != "PENDING_EXACT_HEAD_CI_AND_REVIEW":
        errors.append("premature release decision")
    if data.get("baseline_locks") != EXPECTED_BASELINES:
        errors.append("sealed baseline lock drift")
    if set(data.get("required_gates", [])) != EXPECTED_GATES:
        errors.append("ten-gate composition")

    boundaries = data.get("promotion_boundaries")
    if (
        not isinstance(boundaries, dict)
        or set(boundaries) != EXPECTED_BOUNDARIES
        or any(value is not False for value in boundaries.values())
    ):
        errors.append("promotion boundary")

    artifacts = data.get("governed_artifacts")
    if not isinstance(artifacts, list):
        errors.append("governed artifacts")
        artifacts = []

    paths: set[str] = set()
    artifact_mapping: dict[str, str] = {}
    for artifact in artifacts:
        if not isinstance(artifact, dict):
            errors.append("artifact record")
            continue
        path = artifact.get("path")
        digest = artifact.get("git_blob_sha")
        role = artifact.get("role")
        if not isinstance(path, str) or path.startswith("/") or ".." in Path(path).parts:
            errors.append("artifact path")
            continue
        if path in paths:
            errors.append("duplicate artifact path")
        paths.add(path)
        artifact_mapping[path] = role
        if not isinstance(digest, str) or not SHA40.fullmatch(digest):
            errors.append("artifact pin")
            continue
        try:
            if git_blob_sha(path) != digest:
                errors.append("governed artifact drift")
        except subprocess.CalledProcessError:
            errors.append("missing governed artifact")

    if artifact_mapping != EXPECTED_ARTIFACTS:
        errors.append("governed artifact mapping")

    expected_fixture_paths = {
        path
        for path, role in EXPECTED_ARTIFACTS.items()
        if role in {
            "OBSERVED_SOURCE_STATUS_FIXTURE",
            "SYNTHETIC_VALIDATOR_ONLY_FIXTURE",
        }
    }
    if discovered_source_status_fixture_paths() != expected_fixture_paths:
        errors.append("ungoverned source-status fixture")

    summary = data.get("candidate_summary", {})
    expected_summary = {
        "question_id": "BQ001",
        "question_status": "UNRESOLVED",
        "accepted_edge_count": 0,
        "source_status_fixture_count": 3,
        "synthetic_fixture_count": 1,
        "observed_retraction_claim_count": 0,
    }
    if summary != expected_summary:
        errors.append("candidate summary")

    return sorted(set(errors))


def run_dependencies() -> None:
    commands = [
        [sys.executable, "scripts/validate_v016_readiness.py"],
        [sys.executable, "scripts/validate_source_status_v016.py"],
        [sys.executable, "-m", "unittest", "tests.test_knowledge_graph_beta_v016"],
        [sys.executable, "-m", "pytest", "-q", "tests/test_source_status_v016.py"],
        [sys.executable, "-m", "unittest", "tests.test_v016_release_candidate"],
    ]
    for command in commands:
        result = subprocess.run(command, cwd=ROOT)
        if result.returncode != 0:
            raise AssertionError(f"dependency failed: {' '.join(command[1:])}")


def main() -> int:
    try:
        data = json.loads(MANIFEST.read_text(encoding="utf-8"))
        errors = validate_manifest(data) + validate_repository_binding()
        if errors:
            raise AssertionError(", ".join(errors))
        run_dependencies()
    except (AssertionError, json.JSONDecodeError, OSError) as exc:
        print(f"v0.16-release-candidate: FAIL: {exc}", file=sys.stderr)
        return 1

    print("PASS: v0.16 composite candidate is pinned and review-only")
    print("PENDING: exact-head CI and human merge/release decision")
    print("PASS: BQ001 unresolved; accepted edges and all promotion boundaries remain zero")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
