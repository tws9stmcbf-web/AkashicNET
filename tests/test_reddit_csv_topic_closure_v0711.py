import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_reddit_csv_topic_closure_v0711():
    completed = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "reddit_csv_topic_closure_v0711.py")],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    result = json.loads(completed.stdout)
    assert result["audited_public_top_level_topic_count"] == 73
    assert result["new_top_level_topics"] == []
    assert result["remaining_source_counts"]["n2n_test_batch_rows"] == 25
    assert result["remaining_source_counts"]["manual_delta_rows"] == 132
    assert result["coverage"]["reddit_csv_explicit_topic_audit"] == "complete"
    assert result["guardrails"]["url_slug_inference"] is False


if __name__ == "__main__":
    test_reddit_csv_topic_closure_v0711()
    print("reddit CSV topic closure v0.7.11 contract: PASS")
