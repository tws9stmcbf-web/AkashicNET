import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_topic_census_promoted_v077():
    completed = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "topic_census_v077.py")],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    result = json.loads(completed.stdout)
    assert result["previous_sealed_public_count"] == 68
    assert result["audited_public_top_level_topic_count"] == 71
    assert result["promotion_state"] == "PROMOTED"
    assert result["new_top_level_topics"] == ["anthropology", "archaeology", "mycology"]
    assert result["canonical_relationships"]["quantum physics"]["narrower_child_concepts"] == ["quantum mechanics"]
    assert result["guardrails"]["semantic_similarity_auto_merge"] is False
    assert result["guardrails"]["private_drive_labels_included"] is False


if __name__ == "__main__":
    test_topic_census_promoted_v077()
    print("topic census promoted v0.7.7 contract: PASS")
