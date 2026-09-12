import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts import validate_reddit_canonical_delta_2026_09_08 as validator  # noqa: E402


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


def _assert_exception(exception_type, call, message):
    try:
        call()
    except exception_type as exc:
        assert message in str(exc)
    else:
        raise AssertionError(f"expected {exception_type.__name__}")


def test_reddit_canonical_delta_2026_09_08_requires_every_allowed_field():
    record = _first_delta_record()
    record.pop("title")

    _assert_exception(
        ValueError,
        lambda: validator.validate_record(record, "NeuronsToNirvana"),
        "exactly match allow-list",
    )


def test_reddit_canonical_delta_2026_09_08_permalink_id_matches_record():
    record = _first_delta_record()
    record["canonical_url"] = record["canonical_url"].replace(
        record["reddit_post_id"], "1mismatched"
    )

    _assert_exception(
        ValueError,
        lambda: validator.validate_record(record, "NeuronsToNirvana"),
        "post ID does not match",
    )


def test_reddit_canonical_delta_2026_09_08_rejects_non_normalized_post_id():
    record = _first_delta_record()
    record["reddit_post_id"] = record["reddit_post_id"].upper()
    record["canonical_url"] = record["canonical_url"].replace(
        record["canonical_url"].split("/comments/", 1)[1].split("/", 1)[0],
        record["reddit_post_id"],
    )

    _assert_exception(
        ValueError,
        lambda: validator.validate_record(record, "NeuronsToNirvana"),
        "lowercase base-36 string",
    )


def test_reddit_canonical_delta_2026_09_08_validates_metadata_values():
    cases = {
        "title": ("   ", "title must be a non-empty string"),
        "created_utc": ("2026-09-07", "created_utc must be an ISO 8601"),
        "retrieved_at_utc": ("2026-09-07T00:00:00Z", "retrieved_at_utc must be an ISO 8601 date"),
        "availability_status": ("unknown", "availability_status must be"),
        "provenance": ("reddit_api", "provenance must be"),
        "import_status": ("ACCEPTED", "import_status must be"),
    }
    for field, (value, message) in cases.items():
        record = _first_delta_record()
        record[field] = value
        _assert_exception(
            ValueError,
            lambda record=record: validator.validate_record(
                record, "NeuronsToNirvana"
            ),
            message,
        )

    record = _first_delta_record()
    record["retrieved_at_utc"] = "2026-09-06"
    _assert_exception(
        ValueError,
        lambda: validator.validate_record(record, "NeuronsToNirvana"),
        "created_utc must not be later",
    )


def test_reddit_canonical_delta_2026_09_08_reconciles_scope_counts():
    scope = {
        "candidates_reviewed": 10,
        "already_present_in_canonical_index": 0,
        "accepted_new_records": 9,
        "rejected_records": 0,
        "held_records": 0,
    }
    _assert_exception(
        SystemExit,
        lambda: validator.validate_scope_counts(
            scope,
            candidates_reviewed=10,
            already_present=0,
            accepted=10,
            rejected=0,
            held=0,
        ),
        "accepted_new_records must equal computed count 10",
    )


def test_reddit_canonical_delta_2026_09_08_requires_audit_checkpoint():
    original_checkpoint_path = validator.CHECKPOINT_PATH
    validator.CHECKPOINT_PATH = ROOT / "missing-reddit-delta-audit-checkpoint.json"
    try:
        _assert_exception(
            SystemExit,
            validator.load_checkpoint,
            "required checked-in audit checkpoint is missing",
        )
    finally:
        validator.CHECKPOINT_PATH = original_checkpoint_path


def test_reddit_canonical_delta_2026_09_08_subreddit_matches_permalink_and_scope():
    record = _first_delta_record()
    record["subreddit"] = "DifferentSubreddit"
    _assert_exception(
        ValueError,
        lambda: validator.validate_record(record, "NeuronsToNirvana"),
        "permalink subreddit does not match",
    )

    record = _first_delta_record()
    _assert_exception(
        ValueError,
        lambda: validator.validate_record(record, "DifferentSubreddit"),
        "does not match declared scope",
    )


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
    test_reddit_canonical_delta_2026_09_08_requires_every_allowed_field()
    test_reddit_canonical_delta_2026_09_08_permalink_id_matches_record()
    test_reddit_canonical_delta_2026_09_08_rejects_non_normalized_post_id()
    test_reddit_canonical_delta_2026_09_08_validates_metadata_values()
    test_reddit_canonical_delta_2026_09_08_reconciles_scope_counts()
    test_reddit_canonical_delta_2026_09_08_requires_audit_checkpoint()
    test_reddit_canonical_delta_2026_09_08_subreddit_matches_permalink_and_scope()
    test_reddit_canonical_delta_2026_09_08_partial_coverage_and_no_public_count_change()
    test_reddit_canonical_delta_2026_09_08_guardrails_hold_reddit_api()
    test_reddit_canonical_delta_2026_09_08_sealed_2026_09_02_delta_untouched()
    print("Reddit canonical-delta 2026-09-08 manual import contract: PASS")
