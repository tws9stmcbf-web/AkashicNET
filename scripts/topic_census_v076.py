#!/usr/bin/env python3
"""Candidate expansion of the AkashicNET deterministic public topic census.

The sealed v0.7.5 count remains unchanged. This checkpoint adds only the
reproducibly public Wikipedia pilot topic_seed field and reports the resulting
candidate lower bound for review.
"""
from __future__ import annotations

import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMMUNITY = ROOT / "references" / "community"

WIKISPINE_FILES = [
    "wikispine-seed-v0.7.0.json",
    "wikispine-batch-a-v0.7.1.json",
    "wikispine-batch-b-v0.7.1.json",
    "wikispine-batch-c-v0.7.2.json",
    "wikispine-batch-d-v0.7.2.json",
    "wikispine-batch-e-science-v0.7.3.json",
    "wikispine-batch-f-v0.7.4.json",
]
ONTOLOGY_FILE = "concept-seed-v0.20.csv"
N2N_FILE = "n2n-pilot-index.csv"
WIKIPEDIA_FILE = "wikipedia-akashic-pilot.csv"

ALIASES = {
    "qabbalah": "kabbalah",
    "quabbalah": "kabbalah",
    "cabala": "kabbalah",
    "contemplative practice": "meditation",
    "psychedelic": "psychedelics",
}


def norm(label: str) -> str:
    value = label.strip().lower().replace("&", " and ")
    value = re.sub(r"[^a-z0-9]+", " ", value)
    value = re.sub(r"\s+", " ", value).strip()
    return ALIASES.get(value, value)


def csv_values(name: str, column: str) -> list[str]:
    with (COMMUNITY / name).open(newline="", encoding="utf-8") as handle:
        return [
            row[column].strip()
            for row in csv.DictReader(handle)
            if row.get(column, "").strip()
        ]


def records_from_json(value):
    if isinstance(value, dict):
        for key in ("records", "resolved_records"):
            if isinstance(value.get(key), list):
                return value[key]
    return []


def wikispine_values() -> list[str]:
    values = []
    for name in WIKISPINE_FILES:
        data = json.loads((COMMUNITY / name).read_text(encoding="utf-8"))
        for record in records_from_json(data):
            label = (
                record.get("akashic_concept")
                or record.get("concept")
                or record.get("label")
                or ""
            ).strip()
            if label:
                values.append(label)
    return values


def main() -> int:
    baseline_sources = {
        "reviewed_ontology": {norm(x) for x in csv_values(ONTOLOGY_FILE, "label")},
        "wikispine": {norm(x) for x in wikispine_values()},
        "n2n_metadata_categories": {norm(x) for x in csv_values(N2N_FILE, "category")},
    }
    baseline = set().union(*baseline_sources.values())
    wikipedia = {norm(x) for x in csv_values(WIKIPEDIA_FILE, "topic_seed")}
    expanded = baseline | wikipedia
    additions = sorted(wikipedia - baseline)

    if len(baseline) != 68:
        raise SystemExit(f"sealed baseline drift: expected 68, found {len(baseline)}")
    if additions != ["anthropology", "archaeology", "mycology", "quantum physics"]:
        raise SystemExit(f"unexpected candidate additions: {additions}")
    if len(expanded) != 72:
        raise SystemExit(f"candidate census drift: expected 72, found {len(expanded)}")

    result = {
        "version": "0.7.6",
        "status": "CANDIDATE_REVIEW_CHECKPOINT",
        "sealed_public_count": 68,
        "candidate_reproducible_lower_bound": 72,
        "new_candidate_topics": additions,
        "source_counts": {
            **{key: len(value) for key, value in baseline_sources.items()},
            "wikipedia_topic_seeds": len(wikipedia),
        },
        "promotion_state": "NOT_PROMOTED",
        "required_next_gate": "canonical topic review and explicit approval",
        "guardrails": {
            "semantic_similarity_auto_merge": False,
            "people_are_topics": False,
            "works_are_topics": False,
            "document_count_is_topic_count": False,
            "private_drive_labels_included": False,
            "truth_inference": False,
            "rights_promotion": False,
            "scientific_evidence_promotion": False,
        },
    }
    print(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
