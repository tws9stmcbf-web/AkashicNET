import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_reddit_source_registry_topic_audit_v0713():
    completed = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "reddit_source_registry_topic_audit_v0713.py")],
        cwd=ROOT, check=True, capture_output=True, text=True,
    )
    result = json.loads(completed.stdout)
    assert result["audited_public_top_level_topic_count"] == 73
    assert result["new_top_level_topics"] == []
    assert result["registry"]["source_count"] == 4
    assert result["registry"]["enabled_sources"] == 4
    assert result["registry"]["post_level_topic_or_flair_fields"] == []
    assert result["guardrails"]["classification_profile_is_topic"] is False


if __name__ == "__main__":
    test_reddit_source_registry_topic_audit_v0713()
    print("Reddit source-registry topic audit v0.7.13 contract: PASS")
