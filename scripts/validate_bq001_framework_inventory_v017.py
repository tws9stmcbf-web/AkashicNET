#!/usr/bin/env python3
"""Fail-closed validation for the v0.17 BQ001 framework inventory."""
import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
INVENTORY = ROOT / "references/big-questions/BQ001/framework-inventory-v0.17-slice1.json"
SCHEMA = ROOT / "schemas/bq001-framework-inventory-v0.17-slice1.schema.json"
EXPECTED_PIN = "4867ca7c8c9a4e1bc139f630815ecf49c79a2ef7"
EXPECTED_IDS = {
    "FW-BQ001-UMBRELLA-BIOLOGICAL-DEPENDENCE",
    "FW-BQ001-UMBRELLA-CONTINUITY",
    "FW-BQ001-PHILOSOPHY-PHYSICALISM",
    "FW-BQ001-PHILOSOPHY-DUALISM",
    "FW-BQ001-PHILOSOPHY-PANPSYCHISM",
    "FW-BQ001-CONTEMPLATIVE-BUDDHIST-NONSELF",
    "FW-BQ001-CONTEMPLATIVE-DAHL-PRACTICE-FAMILIES",
    "FW-BQ001-CONTEMPLATIVE-SART",
    "FW-BQ001-NDE-NEUROSCIENTIFIC-MODEL",
    "FW-BQ001-CONSCIOUSNESS-GNWT",
    "FW-BQ001-CONSCIOUSNESS-IIT",
}
FORBIDDEN_KEYS = {
    "driveid", "drivefileid", "driveobjectid", "fileid", "objectid",
    "filename", "filepath", "privatepath", "parentid", "objecthash",
    "objectsha256", "md5checksum", "sha256checksum", "privatedriveid",
}


def canonical(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=False, indent=2, allow_nan=False) + "\n"


def load_json(raw):
    def unique_pairs(pairs):
        out = {}
        for key, value in pairs:
            if key in out:
                raise ValueError("duplicate JSON key")
            out[key] = value
        return out
    def reject_constant(_):
        raise ValueError("non-finite JSON number")
    return json.loads(raw, object_pairs_hook=unique_pairs, parse_constant=reject_constant)


def decode_percent(text):
    decoded = text
    for _ in range(32):
        updated = unquote(decoded)
        if updated == decoded:
            return decoded
        decoded = updated
    raise ValueError("encoding did not stabilize")


def privacy_check(value):
    def check(text, is_key=False):
        decoded = decode_percent(text)
        folded = decoded.casefold().replace("\\", "/")
        if any(marker in folded for marker in (
            "drive.google.com", "docs.google.com", "/my drive/", "akm-",
            "file://", "gdrive://",
        )):
            raise ValueError("private metadata rejected")
        if not is_key and re.search(r"(?<![a-f0-9])[a-f0-9]{64}(?![a-f0-9])", folded):
            raise ValueError("unscoped digest rejected")
    if isinstance(value, dict):
        for key, child in value.items():
            check(key, True)
            normalized_key = re.sub(
                r"[^a-z0-9]", "", decode_percent(key).casefold()
            )
            if normalized_key in FORBIDDEN_KEYS:
                raise ValueError("private metadata rejected")
            if key == "git_blob_sha" and isinstance(child, str) and re.fullmatch(r"[a-f0-9]{40}", child):
                continue
            if key == "inherited_v016_readiness_pin" and child == EXPECTED_PIN:
                continue
            privacy_check(child)
    elif isinstance(value, list):
        for child in value:
            privacy_check(child)
    elif isinstance(value, str):
        check(value)


def git_blob_sha(raw):
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()


def resolve_pointer(document, pointer):
    current = document
    for token in pointer.split("/")[1:]:
        token = token.replace("~1", "/").replace("~0", "~")
        if isinstance(current, list):
            if not re.fullmatch(r"(?:0|[1-9][0-9]*)", token):
                raise ValueError("invalid governed locator")
            current = current[int(token)]
        elif isinstance(current, dict) and token in current:
            current = current[token]
        else:
            raise ValueError("invalid governed locator")
    return current


def collect_strings(value):
    if isinstance(value, dict):
        return {item for child in value.values() for item in collect_strings(child)}
    if isinstance(value, list):
        return {item for child in value for item in collect_strings(child)}
    return {value} if isinstance(value, str) else set()


