import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_reddit_topic_review_v079():
    completed = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "reddit_topic_review_v079.py")],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    result = json.loads(completed.stdout)
    assert result["sealed_public_top_level_topic_count"] == 71
    assert result["recommended_candidate_count"] == 73
    assert result["recommended_new_top_level_topics"] == ["meaning-making", "unity"]
    assert result["recommended_child_relationships"]["selfhood"] == ["ego"]
    assert result["promotion_state"] == "NOT_PROMOTED"
    assert result["guardrails"]["comma_token_auto_promotion"] is False


if __name__ == "__main__":
    test_reddit_topic_review_v079()
    print("reddit topic canonical review v0.7.9 contract: PASS")
