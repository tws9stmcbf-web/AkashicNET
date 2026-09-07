#!/usr/bin/env python3
"""Validate the public-safe, non-blocking v0.15 CI provenance envelope."""

from __future__ import annotations

import copy
import hashlib
import json
import re
import sys
from datetime import datetime
from pathlib import Path

SCHEMA_VERSION = "0.1"
RECORD_TYPE = "CI_PROVENANCE_ENVELOPE"
SHA1_RE = re.compile(r"[0-9a-f]{40}")
SHA256_RE = re.compile(r"[0-9a-f]{64}")
SAFE_PATH_RE = re.compile(r"[A-Za-z0-9._/-]+")

TOP_LEVEL_KEYS = {
    "schema_version",
    "record_type",
    "scope",
    "generated_at",
    "run",
    "workflow",
    "artifacts",
    "governance",
}
RUN_KEYS = {
    "id",
    "attempt",
    "event",
    "repository",
    "commit_sha",
    "conclusion",
    "url",
}
WORKFLOW_KEYS = {"repository", "file_path", "ref", "sha"}
ARTIFACT_KEYS = {"inputs", "output"}
INPUT_KEYS = {"role", "path", "sha256"}
OUTPUT_KEYS = {"path", "payload_sha256"}
GOVERNANCE = {
    "non_blocking": True,
    "evidence_only": True,
    "automatic_promotion": False,
    "truth_inference": False,
    "rights_promotion": False,
    "scientific_evidence_promotion": False,
    "private_drive_promotion": False,
}
EXPECTED_INPUTS = {
    "release_manifest": "references/community/public-sync-observability-beta-release-manifest-v0.15.json",
    "readiness_validator": "scripts/validate_v015_readiness.py",
}
EXPECTED_OUTPUT = "artifacts/ci-provenance/v015-readiness-envelope.json"
EXPECTED_WORKFLOW_FILE_PATH = ".github/workflows/validate-v015-readiness.yml"


def canonical_payload_sha256(data: dict) -> str:
    payload = copy.deepcopy(data)
    payload["artifacts"]["output"].pop("payload_sha256", None)
    encoded = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def _exact_keys(value: object, expected: set[str], label: str, errors: list[str]) -> None:
    if not isinstance(value, dict) or set(value) != expected:
        errors.append(f"{label} keys must be exactly {sorted(expected)}")


def _safe_repo_path(value: object) -> bool:
    return (
        isinstance(value, str)
        and bool(value)
        and bool(SAFE_PATH_RE.fullmatch(value))
        and not value.startswith(("/", "../"))
        and "/../" not in value
        and "//" not in value
    )


def validate(data: object) -> list[str]:
    errors: list[str] = []
    _exact_keys(data, TOP_LEVEL_KEYS, "top-level", errors)
    if errors:
        return errors
    assert isinstance(data, dict)

    if data["schema_version"] != SCHEMA_VERSION:
        errors.append("schema_version must be 0.1")
    if data["record_type"] != RECORD_TYPE:
        errors.append("record_type mismatch")
    if data["scope"] != "v0.15-readiness":
        errors.append("scope mismatch")
    try:
        timestamp = str(data["generated_at"])
        datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
        if not timestamp.endswith("Z"):
            errors.append("generated_at must be UTC with a Z suffix")
    except ValueError:
        errors.append("generated_at must be RFC 3339")

    run = data["run"]
    _exact_keys(run, RUN_KEYS, "run", errors)
    if isinstance(run, dict) and set(run) == RUN_KEYS:
        if not isinstance(run["id"], int) or run["id"] < 1:
            errors.append("run.id must be a positive integer")
        if not isinstance(run["attempt"], int) or run["attempt"] < 1:
            errors.append("run.attempt must be a positive integer")
        if not SHA1_RE.fullmatch(str(run["commit_sha"])):
            errors.append("run.commit_sha must be a full commit SHA")
        if run["conclusion"] not in {"success", "failure", "cancelled", "skipped"}:
            errors.append("run.conclusion is invalid")
        if not str(run["url"]).startswith("https://github.com/"):
            errors.append("run.url must be a GitHub URL")

    workflow = data["workflow"]
    _exact_keys(workflow, WORKFLOW_KEYS, "workflow", errors)
    if isinstance(workflow, dict) and set(workflow) == WORKFLOW_KEYS:
        if workflow["file_path"] != EXPECTED_WORKFLOW_FILE_PATH:
            errors.append(f"workflow.file_path must be {EXPECTED_WORKFLOW_FILE_PATH}")
        if not SHA1_RE.fullmatch(str(workflow["sha"])):
            errors.append("workflow.sha must be a full commit SHA")

    artifacts = data["artifacts"]
    _exact_keys(artifacts, ARTIFACT_KEYS, "artifacts", errors)
    if isinstance(artifacts, dict) and set(artifacts) == ARTIFACT_KEYS:
        inputs = artifacts["inputs"]
        if not isinstance(inputs, list) or len(inputs) != len(EXPECTED_INPUTS):
            errors.append("artifacts.inputs must contain the two governed inputs")
        else:
            observed = {}
            for item in inputs:
                _exact_keys(item, INPUT_KEYS, "input artifact", errors)
                if isinstance(item, dict) and set(item) == INPUT_KEYS:
                    observed[item["role"]] = item["path"]
                    if not _safe_repo_path(item["path"]):
                        errors.append("input artifact path must be repository-relative")
                    if not SHA256_RE.fullmatch(str(item["sha256"])):
                        errors.append("input artifact sha256 is invalid")
                    elif EXPECTED_INPUTS.get(item["role"]) == item["path"]:
                        try:
                            actual_sha256 = hashlib.sha256((ROOT / item["path"]).read_bytes()).hexdigest()
                        except OSError as exc:
                            errors.append(f"cannot hash governed input {item['path']}: {exc}")
                        else:
                            if item["sha256"] != actual_sha256:
                                errors.append(f"governed input digest mismatch: {item['path']}")
            if observed != EXPECTED_INPUTS:
                errors.append("governed input roles or paths changed")
        output = artifacts["output"]
        _exact_keys(output, OUTPUT_KEYS, "output artifact", errors)
        if isinstance(output, dict) and set(output) == OUTPUT_KEYS:
            if output["path"] != EXPECTED_OUTPUT:
                errors.append("output artifact path changed")
            if output["payload_sha256"] != canonical_payload_sha256(data):
                errors.append("output payload digest mismatch")

    if data["governance"] != GOVERNANCE:
        errors.append("fail-closed governance boundaries changed")

    forbidden = re.compile(r"secret|token|password|credential", re.IGNORECASE)
    for key in _walk_keys(data):
        if forbidden.search(key):
            errors.append(f"forbidden sensitive key: {key}")
    return errors


def _walk_keys(value: object):
    if isinstance(value, dict):
        for key, child in value.items():
            yield str(key)
            yield from _walk_keys(child)
    elif isinstance(value, list):
        for child in value:
            yield from _walk_keys(child)


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: validate_ci_provenance_envelope_v015.py ENVELOPE.json", file=sys.stderr)
        return 2
    path = Path(sys.argv[1])
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"FAIL: cannot read CI provenance envelope: {exc}", file=sys.stderr)
        return 1
    errors = validate(data)
    if errors:
        print("FAIL: CI provenance envelope failed closed:", file=sys.stderr)
        for error in errors:
            print(f" - {error}", file=sys.stderr)
        return 1
    print("PASS: public-safe non-blocking v0.15 CI provenance envelope validates")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
