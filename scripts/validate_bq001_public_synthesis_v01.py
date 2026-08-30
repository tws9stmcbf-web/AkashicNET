#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BQ = ROOT / "references" / "big-questions" / "BQ001"
SYNTHESIS = BQ / "public-synthesis-v0.1.json"
MARKDOWN = BQ / "PUBLIC_SYNTHESIS.md"
TAXONOMY = ROOT / "references" / "community" / "evidence-taxonomy-v0.10.json"
BATCHES = [BQ / f"evidence-batch{i}-v0.1.json" for i in range(1, 5)]
EXPECTED_SECTION_IDS = {
    "CURRENT_STATUS",
    "WHAT_WE_KNOW",
    "COMPETING_MODELS",
    "EVIDENCE_BY_DOMAIN",
    "CONTRADICTIONS_AND_LIMITS",
    "WHAT_THIS_DOES_NOT_SHOW",
    "OPEN_QUESTIONS",
    "CURRENT_CONCLUSION",
}
EXPECTED_LABELS = {
    "Established Evidence",
    "Interpretation",
    "Lived Experience/Testimony",
    "Hypothesis",
    "Speculation",
}


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def validate(payload: dict) -> None:
    assert payload["question_id"] == "BQ001"
    assert payload["status"] == "UNRESOLVED"
    assert payload["taxonomy_ref"] == "references/community/evidence-taxonomy-v0.10.json"
    assert payload["evidence_batches"] == [
        f"references/big-questions/BQ001/evidence-batch{i}-v0.1.json" for i in range(1, 5)
    ]

    taxonomy = load(TAXONOMY)
    assert set(taxonomy["canonical_labels"]) == EXPECTED_LABELS

    valid_claims = {}
    valid_sources = set()
    for path in BATCHES:
        batch = load(path)
        assert batch["question_id"] == "BQ001"
        assert batch["question_status"] == "UNRESOLVED"
        for source in batch["sources"]:
            valid_sources.add(source["source_id"])
        for claim in batch["claims"]:
            valid_claims[claim["claim_id"]] = claim

    sections = payload["sections"]
    assert {section["section_id"] for section in sections} == EXPECTED_SECTION_IDS
    assert len(sections) == len(EXPECTED_SECTION_IDS)

    for section in sections:
        assert section["summary"].strip()
        claim_ids = section["claim_ids"]
        source_ids = section["source_ids"]
        assert claim_ids and source_ids
        assert len(claim_ids) == len(set(claim_ids))
        assert len(source_ids) == len(set(source_ids))
        for claim_id in claim_ids:
            assert claim_id in valid_claims, f"unsupported claim id: {claim_id}"
        for source_id in source_ids:
            assert source_id in valid_sources, f"unsupported source id: {source_id}"
        traced_sources = {
            source_id
            for claim_id in claim_ids
            for source_id in valid_claims[claim_id]["source_ids"]
        }
        assert set(source_ids) <= traced_sources, f"section source not supported by cited claims: {section['section_id']}"

    guards = payload["guards"]
    assert all(value is False for value in guards.values())

    markdown = MARKDOWN.read_text(encoding="utf-8")
    assert "**Current status: UNRESOLVED**" in markdown
    assert "## What we know" in markdown
    assert "## Competing models" in markdown
    assert "## Evidence by domain" in markdown
    assert "## Contradictions and limits" in markdown
    assert "## What this does not show" in markdown
    assert "## Open questions" in markdown
    assert "## Current conclusion" in markdown
    assert "**UNRESOLVED.**" in markdown
    forbidden = (
        "proves consciousness survives death",
        "proves consciousness cannot survive death",
        "reincarnation is proven",
        "physicalism is proven",
        "dualism is proven",
    )
    lower = markdown.lower()
    for phrase in forbidden:
        assert phrase not in lower


def main() -> int:
    validate(load(SYNTHESIS))
    print("BQ001 PUBLIC SYNTHESIS v0.1 PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
