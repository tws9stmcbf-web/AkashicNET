#!/usr/bin/env python3
"""Focused negative tests for the v0.15 CI provenance envelope validator."""

from __future__ import annotations

import hashlib
import sys
import unittest
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import validate_ci_provenance_envelope_v015 as validator  # noqa: E402


def sha256_file(relative_path: str) -> str:
    return hashlib.sha256((ROOT / relative_path).read_bytes()).hexdigest()


def valid_envelope() -> dict:
    data = {
        "schema_version": validator.SCHEMA_VERSION,
        "record_type": validator.RECORD_TYPE,
        "scope": "v0.15-readiness",
        "generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "run": {
            "id": 1,
            "attempt": 1,
            "event": "pull_request",
            "repository": "tws9stmcbf-web/AkashicNET",
            "commit_sha": "a" * 40,
            "conclusion": "success",
            "url": "https://github.com/tws9stmcbf-web/AkashicNET/actions/runs/1",
        },
        "workflow": {
            "repository": "tws9stmcbf-web/AkashicNET",
            "file_path": validator.EXPECTED_WORKFLOW_FILE_PATH,
            "ref": "tws9stmcbf-web/AkashicNET/.github/workflows/validate-v015-readiness.yml@refs/pull/1/merge",
            "sha": "b" * 40,
        },
        "artifacts": {
            "inputs": [
                {"role": role, "path": path, "sha256": sha256_file(path)}
                for role, path in validator.EXPECTED_INPUTS.items()
            ],
            "output": {"path": validator.EXPECTED_OUTPUT, "payload_sha256": ""},
        },
        "governance": validator.GOVERNANCE.copy(),
    }
    data["artifacts"]["output"]["payload_sha256"] = validator.canonical_payload_sha256(data)
    return data


class ProvenanceEnvelopeValidationTests(unittest.TestCase):
    def test_valid_envelope_passes(self) -> None:
        self.assertEqual(validator.validate(valid_envelope()), [])

    def test_stale_governed_input_digest_fails_even_with_recomputed_payload(self) -> None:
        data = valid_envelope()
        data["artifacts"]["inputs"][0]["sha256"] = "0" * 64
        data["artifacts"]["output"]["payload_sha256"] = validator.canonical_payload_sha256(data)
        self.assertTrue(any("governed input digest mismatch" in error for error in validator.validate(data)))

    def test_wrong_workflow_path_fails(self) -> None:
        data = valid_envelope()
        data["workflow"]["file_path"] = ".github/workflows/unrelated.yml"
        data["artifacts"]["output"]["payload_sha256"] = validator.canonical_payload_sha256(data)
        self.assertTrue(any("workflow.file_path must be" in error for error in validator.validate(data)))


if __name__ == "__main__":
    unittest.main()
