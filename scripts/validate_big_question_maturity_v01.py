#!/usr/bin/env python3
import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LADDER = ROOT / "references/big-questions/research-maturity-ladder-v0.1.json"
ASSESSMENTS = ROOT / "references/big-questions/maturity-assessments-v0.1.json"
MANAGED_FILES = (
    ROOT / "website/app/big-questions/page.tsx",
    ROOT / "website/app/big-questions/bq001/page.tsx",
    ROOT / "website/app/big-questions/bq002/page.tsx",
    ROOT / "references/big-questions/BQ003/progress-assessment-v0.1.json",
)
ASSERTION = re.compile(r"\b(BQ\d{3})\b[^\n]{0,160}?\bLevel\s+(\d{1,2})/10\b", re.IGNORECASE)


def fail(message):
    raise ValueError(message)


def _assertions(text):
    return [(question.upper(), int(level)) for question, level in ASSERTION.findall(text)]


def validate(ladder, registry, managed_texts=(), pr_body=""):
    stages = ladder.get("stages", [])
    levels = [stage.get("level") for stage in stages]
    if ladder.get("status") != "CANONICAL" or levels != list(range(1, 11)):
        fail("canonical maturity ladder must contain ordered Levels 1 through 10")
    if len({stage.get("id") for stage in stages}) != 10:
        fail("canonical maturity stage ids must be unique")
    rules = ladder.get("fail_closed_rules", {})
    for key in (
        "levels_are_cumulative",
        "asserted_level_must_equal_highest_completed_stage",
        "missing_or_unvalidated_stage_blocks_higher_assertions",
        "level_8_requires_governed_test_execution",
        "unresolved_is_allowed_at_every_level",
    ):
        if rules.get(key) is not True:
            fail(f"canonical fail-closed rule weakened: {key}")

    expected_ref = "references/big-questions/research-maturity-ladder-v0.1.json"
    if registry.get("ladder_ref") != expected_ref:
        fail("assessment registry must reference the canonical ladder")
    assessments = registry.get("assessments", [])
    by_id = {item.get("question_id"): item for item in assessments}
    if set(by_id) != {f"BQ{number:03d}" for number in range(1, 10)} or len(by_id) != len(assessments):
        fail("assessment registry must contain exactly BQ001 through BQ009")
    for question_id, item in by_id.items():
        if item.get("question_status") != "UNRESOLVED":
            fail(f"{question_id} must remain unresolved")
        completed = item.get("completed_stages", [])
        level = item.get("asserted_level")
        if level is None:
            if completed:
                fail(f"{question_id} unscored assessment cannot claim completed stages")
            continue
        if not isinstance(level, int) or not 1 <= level <= 10:
            fail(f"{question_id} asserted level invalid")
        if completed != list(range(1, level + 1)):
            fail(f"{question_id} assertion exceeds its highest consecutive completed stage")
        if level >= 8 and 8 not in completed:
            fail(f"{question_id} Level 8 requires governed test execution")

    governance = registry.get("governance", {})
    if governance.get("supports_models") != [] or governance.get("accepted_canonical_edges") != 0:
        fail("model support or canonical edges promoted")
    for key in (
        "truth_inference_allowed",
        "scientific_evidence_promotion_allowed",
        "rights_promotion_allowed",
        "public_synthesis_updated",
        "website_promotion_allowed",
    ):
        if governance.get(key) is not False:
            fail(f"governance gate opened: {key}")

    for source, text in managed_texts:
        for question_id, asserted in _assertions(text):
            governed = by_id.get(question_id)
            if governed is None or governed.get("asserted_level") != asserted:
                fail(f"{source}: {question_id} Level {asserted}/10 exceeds or conflicts with governed assessment")
    for question_id, asserted in _assertions(pr_body):
        governed = by_id.get(question_id)
        if governed is None or governed.get("asserted_level") != asserted:
            fail(f"pull-request body: {question_id} Level {asserted}/10 exceeds or conflicts with governed assessment")


def main():
    ladder = json.loads(LADDER.read_text())
    registry = json.loads(ASSESSMENTS.read_text())
    managed = [(str(path.relative_to(ROOT)), path.read_text()) for path in MANAGED_FILES]
    pr_body = ""
    event_path = os.environ.get("GITHUB_EVENT_PATH")
    if event_path:
        event = json.loads(Path(event_path).read_text())
        pr_body = event.get("pull_request", {}).get("body") or ""
    validate(ladder, registry, managed, pr_body)
    print("Big Question maturity ladder and assessments valid")


if __name__ == "__main__":
    try:
        main()
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
