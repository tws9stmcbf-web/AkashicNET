import copy
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.reddit_topic_census_seal_v0718 import load_documents, validate_chain


def expect_rejected(documents):
    try:
        validate_chain(documents)
    except ValueError:
        return
    raise AssertionError("invalid checkpoint chain was accepted")


def test_reddit_topic_census_seal_v0718():
    completed = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "reddit_topic_census_seal_v0718.py")],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    result = json.loads(completed.stdout)
    assert result["status"] == "REDDIT_TOPIC_CENSUS_SEALED"
    assert result["previous_sealed_public_top_level_topic_count"] == 71
    assert result["audited_public_top_level_topic_count"] == 73
    assert result["promoted_top_level_topics"] == ["meaning-making", "unity"]
    assert result["coverage"]["checkpoint_count"] == 10
    assert result["coverage"]["explicit_topic_coverage"] == "complete_for_current_governed_reddit_sources"
    assert result["guardrails"]["new_source_requires_reaudit"] is True


def test_count_drift_fails_closed():
    documents = copy.deepcopy(load_documents())
    documents["0.7.16"]["audited_public_top_level_topic_count"] = 74
    expect_rejected(documents)


def test_governance_drift_fails_closed():
    documents = copy.deepcopy(load_documents())
    documents["0.7.17"]["guardrails"]["truth_inference"] = True
    expect_rejected(documents)


if __name__ == "__main__":
    test_reddit_topic_census_seal_v0718()
    test_count_drift_fails_closed()
    test_governance_drift_fails_closed()
    print("Reddit topic census seal v0.7.18 contract: PASS")
