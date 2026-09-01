#!/usr/bin/env python3
"""Fail closed if any external GitHub Action uses a mutable ref.

Local actions (./...) are allowed. External actions must be pinned to an exact
40-character hexadecimal commit SHA. Readable version comments may follow.
"""

from pathlib import Path
import re
import sys

WORKFLOWS = Path(".github/workflows")
USES_RE = re.compile(r"^\s*(?:-\s*)?uses:\s*([^\s#]+)")
SHA40_RE = re.compile(r"^[0-9a-fA-F]{40}$")


def audit() -> list[str]:
    failures: list[str] = []
    files = sorted([*WORKFLOWS.glob("*.yml"), *WORKFLOWS.glob("*.yaml")])
    if not files:
        return ["no workflow files found under .github/workflows"]

    for path in files:
        for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            match = USES_RE.match(line)
            if not match:
                continue
            target = match.group(1).strip('"\'')
            if target.startswith("./"):
                continue
            if "@" not in target:
                failures.append(f"{path}:{lineno}: external action has no ref: {target}")
                continue
            action, ref = target.rsplit("@", 1)
            if not action or not SHA40_RE.fullmatch(ref):
                failures.append(
                    f"{path}:{lineno}: mutable or non-commit action ref: {target}"
                )

    return failures


def main() -> int:
    failures = audit()
    if failures:
        print("IMMUTABLE ACTIONS AUDIT: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("IMMUTABLE ACTIONS AUDIT: PASS")
    print("All external uses: references are pinned to exact 40-character commit SHAs.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
