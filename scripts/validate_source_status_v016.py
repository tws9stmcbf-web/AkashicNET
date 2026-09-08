#!/usr/bin/env python3
"""Deterministic validator for the bounded v0.16 source-status review fixture."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = sorted((ROOT / "references").glob("source-status-fixture-v0.16*.json"))
SCHEMA = ROOT / "schemas/source-status-v0.16.schema.json"
ALL_STATUSES = {
    "AVAILABLE", "REDIRECTED", "TITLE_CHANGED", "UNAVAILABLE_INDETERMINATE",
    "CORRECTED", "RETRACTED", "DELETED", "DUPLICATE_REFERENCE_CANDIDATE",
    "PROVENANCE_INCOMPLETE",
}
SHA40 = re.compile(r"^[0-9a-f]{40}$")


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


def validate(data: dict) -> None:
    if not SCHEMA.is_file():
        fail("schema missing")
    if data.get("schema_version") != "0.16.0-beta.1":
        fail("unexpected schema version")
    if data.get("artifact_status") != "REVIEW_FIXTURE_ONLY":
        fail("fixture must remain review-only")
    if data.get("issue") != 282:
        fail("fixture must bind to issue 282")

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
        observation = event["evidence"]["observation"].lower()
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
    if "RETRACTED" not in gaps:
        fail("fixture must not imply verified retraction coverage")


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
