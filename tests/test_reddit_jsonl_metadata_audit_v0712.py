import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_reddit_jsonl_metadata_audit_v0712():
    completed = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "reddit_jsonl_metadata_audit_v0712.py")],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    result = json.loads(completed.stdout)
    assert result["audited_public_top_level_topic_count"] == 73
    assert result["new_top_level_topics"] == []
    assert result["batch"]["records"] == 25
    assert result["batch"]["unique_reddit_post_ids"] == 25
    assert result["batch"]["distinct_normalized_categories"] == 12
    assert result["batch"]["reddit_native_topic_or_flair_fields"] == []
    assert result["lineage"]["same_reddit_url_set"] is True
    assert result["lineage"]["independent_topic_evidence"] is False
    assert result["guardrails"]["title_inference"] is False


if __name__ == "__main__":
    test_reddit_jsonl_metadata_audit_v0712()
    print("Reddit JSONL metadata audit v0.7.12 contract: PASS")
