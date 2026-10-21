#!/usr/bin/env python3
"""Preserve the historical v0.16 candidate on an exact descendant checkout.

This is not the original candidate-position check or a new release decision.
The historical validator and manifest remain unchanged.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys

from scripts import validate_v016_release_candidate as historical

ROOT = historical.ROOT
HISTORICAL_BASE_COMMIT = "5fb99152524b57948aa10662a1467944fea706c6"


def git_commit(ref: str) -> str:
    return subprocess.run(
        ["git", "rev-parse", "--verify", f"{ref}^{{commit}}"],
        cwd=ROOT, check=True, text=True, capture_output=True,
    ).stdout.strip()


def validate_repository_binding() -> list[str]:
    """Require exact HEAD and historical-anchor -> current-main -> HEAD ancestry."""
    errors: list[str] = []
    if historical.EXPECTED_BASE_COMMIT != HISTORICAL_BASE_COMMIT:
        errors.append("historical candidate base identity changed")
    expected_head = os.environ.get("CANDIDATE_HEAD_SHA", "").strip()
    if not historical.SHA40.fullmatch(expected_head):
        errors.append("full exact candidate head SHA required")
    try:
        head = git_commit("HEAD")
        current_main = git_commit("origin/main")
        anchor = git_commit(HISTORICAL_BASE_COMMIT)
        if head != expected_head:
            errors.append("exact candidate head checkout")
        for ancestor, descendant, error in (
            (anchor, current_main, "historical base must be an ancestor of current origin/main"),
            (anchor, head, "historical base must be an ancestor of candidate head"),
            (current_main, head, "candidate must contain current origin/main"),
        ):
            result = subprocess.run(
                ["git", "merge-base", "--is-ancestor", ancestor, descendant],
                cwd=ROOT, check=False, text=True, capture_output=True,
            )
            if result.returncode != 0:
                errors.append(error)
    except (subprocess.CalledProcessError, OSError):
        errors.append("candidate repository binding")
    return errors


def main() -> int:
    try:
        errors = validate_repository_binding()
        errors += historical.validate_manifest(
            json.loads(historical.MANIFEST.read_text(encoding="utf-8"))
        )
        if errors:
            raise AssertionError(", ".join(errors))
        print(f"Historical v0.16 base: {HISTORICAL_BASE_COMMIT}", flush=True)
        print(f"Fetched current main: {git_commit('origin/main')}", flush=True)
        print(f"Exact tested head: {git_commit('HEAD')}", flush=True)
        historical.run_dependencies()
    except (AssertionError, json.JSONDecodeError, OSError, subprocess.CalledProcessError) as exc:
        print(f"v0.16-preservation: FAIL: {exc}", file=sys.stderr)
        return 1
    print("PASS: historical v0.16 artifacts preserved on an integrated exact head")
    print("PENDING: independent review and human merge/release decision")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
