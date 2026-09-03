import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_reddit_markdown_topic_closure_v0717():
    completed = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "reddit_markdown_topic_closure_v0717.py")],
        cwd=ROOT, check=True, capture_output=True, text=True,
    )
    result = json.loads(completed.stdout)
    coverage = result["coverage"]
    assert result["audited_public_top_level_topic_count"] == 73
    assert result["new_top_level_topics"] == []
    assert coverage["source_bearing_markdown_documents"] == 10
    assert coverage["explicit_topic_category_or_flair_declarations"] == {}
    assert coverage["markdown_explicit_topic_audit"] == "complete"
    assert result["guardrails"]["method_document_is_source_evidence"] is False


if __name__ == "__main__":
    test_reddit_markdown_topic_closure_v0717()
    print("Reddit Markdown topic closure v0.7.17 contract: PASS")
