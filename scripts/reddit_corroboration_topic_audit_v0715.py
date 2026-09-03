#!/usr/bin/env python3
"""Audit Reddit corroboration seed lineage for explicit topic fields."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMMUNITY = ROOT / "references" / "community"
VERSIONS = ("0.3", "0.4", "0.5", "0.6")
EXPECTED_COUNTS = {"0.3": 20, "0.4": 29, "0.5": 38, "0.6": 39}
EXPECTED_ADDED_06 = ["10a8yeh", "11rok7i", "12v43s7", "1d50iie", "1hij76m"]
EXPECTED_REMOVED_06 = ["1pczj8w", "1proj4m", "1r3tngh", "1vn54g4"]
EXPECTED_FIELDS = {"post_id", "subreddit"}
EXPECTED_DOCUMENT_FIELDS = {"notes", "records", "schema", "source_type"}
TOPIC_FIELDS = {
    "topic", "topics", "category", "categories", "flair",
    "link_flair_text", "link_flair_template_id",
}


def pair(record):
    return (record["subreddit"], record["post_id"])


def main() -> int:
    data = {}
    sets = {}
    for version in VERSIONS:
        path = COMMUNITY / f"reddit-corroboration-seed-v{version}.json"
        payload = json.loads(path.read_text(encoding="utf-8"))
        if set(payload) != EXPECTED_DOCUMENT_FIELDS:
            raise SystemExit(f"v{version} document-field drift: {sorted(payload)}")
        records = payload["records"]
        if len(records) != EXPECTED_COUNTS[version]:
            raise SystemExit(f"v{version} record-count drift")
        invalid = [i for i, record in enumerate(records) if set(record) != EXPECTED_FIELDS]
        if invalid:
            raise SystemExit(f"v{version} per-record field drift at rows: {invalid}")
        pairs = {pair(record) for record in records}
        normalized_post_ids = {record["post_id"].lower() for record in records}
        if len(pairs) != len(records):
            raise SystemExit(f"v{version} duplicate subreddit/post-ID pair")
        if len(normalized_post_ids) != len(records):
            raise SystemExit(f"v{version} duplicate normalized post ID")
        data[version] = records
        sets[version] = pairs

    if not sets["0.3"] < sets["0.4"] or len(sets["0.4"] - sets["0.3"]) != 9:
        raise SystemExit("v0.3 to v0.4 lineage drift")
    if not sets["0.4"] < sets["0.5"] or len(sets["0.5"] - sets["0.4"]) != 9:
        raise SystemExit("v0.4 to v0.5 lineage drift")

    added_06 = sorted(post_id for subreddit, post_id in sets["0.6"] - sets["0.5"])
    removed_06 = sorted(post_id for subreddit, post_id in sets["0.5"] - sets["0.6"])
    if added_06 != EXPECTED_ADDED_06 or removed_06 != EXPECTED_REMOVED_06:
        raise SystemExit("v0.5 to v0.6 replacement lineage drift")

    observed_fields = {key for records in data.values() for record in records for key in record}
    document_fields = {key for version in VERSIONS for key in json.loads(
        (COMMUNITY / f"reddit-corroboration-seed-v{version}.json").read_text(encoding="utf-8")
    )}
    topic_fields = sorted(TOPIC_FIELDS.intersection(observed_fields | document_fields))
    if topic_fields:
        raise SystemExit(f"unexpected topic-bearing fields: {topic_fields}")

    result = {
        "version": "0.7.15",
        "status": "REDDIT_CORROBORATION_TOPIC_AUDITED",
        "audited_public_top_level_topic_count": 73,
        "new_top_level_topics": [],
        "promotion_state": "NO_COUNT_CHANGE",
        "series": {
            "record_counts": EXPECTED_COUNTS,
            "record_fields": sorted(observed_fields),
            "explicit_topic_category_or_flair_fields": topic_fields,
            "transitions": {
                "v0.3_to_v0.4": {"added": 9, "removed": 0, "cumulative": True},
                "v0.4_to_v0.5": {"added": 9, "removed": 0, "cumulative": True},
                "v0.5_to_v0.6": {
                    "added": 5, "removed": 4, "cumulative": False,
                    "added_post_ids": added_06, "removed_post_ids": removed_06,
                },
            },
        },
        "decision": "Corroboration seeds contain public-presence identifiers only. They contain no explicit topic, category, or Reddit flair evidence.",
        "guardrails": {
            "post_id_inference": False,
            "subreddit_is_topic": False,
            "presence_is_topic_evidence": False,
            "truth_inference": False,
            "rights_promotion": False,
            "scientific_evidence_promotion": False,
        },
    }
    checkpoint = json.loads((COMMUNITY / "reddit-corroboration-topic-audit-v0.7.15.json").read_text(encoding="utf-8"))
    if result != checkpoint:
        raise SystemExit("generated audit differs from checked-in checkpoint")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
