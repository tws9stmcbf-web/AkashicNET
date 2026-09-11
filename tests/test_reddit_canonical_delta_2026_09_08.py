import hashlib
import json
import subprocess
import sys
from pathlib import Path

import pytest

from scripts import validate_reddit_canonical_delta_2026_09_08 as validator

ROOT = Path(__file__).resolve().parents[1]


def _run():
    completed = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "validate_reddit_canonical_delta_2026_09_08.py")],
        cwd=ROOT, check=True, capture_output=True, text=True,
    )
    return json.loads(completed.stdout)


def test_reddit_canonical_delta_2026_09_08_all_candidates_accepted():
    result = _run()
    assert result["candidates_reviewed"] == 10
    assert result["already_present"] == []
    assert result["rejected"] == []
    assert result["held"] == []
    assert len(result["accepted"]) == 10
    assert result["unique_reddit_post_ids"] == 10
    assert result["unique_canonical_urls"] == 10


def test_reddit_canonical_delta_2026_09_08_field_allowlist():
    result = _run()
    assert set(result["record_fields"]) == {
        "reddit_post_id", "canonical_url", "subreddit", "title",
        "created_utc", "availability_status", "retrieved_at_utc",
        "provenance", "import_status",
    }
    forbidden = {
        "author", "username", "body", "comments", "score", "upvote_ratio",
        "num_comments", "flair", "link_flair_text", "topic", "category",
    }
    assert forbidden.isdisjoint(result["record_fields"])


def _first_delta_record():
    delta_path = (
        ROOT / "references" / "community" / "reddit-canonical-delta-import-2026-09-08.json"
    )
    delta = json.loads(delta_path.read_text(encoding="utf-8"))
    return dict(delta["records"][0])


def test_reddit_canonical_delta_2026_09_08_requires_every_allowed_field():
    record = _first_delta_record()
    record.pop("title")

    with pytest.raises(ValueError, match="exactly match allow-list"):
        validator.validate_record(record)


def test_reddit_canonical_delta_2026_09_08_permalink_id_matches_record():
    record = _first_delta_record()
    record["canonical_url"] = record["canonical_url"].replace(
        record["reddit_post_id"], "1mismatched"
    )

    with pytest.raises(ValueError, match="post ID does not match"):
        validator.validate_record(record)


def test_reddit_canonical_delta_2026_09_08_partial_coverage_and_no_public_count_change():
    result = _run()
    assert result["coverage"] == "partial_manual"
    assert result["public_count_promoted"] is False


def test_reddit_canonical_delta_2026_09_08_guardrails_hold_reddit_api():
    result = _run()
    guardrails = result["guardrails"]
    assert guardrails["reddit_api_called"] is False
    assert guardrails["reddit_api_approved_enabled"] is False
    assert guardrails["credentials_used"] is False
    assert guardrails["crawled_or_paginated"] is False
    assert guardrails["truth_inference"] is False
    assert guardrails["rights_promotion"] is False
    assert guardrails["scientific_evidence_promotion"] is False


def test_reddit_canonical_delta_2026_09_08_sealed_2026_09_02_delta_untouched():
    prior_path = (
        ROOT / "references" / "community" / "reddit-canonical-delta-import-2026-09-02.json"
    )
    assert hashlib.sha256(prior_path.read_bytes()).hexdigest() == (
        "edb59e8142183a7be57f81ced62c0e411eb5158ca1bed1276c78980a5832e667"
    )


if __name__ == "__main__":
    test_reddit_canonical_delta_2026_09_08_all_candidates_accepted()
    test_reddit_canonical_delta_2026_09_08_field_allowlist()
    test_reddit_canonical_delta_2026_09_08_partial_coverage_and_no_public_count_change()
    test_reddit_canonical_delta_2026_09_08_guardrails_hold_reddit_api()
    test_reddit_canonical_delta_2026_09_08_sealed_2026_09_02_delta_untouched()
    print("Reddit canonical-delta 2026-09-08 manual import contract: PASS")
