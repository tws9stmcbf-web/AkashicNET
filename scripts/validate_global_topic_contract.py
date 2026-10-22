"""Schema and claim-to-source integrity checks; no evidence promotion performed."""
import json
from pathlib import Path
from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = json.loads((ROOT / "schemas/global_topic_v01.schema.json").read_text())
VALIDATOR = Draft202012Validator(SCHEMA, format_checker=FormatChecker())


def validate_topic(topic):
    VALIDATOR.validate(topic)
    sources = {source["id"]: source for source in topic["sources"]}
    if len(sources) != len(topic["sources"]):
        raise ValueError("Duplicate source identity")
    for claim in topic["connections"] + topic.get("solution_space", {}).get("candidates", []):
        refs = claim["source_ids"]
        if not set(refs) <= sources.keys():
            raise ValueError("Unregistered claim-level source")
        if claim.get("evidence_status") in ("supported", "mixed"):
            if not any(sources[id]["evidence_role"] in ("claim", "replication")
                       and sources[id]["source_type"] in ("primary-source", "institutional-record")
                       for id in refs):
                raise ValueError("Rating requires claim-level evidence, not context or testimony")


def validate_seed(seed):
    if seed["controlled_values"]["ultimate_status"] != SCHEMA["properties"]["origin"]["properties"]["ultimate_status"]["enum"]:
        raise ValueError("Origin vocabulary drift")
    for field in ("id", "slug"):
        values = [topic[field] for topic in seed["topics"]]
        if len(values) != len(set(values)):
            raise ValueError(f"Duplicate topic {field}")
    for topic in seed["topics"]:
        validate_topic(topic)


if __name__ == "__main__":
    validate_seed(json.loads((ROOT / "data/global_metadata_discovery_v01.seed.json").read_text()))
    print("Global topic schema and claim provenance: PASS")
