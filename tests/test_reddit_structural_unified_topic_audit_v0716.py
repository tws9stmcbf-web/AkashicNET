import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_reddit_structural_unified_topic_audit_v0716():
    completed = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "reddit_structural_unified_topic_audit_v0716.py")],
        cwd=ROOT, check=True, capture_output=True, text=True,
    )
    result = json.loads(completed.stdout)
    rec = result["reconciliation"]
    assert result["audited_public_top_level_topic_count"] == 73
    assert result["new_top_level_topics"] == []
    assert rec["reddit_source_rows"] + rec["drive_source_rows"] == rec["current_unified_index_records"]
    assert rec["net_change"] == 101
    assert rec["unique_reddit_post_ids_all_subreddits"] == 7457
    assert rec["explicit_topic_category_or_flair_fields"] == []
    assert result["guardrails"]["counts_are_topics"] is False


if __name__ == "__main__":
    test_reddit_structural_unified_topic_audit_v0716()
    print("Reddit structural/unified topic audit v0.7.16 contract: PASS")
