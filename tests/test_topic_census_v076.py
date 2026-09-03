import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_topic_census_candidate_v076():
    completed = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "topic_census_v076.py")],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    result = json.loads(completed.stdout)
    assert result["sealed_public_count"] == 68
    assert result["candidate_reproducible_lower_bound"] == 72
    assert result["promotion_state"] == "NOT_PROMOTED"
    assert result["new_candidate_topics"] == [
        "anthropology",
        "archaeology",
        "mycology",
        "quantum physics",
    ]
    assert result["guardrails"]["private_drive_labels_included"] is False
    assert result["guardrails"]["semantic_similarity_auto_merge"] is False


if __name__ == "__main__":
    test_topic_census_candidate_v076()
    print("topic census candidate v0.7.6 contract: PASS")
