"""Preserve the historical observation and the independently authored appendix.

These byte pins were established from f3d3c99 and the append-only 9cf967a
diff, not regenerated from whatever document happens to be current.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = "research/microdosing-research-2026.md"
APPENDIX = "research/rat-psilocybin-5ht2a-2026.md"
HISTORICAL_BLOB = "05b14477d17edafdfcb80481f134848066cd3a2a"
OCTOBER_BLOB = "14abd8c56074af6d361818c82bd13ccf736cf7be"


def git_blob(raw: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()


def test_historical_source_bytes_preserved():
    assert git_blob((ROOT / SOURCE).read_bytes()) == HISTORICAL_BLOB


def test_relocated_appendix_is_lossless():
    historical = (ROOT / SOURCE).read_bytes()
    appendix = (ROOT / APPENDIX).read_bytes()
    assert hashlib.sha256(appendix).hexdigest() == (
        "658d1ee20a6500b988a2780d8e373d2cde041bf831b5ba2f666ae99685b7dc16"
    )
    # Reconstruct the exact October document: catches dropped qualifications,
    # missing text, and substitutions in either scientific record.
    assert git_blob(historical + appendix) == OCTOBER_BLOB


def test_fixture_and_event_are_not_rebound_or_promoted():
    raw = (ROOT / "references/source-status-fixture-v0.16.json").read_bytes()
    assert git_blob(raw) == "1b19312035d6d9bc763c645d70139989fdd05c53"
    fixture = json.loads(raw)
    node = next(n for n in fixture["source_nodes"]
                if n["source_node_id"] == "SRC-MICRODOSING-PETRANKER-2026")
    event = next(e for e in fixture["events"]
                 if e["source_node_id"] == node["source_node_id"])
    assert node["input_path"] == SOURCE
    assert node["input_blob_sha"] == event["input_blob_sha"] == HISTORICAL_BLOB
    assert node["original_url"] == event["original_url"] == (
        "https://doi.org/10.1016/j.drugpo.2026.105459"
    )
    assert event["retrieved_at"] == "2026-09-02"
    assert event["status"] == "UNAVAILABLE_INDETERMINATE"
    assert event["human_review_state"] == "REVIEWED_NO_PROMOTION"
    assert event["truth_inference"] == "NONE"
    assert event["promotion_applied"] is False
    assert all(value is False for value in fixture["promotion_guards"].values())
