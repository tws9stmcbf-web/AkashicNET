import copy
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tools" / "validate_public_beta_status.py"
spec = importlib.util.spec_from_file_location("public_beta_status", SCRIPT)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def latest_aggregate():
    path = mod.latest_wikispine_aggregate()
    return json.loads(path.read_text(encoding="utf-8"))


def current_readme():
    return (ROOT / "README.md").read_text(encoding="utf-8")


def deliberately_stale_aggregate(aggregate: dict) -> dict:
    """Build a valid but one-version-behind snapshot without hard-coding counts."""
    stale = copy.deepcopy(aggregate)
    assert stale["resolved_high_precision"] > 0
    assert stale["resolved_by_type"]["WORK"] > 0
    stale["resolved_high_precision"] -= 1
    stale["resolved_by_type"]["WORK"] -= 1
    stale["pending_resolution"] = 1
    stale["pending_entities"] = [
        {
            "akashic_entity": "Synthetic stale reference",
            "entity_type": "WORK",
            "resolution_state": "PENDING_VERIFIED_QID",
        }
    ]
    return stale


def test_current_readme_matches_latest_wikispine_aggregate():
    assert mod.validate(current_readme(), latest_aggregate()) == []


def test_stale_publication_snapshot_fails_closed():
    aggregate = latest_aggregate()
    snapshot, _ = mod.expected_wikispine_tokens(aggregate)
    stale_snapshot, _ = mod.expected_wikispine_tokens(deliberately_stale_aggregate(aggregate))
    text = current_readme().replace(snapshot, stale_snapshot)
    failures = mod.validate(text, aggregate)
    assert any("publication snapshot mismatch" in item for item in failures)


def test_stale_milestone_snapshot_fails_closed():
    aggregate = latest_aggregate()
    _, milestone = mod.expected_wikispine_tokens(aggregate)
    _, stale_milestone = mod.expected_wikispine_tokens(deliberately_stale_aggregate(aggregate))
    text = current_readme().replace(milestone, stale_milestone)
    failures = mod.validate(text, aggregate)
    assert any("milestone snapshot mismatch" in item for item in failures)


def test_inconsistent_aggregate_counts_fail_closed():
    aggregate = latest_aggregate()
    aggregate["resolved_high_precision"] += 1
    try:
        mod.expected_wikispine_tokens(aggregate)
    except AssertionError:
        pass
    else:
        raise AssertionError("expected inconsistent aggregate counts to fail closed")


def test_promotion_gate_regression_is_rejected():
    aggregate = latest_aggregate()
    text = current_readme().replace("Truth inference: OFF", "Truth inference: ON")
    failures = mod.validate(text, aggregate)
    assert any("truth gate" in item for item in failures)
    assert any("forbidden status: Truth inference: ON" in item for item in failures)
