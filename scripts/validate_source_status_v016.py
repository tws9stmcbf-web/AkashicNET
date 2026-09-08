#!/usr/bin/env python3
"""Deterministic validator for the bounded v0.16 source-status review fixture."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = sorted((ROOT / "references").glob("source-status-fixture-v0.16*.json"))
SCHEMA = ROOT / "schemas/source-status-v0.16.schema.json"
ALL_STATUSES = {
    "AVAILABLE", "REDIRECTED", "TITLE_CHANGED", "UNAVAILABLE_INDETERMINATE",
    "CORRECTED", "RETRACTED", "DELETED", "DUPLICATE_REFERENCE_CANDIDATE",
    "PROVENANCE_INCOMPLETE",
}
SHA40 = re.compile(r"^[0-9a-f]{40}$")
TERMINAL_STATUSES = {"TITLE_CHANGED", "RETRACTED", "DELETED"}
NEGATED_TERMINAL_MARKERS = {
    "TITLE_CHANGED": (
        "no title-change",
        "title did not change",
        "title was not changed",
        "title-change was not observed",
    ),
    "RETRACTED": (
        "no retraction",
        "not retracted",
        "was not retracted",
        "has not been retracted",
        "retraction was not observed",
    ),
    "DELETED": (
        "no deletion",
        "not deleted",
        "was not deleted",
        "has not been deleted",
        "deletion was not observed",
    ),
}
NEGATION_CONTRACTIONS = {
    "wasn't": "was not",
    "wasn’t": "was not",
    "isn't": "is not",
    "isn’t": "is not",
    "hasn't": "has not",
    "hasn’t": "has not",
    "didn't": "did not",
    "didn’t": "did not",
}


def fail(message: str) -> None:
    raise AssertionError(message)


def git_blob_sha(path: str) -> str:
    result = subprocess.run(
        ["git", "rev-parse", f"HEAD:{path}"],
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
    )
    return result.stdout.strip()


def iter_url_fields(value, path=""):
    if isinstance(value, dict):
        for key, child in value.items():
            child_path = f"{path}.{key}" if path else key
            if key.endswith("_url"):
                yield child_path, child
            yield from iter_url_fields(child, child_path)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from iter_url_fields(child, f"{path}[{index}]")


def require_reserved_url(value, field: str) -> None:
    try:
        parsed = urlparse(value)
        hostname = parsed.hostname
    except (AttributeError, TypeError, ValueError):
        fail(f"synthetic URL is invalid: {field}")
    if (
        parsed.scheme != "https"
        or hostname is None
        or not hostname.endswith(".invalid")
        or parsed.username is not None
        or parsed.password is not None
    ):
        fail(f"synthetic URL must use a reserved hostname: {field}")


def normalize_negation(text: str) -> str:
    normalized = text.lower()
    for contraction, expansion in NEGATION_CONTRACTIONS.items():
        normalized = normalized.replace(contraction, expansion)
    return re.sub(r"\b([a-z]+)n['’]t\b", r"\1 not", normalized)


def terminal_evidence_is_negated(status: str, observation: str) -> bool:
    concept_patterns = {
        "TITLE_CHANGED": r"title(?:[- ]chang(?:e|ed|ing))",
        "RETRACTED": r"retract(?:ion|ed|ing)",
        "DELETED": r"delet(?:ion|ed|ing)",
    }
    without_denial = (
        r"without(?:[\s,]+(?:any|sufficient|independent|direct|documented|published|supporting|corroborating)){0,2}[\s,]+"
        r"(?:confirmation|verification|evidence|observation)\b"
        r"|without(?:[\s,]+(?:independently|directly|actually)){0,2}[\s,]+"
        r"(?:confirming|verifying|observing)\b"
        r"|without(?:[\s,]+(?:independently|directly|actually)){0,2}[\s,]+"
        r"(?:finding|detecting|locating|discovering)(?:[\s,]+[a-z-]+){0,3}[\s,]+"
        r"(?:confirmation|verification|evidence|observation)\b"
    )
    negation = rf"(?:no|not|never|failed to|failure to|{without_denial})"
    concept = concept_patterns[status]
    # A coordinating comma starts a separate clause only when a bounded
    # finite predicate follows. Modifier phrases such as "for the moment"
    # and "so far" therefore remain in the status predicate.
    coordinated_clause = (
        r"(?:but|yet|and|or|nor|so|for)(?=\s+"
        r"(?:[^\s,;:.]+\s+){0,3}"
        r"(?:is|are|was|were|has|have|had|does|do|did|will|would|can|could|"
        r"may|might|must|shall|should|occurred|changed|retracted|deleted|"
        r"remains?|became|becomes?|confirms?|states?|reports?|records?|says|"
        r"indicates?|shows?|notes?|documents?|affirms?|finds?|observes?|verifies?)\b)"
    )
    separator = rf"(?:\s+|,(?!\s*{coordinated_clause})\s*)+"
    negation_before_concept = rf"(?:{negation})(?:{separator}\w+){{0,5}}{separator}(?:{concept})"
    # Only 'without' clauses whose complement denotes missing evidence negate
    # a status. Provenance and no-promotion consequences remain affirmative.
    concept_before_negation = rf"(?:{concept})(?:{separator}\w+){{0,6}}{separator}{negation}\b"
    return bool(
        re.search(negation_before_concept, observation)
        or re.search(concept_before_negation, observation)
        or (status == "TITLE_CHANGED" and re.search(
            rf"\btitle(?:['’]s)?(?:{separator}\w+){{0,6}}{separator}(?:no|not|never|failed to|failure to)(?:{separator}\w+){{0,5}}{separator}chang(?:e|ed|ing)\b",
            observation,
        ))
        or any(marker in observation for marker in NEGATED_TERMINAL_MARKERS[status])
    )


def validate(data: dict) -> None:
    if not SCHEMA.is_file():
        fail("schema missing")
    if data.get("schema_version") != "0.16.0-beta.1":
        fail("unexpected schema version")
    if data.get("artifact_status") != "REVIEW_FIXTURE_ONLY":
        fail("fixture must remain review-only")
    if data.get("issue") != 282:
        fail("fixture must bind to issue 282")

    fixture_kind = data.get("fixture_kind")
    if fixture_kind not in {"OBSERVED_REPOSITORY_EVIDENCE", "SYNTHETIC_VALIDATOR_SCENARIO"}:
        fail("fixture kind must be explicit")
    synthetic = fixture_kind == "SYNTHETIC_VALIDATOR_SCENARIO"
    if synthetic and "not real observations" not in data.get("synthetic_disclaimer", "").lower():
        fail("synthetic fixture lacks non-observational disclaimer")
    if not synthetic and "synthetic_disclaimer" in data:
        fail("observed fixture cannot carry a synthetic disclaimer")
    if synthetic:
        for field, value in iter_url_fields(data):
            require_reserved_url(value, field)

    nodes = data.get("source_nodes", [])
    events = data.get("events", [])
    if not 3 <= len(events) <= 5:
        fail("fixture must contain 3-5 events")

    node_map = {}
    for node in nodes:
        node_id = node["source_node_id"]
        if node_id in node_map:
            fail(f"duplicate source node: {node_id}")
        if not SHA40.fullmatch(node["input_blob_sha"]):
            fail(f"invalid input blob SHA: {node_id}")
        if synthetic:
            if not node_id.startswith("SYNTHETIC-"):
                fail(f"synthetic node ID is not isolated: {node_id}")
        if git_blob_sha(node["input_path"]) != node["input_blob_sha"]:
            fail(f"input digest drift: {node_id}")
        node_map[node_id] = node

    event_ids = set()
    observed_statuses = set()
    for event in events:
        event_id = event["event_id"]
        if event_id in event_ids:
            fail(f"duplicate event: {event_id}")
        event_ids.add(event_id)

        status = event["status"]
        if status not in ALL_STATUSES:
            fail(f"unknown status: {status}")
        observed_statuses.add(status)

        node = node_map.get(event["source_node_id"])
        if node is None:
            fail(f"unbound source node: {event_id}")
        if event["original_url"] != node["original_url"]:
            fail(f"original URL changed: {event_id}")
        if event["input_blob_sha"] != node["input_blob_sha"]:
            fail(f"locator digest mismatch: {event_id}")
        if event["human_review_state"] not in {"PENDING", "REVIEWED_NO_PROMOTION"}:
            fail(f"invalid review state: {event_id}")
        if synthetic and event["human_review_state"] != "PENDING":
            fail(f"synthetic event cannot be marked reviewed: {event_id}")
        if event["truth_inference"] != "NONE" or event["promotion_applied"] is not False:
            fail(f"automatic inference or promotion: {event_id}")

        transition = event.get("transition")
        if status == "REDIRECTED":
            if not transition:
                fail(f"redirect lacks transition: {event_id}")
            if transition["from_url"] != event["original_url"]:
                fail(f"redirect origin mismatch: {event_id}")
            if transition["replacement_applied"] is not False:
                fail(f"redirect replaced original URL: {event_id}")
            if transition["to_url"] == transition["from_url"]:
                fail(f"redirect target is unchanged: {event_id}")
        elif transition is not None:
            fail(f"non-redirect event has transition: {event_id}")

        if status in {"CORRECTED", "RETRACTED"}:
            if not event["evidence"].get("notice_url"):
                fail(f"notice status lacks notice URL: {event_id}")
        observation = normalize_negation(event["evidence"]["observation"])
        if synthetic and status in TERMINAL_STATUSES:
            if event["evidence"].get("observed_status") != status:
                fail(f"synthetic terminal status lacks affirmative structured evidence: {event_id}")
            if terminal_evidence_is_negated(status, observation):
                fail(f"synthetic terminal status evidence is negated: {event_id}")
        if status == "RETRACTED":
            affirmative_markers = ("retraction notice", "has been retracted", "was retracted")
            if not any(marker in observation for marker in affirmative_markers):
                fail(f"retraction evidence is not explicit: {event_id}")
        if status == "DUPLICATE_REFERENCE_CANDIDATE":
            candidate_guards = ("not an automatic merge", "no record is deleted or silently merged")
            if not any(marker in observation for marker in candidate_guards):
                fail(f"duplicate candidate lacks non-merge boundary: {event_id}")
        if status == "PROVENANCE_INCOMPLETE" and "unconfirmed" not in observation:
            fail(f"incomplete provenance is not explicit: {event_id}")
        if status == "TITLE_CHANGED" and "title-change" not in observation:
            fail(f"title-change evidence is not explicit: {event_id}")
        if status == "DELETED" and "delet" not in observation:
            fail(f"deletion evidence is not explicit: {event_id}")

    guards = data.get("promotion_guards", {})
    expected_guards = {"truth", "evidence", "rights", "identity", "edge_acceptance"}
    if set(guards) != expected_guards or any(value is not False for value in guards.values()):
        fail("all promotion guards must be present and false")

    coverage = data.get("coverage", {})
    implemented = set(coverage.get("implemented_statuses", []))
    gaps = set(coverage.get("verified_gaps", []))
    if implemented != observed_statuses:
        fail("implemented_statuses must exactly match fixture events")
    if implemented & gaps:
        fail("a status cannot be implemented and a verified gap")
    if implemented | gaps != ALL_STATUSES:
        fail("coverage must account for every contract status")
    if not synthetic and "RETRACTED" not in gaps:
        fail("observed fixture must not imply verified retraction coverage")
    if synthetic and observed_statuses != {"TITLE_CHANGED", "RETRACTED", "DELETED"}:
        fail("synthetic fixture scope must remain terminal-status validator coverage")


def main() -> int:
    try:
        if not FIXTURES:
            fail("no source-status fixtures found")
        for fixture in FIXTURES:
            validate(json.loads(fixture.read_text(encoding="utf-8")))
    except (AssertionError, KeyError, json.JSONDecodeError, subprocess.CalledProcessError) as exc:
        print(f"source-status-v0.16: FAIL: {exc}", file=sys.stderr)
        return 1
    print(f"source-status-v0.16: PASS ({len(FIXTURES)} review-only fixtures; no promotions)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
