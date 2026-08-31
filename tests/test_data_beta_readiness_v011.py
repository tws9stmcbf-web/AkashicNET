from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "audit_data_beta_readiness_v011.py"
FIXTURE = ROOT / "references" / "community" / "data-beta-readiness-v0.11.json"
CHECKPOINT = ROOT / "references" / "community" / "reddit-corpus-structural-checkpoint-v0.2.json"
README = ROOT / "README.md"


def load_module():
    spec = importlib.util.spec_from_file_location("audit_data_beta_readiness_v011", SCRIPT)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_readiness_audit_is_internally_consistent_and_ready():
    module = load_module()
    errors, summary = module.audit()
    assert errors == []
    assert summary["audit_state"] == "READY"
    assert summary["knowledge_data_beta_ready"] is True
    assert summary["required_gate_count"] == 11
    assert summary["completed_required_gates"] == 11
    assert summary["release_blockers"] == []


def test_beta_is_declared_only_after_all_required_gates_are_complete():
    data = json.loads(FIXTURE.read_text(encoding="utf-8"))
    assert data["knowledge_data_beta_declared"] is True
    assert data["release_blockers"] == []
    assert all(data["required_gates"].values())


def test_documented_denominator_matches_structural_checkpoint():
    data = json.loads(FIXTURE.read_text(encoding="utf-8"))
    checkpoint = json.loads(CHECKPOINT.read_text(encoding="utf-8"))
    readme = README.read_text(encoding="utf-8")
    assert data["required_gates"]["historical_reddit_denominator_documented"] is True
    assert f"**{checkpoint['source_rows']:,} source rows**" in readme
    assert f"**{checkpoint['unique_post_ids_all_subreddits']:,} unique Reddit post IDs / canonical post URLs across all archived subreddits**" in readme
    assert f"**{checkpoint['unique_post_ids_by_subreddit']['NeuronsToNirvana']:,} unique r/NeuronsToNirvana post IDs**" in readme
    assert "not Reddit API verification" in readme


def test_fail_closed_invariants_remain_false():
    data = json.loads(FIXTURE.read_text(encoding="utf-8"))
    assert data["invariants"]
    assert all(value is False for value in data["invariants"].values())


def test_api_verification_is_nonblocking_but_cannot_be_fabricated():
    data = json.loads(FIXTURE.read_text(encoding="utf-8"))
    debt = " ".join(data["nonblocking_debt"])
    assert "Universal Reddit API verification is not required" in debt
    assert data["invariants"]["api_unverified_records_may_be_labelled_api_verified"] is False
