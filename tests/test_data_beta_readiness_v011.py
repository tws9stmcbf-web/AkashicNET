from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "audit_data_beta_readiness_v011.py"
FIXTURE = ROOT / "references" / "community" / "data-beta-readiness-v0.11.json"


def load_module():
    spec = importlib.util.spec_from_file_location("audit_data_beta_readiness_v011", SCRIPT)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_readiness_audit_is_internally_consistent_and_blocked():
    module = load_module()
    errors, summary = module.audit()
    assert errors == []
    assert summary["audit_state"] == "BLOCKED"
    assert summary["knowledge_data_beta_ready"] is False
    assert summary["required_gate_count"] == 11
    assert summary["completed_required_gates"] == 10
    assert summary["release_blockers"] == ["historical_reddit_denominator_documented"]


def test_beta_is_not_declared_while_release_blockers_remain():
    data = json.loads(FIXTURE.read_text(encoding="utf-8"))
    assert data["knowledge_data_beta_declared"] is False
    assert data["release_blockers"]
    for blocker in data["release_blockers"]:
        assert data["required_gates"][blocker] is False


def test_fail_closed_invariants_remain_false():
    data = json.loads(FIXTURE.read_text(encoding="utf-8"))
    assert data["invariants"]
    assert all(value is False for value in data["invariants"].values())


def test_api_verification_is_nonblocking_but_cannot_be_fabricated():
    data = json.loads(FIXTURE.read_text(encoding="utf-8"))
    debt = " ".join(data["nonblocking_debt"])
    assert "Universal Reddit API verification is not required" in debt
    assert data["invariants"]["api_unverified_records_may_be_labelled_api_verified"] is False
