import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_reddit_canonical_delta_topic_audit_v0714():
    completed = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "reddit_canonical_delta_topic_audit_v0714.py")],
        cwd=ROOT, check=True, capture_output=True, text=True,
    )
    result = json.loads(completed.stdout)
    assert result["audited_public_top_level_topic_count"] == 73
    assert result["new_top_level_topics"] == []
    assert result["batch"]["records"] == 101
    assert result["batch"]["unique_reddit_post_ids"] == 101
    assert result["batch"]["unique_canonical_urls"] == 101
    assert result["batch"]["explicit_topic_category_or_flair_fields"] == []
    assert result["guardrails"]["url_inference"] is False


if __name__ == "__main__":
    test_reddit_canonical_delta_topic_audit_v0714()
    print("Reddit canonical-delta topic audit v0.7.14 contract: PASS")