def validate(data):
    from jsonschema import Draft202012Validator

    privacy_check(data)
    schema = load_json(SCHEMA.read_bytes())
    Draft202012Validator.check_schema(schema)
    errors = sorted(Draft202012Validator(schema).iter_errors(data), key=lambda e: list(e.path))
    if errors:
        raise ValueError("framework inventory schema violation")

    if data["inherited_v016_readiness_pin"] != EXPECTED_PIN:
        raise ValueError("v0.16 pin drift")

    artifacts = data["governed_artifacts"]
    paths = [item["path"] for item in artifacts]
    roles = [item["role"] for item in artifacts]
    if len(set(paths)) != len(paths) or len(set(roles)) != len(roles):
        raise ValueError("duplicate governed artifact or role")

    loaded = {}
    by_name = {}
    for artifact in artifacts:
        path = ROOT / artifact["path"]
        raw = path.read_bytes()
        if git_blob_sha(raw) != artifact["git_blob_sha"]:
            raise ValueError("governed artifact drift")
        document = load_json(raw)
        loaded[artifact["path"]] = document
        if path.name in by_name:
            raise ValueError("ambiguous governed artifact name")
        by_name[path.name] = document

    items = data["inventory"]
    ids = [item["inventory_item_id"] for item in items]
    if set(ids) != EXPECTED_IDS or len(ids) != len(set(ids)):
        raise ValueError("framework inventory identity drift")
    names = [item["canonical_name"] for item in items]
    if len(names) != len(set(names)):
        raise ValueError("duplicate canonical framework name")

    for item in items:
        observed = set()
        for locator in item["pinned_locators"]:
            filename, pointer = locator.split("#", 1)
            if filename not in by_name:
                raise ValueError("locator references ungoverned artifact")
            observed |= collect_strings(resolve_pointer(by_name[filename], pointer))
        if not set(item["represented_by"]).issubset(observed):
            raise ValueError("represented identity is not bound to locator")
        if item["evidence_role"] == "Established Evidence" and item["category"] != "CONSCIOUSNESS_THEORY":
            raise ValueError("empirical label applied outside bounded theory test")
        if item["evidence_role"] == "organising_model_only" and item["category"] != "UMBRELLA_MODEL":
            raise ValueError("organising role applied outside umbrella model")
        if item["category"] == "UMBRELLA_MODEL":
            if item["independence_state"] != "NOT_APPLICABLE_TO_MODEL":
                raise ValueError("model assigned evidence independence")
        elif item["independence_state"] == "NOT_APPLICABLE_TO_MODEL":
            raise ValueError("evidence-bearing item lacks review state")

    indexed = {item["inventory_item_id"]: item for item in items}
    gnwt = indexed["FW-BQ001-CONSCIOUSNESS-GNWT"]
    iit = indexed["FW-BQ001-CONSCIOUSNESS-IIT"]
    shared = set(gnwt["represented_by"]) & set(iit["represented_by"])
    if shared != {"SRC-BQ001-COGITATE-2025", "CLAIM-BQ001-COGITATE-2025-OBS-01"}:
        raise ValueError("shared GNWT/IIT provenance drift")
    if iit["independence_state"] != "SHARED_SOURCE_WITH_GNWT_DO_NOT_DOUBLE_COUNT":
        raise ValueError("shared source double-counting guard missing")

    counts = {
        "governed_artifacts": len(artifacts),
        "inventory_items": len(items),
        "umbrella_models": sum(i["category"] == "UMBRELLA_MODEL" for i in items),
        "philosophical_frameworks": sum(i["category"] == "PHILOSOPHICAL_FRAMEWORK" for i in items),
        "contemplative_frameworks": sum(i["category"] in {
            "CONTEMPLATIVE_PHILOSOPHICAL_FRAMEWORK",
            "PEER_REVIEWED_REVIEW_FRAMEWORK",
            "PEER_REVIEWED_THEORETICAL_FRAMEWORK",
        } for i in items),
        "neuroscientific_explanatory_models": sum(i["category"] == "NEUROSCIENTIFIC_EXPLANATORY_MODEL" for i in items),
        "consciousness_theories": sum(i["category"] == "CONSCIOUSNESS_THEORY" for i in items),
        "resolved_items": sum(i["status"] == "RESOLVED" for i in items),
        "accepted_edges": 0,
    }
    if data["summary"] != counts:
        raise ValueError("framework inventory summary drift")
    if any(data["promotion_guards"].values()):
        raise ValueError("promotion guard enabled")
    boundaries = data["operational_boundaries"]
    if boundaries["reddit_live_access"] != "HOLD" or any(
        boundaries[key] for key in boundaries if key != "reddit_live_access"
    ):
        raise ValueError("operational boundary weakened")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", nargs="?", default=str(INVENTORY))
    args = parser.parse_args()
    try:
        target = Path(args.path)
        data = load_json(target.read_bytes())
        validate(data)
        if target == INVENTORY and target.read_text(encoding="utf-8") != canonical(data):
            raise ValueError("noncanonical serialization")
    except (ValueError, TypeError, KeyError, OSError, IndexError, AttributeError):
        print("BQ001 v0.17 framework inventory FAIL; no synthesis or promotion", file=sys.stderr)
        return 1
    print("BQ001 v0.17 framework inventory PASS; unresolved; review-only; zero accepted edges")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
