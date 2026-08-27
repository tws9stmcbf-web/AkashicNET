#!/usr/bin/env python3
"""Validate the canonical AkashicNET framework registry without dependencies."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path
from typing import Any

DEFAULT_REGISTRY = Path(__file__).resolve().parents[2] / "data" / "framework-registry.json"
ENTITY_TYPES = {"framework", "model", "methodology", "protocol", "meta-framework"}
CONFIDENCE_LEVELS = {"strong", "moderate", "emerging", "speculative"}
SOURCE_TYPES = {
    "reddit_archive",
    "google_drive_metadata",
    "research_evidence_layer",
    "manual_akashicnet_record",
    "other",
}
RELATIONSHIP_TYPES = {
    "derived_from", "supersedes", "superseded_by", "fork_of", "merged_from",
    "inspired_by", "overlaps_with", "supports", "contradicts", "depends_on", "part_of",
}
ID_PATTERN = re.compile(r"^[a-z][a-z0-9]*(?:-[a-z0-9]+)*$")
FRAMEWORK_FIELDS = {
    "framework_id", "name", "short_name", "entity_type", "family", "description",
    "status", "maturity", "first_seen_date", "latest_version", "versions", "aliases",
    "domains", "tags", "source_refs", "evidence_confidence", "claims", "notes",
}


def _duplicates(values: list[str]) -> set[str]:
    seen: set[str] = set()
    return {value for value in values if value in seen or seen.add(value)}


def _valid_date(value: Any) -> bool:
    if value is None:
        return True
    try:
        return date.fromisoformat(value).isoformat() == value
    except (TypeError, ValueError):
        return False


def validate_registry(payload: dict[str, Any]) -> list[str]:
    """Return all validation errors instead of stopping at the first problem."""
    errors: list[str] = []
    frameworks = payload.get("frameworks", [])
    relationships = payload.get("relationships", [])
    sources = payload.get("source_records", [])
    if not all(isinstance(items, list) for items in (frameworks, relationships, sources)):
        return ["frameworks, relationships and source_records must be arrays"]

    source_ids = [item.get("source_id") for item in sources if isinstance(item, dict)]
    framework_ids = [item.get("framework_id") for item in frameworks if isinstance(item, dict)]
    relationship_ids = [item.get("relationship_id") for item in relationships if isinstance(item, dict)]
    for label, values in (("source_id", source_ids), ("framework_id", framework_ids), ("relationship_id", relationship_ids)):
        for duplicate in sorted(_duplicates(values)):
            errors.append(f"duplicate {label}: {duplicate}")
    known_sources, known_frameworks = set(source_ids), set(framework_ids)

    for source in sources:
        sid = source.get("source_id", "<missing>")
        if not ID_PATTERN.fullmatch(str(sid)):
            errors.append(f"source {sid}: invalid stable ID")
        if source.get("source_type") not in SOURCE_TYPES:
            errors.append(f"source {sid}: invalid source_type")
        if not source.get("locator"):
            errors.append(f"source {sid}: locator is required")

    searchable_names: list[tuple[str, str]] = []
    for framework in frameworks:
        fid = framework.get("framework_id", "<missing>")
        missing = FRAMEWORK_FIELDS - framework.keys()
        if missing:
            errors.append(f"framework {fid}: missing fields: {', '.join(sorted(missing))}")
        if not ID_PATTERN.fullmatch(str(fid)):
            errors.append(f"framework {fid}: invalid stable ID")
        if framework.get("entity_type") not in ENTITY_TYPES:
            errors.append(f"framework {fid}: invalid entity_type")
        if framework.get("evidence_confidence") not in CONFIDENCE_LEVELS:
            errors.append(f"framework {fid}: invalid evidence_confidence")
        if not _valid_date(framework.get("first_seen_date")):
            errors.append(f"framework {fid}: invalid first_seen_date")
        for field in ("aliases", "domains", "tags", "source_refs", "versions", "claims"):
            if not isinstance(framework.get(field), list):
                errors.append(f"framework {fid}: {field} must be an array")
        searchable_names.extend((str(value).casefold(), fid) for value in [framework.get("name"), framework.get("short_name"), *framework.get("aliases", [])] if value)
        for ref in framework.get("source_refs", []):
            if ref not in known_sources:
                errors.append(f"framework {fid}: unknown source_ref {ref}")
        versions = framework.get("versions", [])
        version_names = [version.get("version") for version in versions]
        for duplicate in sorted(_duplicates(version_names)):
            errors.append(f"framework {fid}: duplicate version {duplicate}")
        if framework.get("latest_version") is not None and framework.get("latest_version") not in version_names:
            errors.append(f"framework {fid}: latest_version is not represented in versions")
        for version in versions:
            if not _valid_date(version.get("date")):
                errors.append(f"framework {fid} version {version.get('version')}: invalid date")
            for ref in version.get("source_refs", []):
                if ref not in known_sources:
                    errors.append(f"framework {fid} version {version.get('version')}: unknown source_ref {ref}")
        for claim in framework.get("claims", []):
            if claim.get("evidence_confidence") not in CONFIDENCE_LEVELS:
                errors.append(f"framework {fid} claim {claim.get('claim_id')}: invalid evidence_confidence")
            for ref in claim.get("source_refs", []):
                if ref not in known_sources:
                    errors.append(f"framework {fid} claim {claim.get('claim_id')}: unknown source_ref {ref}")

    for name in sorted({name for name, _ in searchable_names}):
        owners = sorted({fid for candidate, fid in searchable_names if candidate == name})
        if len(owners) > 1:
            errors.append(f"duplicate canonical name/short name/alias {name!r}: {', '.join(owners)}")

    for relationship in relationships:
        rid = relationship.get("relationship_id", "<missing>")
        if not ID_PATTERN.fullmatch(str(rid)):
            errors.append(f"relationship {rid}: invalid stable ID")
        if relationship.get("relationship_type") not in RELATIONSHIP_TYPES:
            errors.append(f"relationship {rid}: invalid relationship_type")
        for endpoint in ("source_framework_id", "target_framework_id"):
            if relationship.get(endpoint) not in known_frameworks:
                errors.append(f"relationship {rid}: unknown {endpoint} {relationship.get(endpoint)}")
        if relationship.get("source_framework_id") == relationship.get("target_framework_id"):
            errors.append(f"relationship {rid}: self-reference is not allowed")
        if relationship.get("evidence_confidence") not in CONFIDENCE_LEVELS:
            errors.append(f"relationship {rid}: invalid evidence_confidence")
        if not relationship.get("source_refs"):
            errors.append(f"relationship {rid}: at least one source_ref is required")
        for ref in relationship.get("source_refs", []):
            if ref not in known_sources:
                errors.append(f"relationship {rid}: unknown source_ref {ref}")

    if payload.get("generated_count") != len(frameworks):
        errors.append("generated_count does not match the number of framework records")
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("registry", nargs="?", type=Path, default=DEFAULT_REGISTRY)
    args = parser.parse_args(argv)
    try:
        payload = json.loads(args.registry.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: cannot load registry: {exc}", file=sys.stderr)
        return 2
    errors = validate_registry(payload)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(f"Framework registry valid: {len(payload['frameworks'])} curated seed records")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
