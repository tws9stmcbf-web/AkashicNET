import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_reddit_topic_promotion_v0710():
    completed = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "reddit_topic_promotion_v0710.py")],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    result = json.loads(completed.stdout)
    assert result["previous_public_top_level_topic_count"] == 71
    assert result["audited_public_top_level_topic_count"] == 73
    assert result["promoted_top_level_topics"] == ["meaning-making", "unity"]
    assert result["canonical_child_relationships"]["selfhood"] == ["ego"]
    assert result["canonical_child_relationships"]["cognition"] == ["symbolic memory"]
    assert result["promotion_state"] == "PROMOTED"
    assert result["guardrails"]["url_slug_inference"] is False


if __name__ == "__main__":
    test_reddit_topic_promotion_v0710()
    print("reddit topic promotion v0.7.10 contract: PASS")
