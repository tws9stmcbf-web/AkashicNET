import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_reddit_corroboration_topic_audit_v0715():
    completed = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "reddit_corroboration_topic_audit_v0715.py")],
        cwd=ROOT, check=True, capture_output=True, text=True,
    )
    result = json.loads(completed.stdout)
    assert result["audited_public_top_level_topic_count"] == 73
    assert result["new_top_level_topics"] == []
    assert result["series"]["record_counts"]["0.6"] == 39
    assert result["series"]["explicit_topic_category_or_flair_fields"] == []
    transition = result["series"]["transitions"]["v0.5_to_v0.6"]
    assert transition["added"] == 5
    assert transition["removed"] == 4
    assert transition["cumulative"] is False
    assert result["guardrails"]["presence_is_topic_evidence"] is False


if __name__ == "__main__":
    test_reddit_corroboration_topic_audit_v0715()
    print("Reddit corroboration topic audit v0.7.15 contract: PASS")
