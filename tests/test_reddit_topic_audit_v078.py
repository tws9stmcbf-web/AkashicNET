import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_reddit_topic_audit_v078():
    completed = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "reddit_topic_audit_v078.py")],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    result = json.loads(completed.stdout)
    assert result["sealed_public_top_level_topic_count"] == 71
    assert result["automatically_promotable_topics_from_uri_and_semantic_indexes"] == 0
    assert result["source_counts"]["reddit_uri_rows"] == 9502
    assert result["source_counts"]["reddit_semantic_rows"] == 9401
    assert result["source_counts"]["n2n_pilot_categories"] == 15
    assert len(result["held_explicit_topic_cells"]) == 3
    assert result["promotion_state"] == "NO_COUNT_CHANGE"
    assert result["guardrails"]["url_slug_inference"] is False


if __name__ == "__main__":
    test_reddit_topic_audit_v078()
    print("reddit topic-source audit v0.7.8 contract: PASS")
