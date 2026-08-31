#!/usr/bin/env python3
"""Fail closed if README Public Beta status drifts from governed repository state."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
COMMUNITY = ROOT / "references" / "community"
AGGREGATE_RE = re.compile(r"wikispine-entity-aggregate-v(\d+)\.(\d+)\.(\d+)\.json$")


def latest_wikispine_aggregate(directory: Path = COMMUNITY) -> Path:
    candidates: list[tuple[tuple[int, int, int], Path]] = []
    for path in directory.glob("wikispine-entity-aggregate-v*.json"):
        match = AGGREGATE_RE.fullmatch(path.name)
        if match:
            candidates.append((tuple(map(int, match.groups())), path))
    if not candidates:
        raise ValueError("no WikiSpine aggregate found")
    return max(candidates, key=lambda item: item[0])[1]


def expected_wikispine_tokens(aggregate: dict) -> tuple[str, str]:
    total = aggregate["resolved_high_precision"]
    by_type = aggregate["resolved_by_type"]
    person = by_type["PERSON"]
    work = by_type["WORK"]
    pending = aggregate["pending_resolution"]
    assert person + work == total
    assert pending == len(aggregate["pending_entities"])
    identity_word = "identity" if pending == 1 else "identities"
    snapshot = f"WikiSpine: **{total} resolved (PERSON {person} · WORK {work}) · {pending} WORK pending**"
    milestone = (
        f"**WikiSpine:** {total} resolved high-precision typed reference identities "
        f"(PERSON {person}, WORK {work}); {pending} WORK {identity_word} pending"
    )
    return snapshot, milestone


def validate(readme_text: str, aggregate: dict) -> list[str]:
    required = {
        "current phase": "PUBLIC BETA",
        "sealed release": "PRE-ALPHA v0.10",
        "sealed tag": "v0.10.0-prealpha",
        "truth gate": "Truth inference: OFF",
        "rights gate": "Rights promotion: OFF",
        "scientific gate": "Scientific-evidence promotion: OFF",
    }
    missing = [label for label, token in required.items() if token not in readme_text]

    for forbidden in (
        "Truth inference: ON",
        "Rights promotion: ON",
        "Scientific-evidence promotion: ON",
    ):
        if forbidden in readme_text:
            missing.append(f"forbidden status: {forbidden}")

    snapshot, milestone = expected_wikispine_tokens(aggregate)
    if snapshot not in readme_text:
        missing.append(f"WikiSpine publication snapshot mismatch: expected {snapshot}")
    if milestone not in readme_text:
        missing.append(f"WikiSpine milestone snapshot mismatch: expected {milestone}")
    return missing


def main() -> int:
    try:
        aggregate_path = latest_wikispine_aggregate()
        aggregate = json.loads(aggregate_path.read_text(encoding="utf-8"))
        missing = validate(README.read_text(encoding="utf-8"), aggregate)
    except (OSError, json.JSONDecodeError, KeyError, AssertionError, ValueError) as exc:
        print(f"Public Beta status validation FAILED: {exc}")
        return 1

    if missing:
        print("Public Beta status validation FAILED:")
        for item in missing:
            print(f"- {item}")
        return 1

    print(
        "Public Beta status validation passed: current phase and sealed release remain distinct; "
        "promotion gates remain OFF; README WikiSpine snapshot matches "
        f"{aggregate_path.name}."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
