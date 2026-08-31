#!/usr/bin/env python3
"""Fail-closed selector for the latest semantic-versioned WikiSpine aggregate/validator."""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMMUNITY = ROOT / "references" / "community"
SCRIPTS = ROOT / "scripts"
AGGREGATE_RE = re.compile(r"wikispine-entity-aggregate-v(\d+)\.(\d+)\.(\d+)\.json$")


def version_from_aggregate(path: Path) -> tuple[int, int, int]:
    match = AGGREGATE_RE.fullmatch(path.name)
    if not match:
        raise ValueError(f"invalid WikiSpine aggregate filename: {path.name}")
    return tuple(map(int, match.groups()))


def latest_aggregate(directory: Path = COMMUNITY) -> Path:
    candidates = [path for path in directory.glob("wikispine-entity-aggregate-v*.json") if AGGREGATE_RE.fullmatch(path.name)]
    if not candidates:
        raise ValueError("no WikiSpine aggregate found")
    return max(candidates, key=version_from_aggregate)


def validator_name(version: tuple[int, int, int]) -> str:
    major, minor, patch = version
    if major < 0 or minor < 0 or patch < 0:
        raise ValueError("negative semantic version component")
    return f"validate_wikispine_v{major}{minor}{patch:02d}.py"


def resolve_current(directory: Path = COMMUNITY, scripts_dir: Path = SCRIPTS) -> tuple[Path, Path, tuple[int, int, int]]:
    aggregate = latest_aggregate(directory)
    version = version_from_aggregate(aggregate)
    payload = json.loads(aggregate.read_text(encoding="utf-8"))
    expected_version = ".".join(map(str, version))
    if payload.get("version") != expected_version:
        raise ValueError(
            f"WikiSpine aggregate filename/content version mismatch: {aggregate.name} vs {payload.get('version')!r}"
        )
    validator = scripts_dir / validator_name(version)
    if not validator.is_file():
        raise ValueError(f"latest WikiSpine aggregate lacks matching validator: {validator.name}")
    return aggregate, validator, version


def main() -> int:
    try:
        aggregate, validator, version = resolve_current()
        result = subprocess.run(
            [sys.executable, str(validator)],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"CURRENT WIKISPINE FAIL: {exc}", file=sys.stderr)
        return 1

    if result.returncode != 0:
        detail = (result.stderr or result.stdout).strip()
        print(f"CURRENT WIKISPINE FAIL: {validator.name}: {detail}", file=sys.stderr)
        return 1

    print(
        "CURRENT WIKISPINE PASS",
        {
            "version": ".".join(map(str, version)),
            "aggregate": aggregate.name,
            "validator": validator.name,
        },
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
