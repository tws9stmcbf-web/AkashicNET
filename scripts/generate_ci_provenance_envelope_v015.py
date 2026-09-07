#!/usr/bin/env python3
"""Generate a durable evidence-only envelope for the v0.15 readiness run."""

from __future__ import annotations

import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path

from validate_ci_provenance_envelope_v015 import (
    EXPECTED_INPUTS,
    EXPECTED_OUTPUT,
    GOVERNANCE,
    canonical_payload_sha256,
    validate,
)

ROOT = Path(__file__).resolve().parents[1]


def required_env(name: str) -> str:
    value = os.environ.get(name, "").strip()
    if not value:
        raise SystemExit(f"FAIL: required CI identity field is empty: {name}")
    return value


def sha256_file(relative_path: str) -> str:
    return hashlib.sha256((ROOT / relative_path).read_bytes()).hexdigest()


def main() -> int:
    generated_at = os.environ.get("AKASHIC_CI_GENERATED_AT") or datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    inputs = [
        {"role": role, "path": path, "sha256": sha256_file(path)}
        for role, path in EXPECTED_INPUTS.items()
    ]
    data = {
        "schema_version": "0.1",
        "record_type": "CI_PROVENANCE_ENVELOPE",
        "scope": "v0.15-readiness",
        "generated_at": generated_at,
        "run": {
            "id": int(required_env("GITHUB_RUN_ID")),
            "attempt": int(required_env("GITHUB_RUN_ATTEMPT")),
            "event": required_env("GITHUB_EVENT_NAME"),
            "repository": required_env("GITHUB_REPOSITORY"),
            "commit_sha": required_env("GITHUB_SHA"),
            "conclusion": required_env("AKASHIC_READINESS_CONCLUSION"),
            "url": f"{required_env('GITHUB_SERVER_URL')}/{required_env('GITHUB_REPOSITORY')}/actions/runs/{required_env('GITHUB_RUN_ID')}",
        },
        "workflow": {
            "repository": required_env("AKASHIC_WORKFLOW_REPOSITORY"),
            "file_path": required_env("AKASHIC_WORKFLOW_FILE_PATH"),
            "ref": required_env("AKASHIC_WORKFLOW_REF"),
            "sha": required_env("AKASHIC_WORKFLOW_SHA"),
        },
        "artifacts": {
            "inputs": inputs,
            "output": {"path": EXPECTED_OUTPUT, "payload_sha256": ""},
        },
        "governance": GOVERNANCE,
    }
    data["artifacts"]["output"]["payload_sha256"] = canonical_payload_sha256(data)
    errors = validate(data)
    if errors:
        raise SystemExit("FAIL: generated envelope is invalid: " + "; ".join(errors))
    output = ROOT / EXPECTED_OUTPUT
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"PASS: wrote {EXPECTED_OUTPUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
