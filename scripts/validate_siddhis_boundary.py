#!/usr/bin/env python3
"""Temporary fail-closed question-only boundary for the unreviewed Siddhis draft.

No governed references or reviewed connections exist for this page. Freeze the
question-only surface until a separate reviewed change supplies those contracts.
Do not refresh the digest merely to admit an evidence label or a new association.
This is a content hold, not evidence approval or a general provenance validator.
"""
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "website/app/topics/siddhis/page.tsx"
QUESTION_ONLY_SHA256 = "d5f35acc1b8456c5405fb220e1003abb3679e8502740b544a49c6a96af2da909"


def validate(text: str) -> None:
    if hashlib.sha256(text.encode("utf-8")).hexdigest() != QUESTION_ONLY_SHA256:
        raise ValueError(
            "Siddhis question-only hold changed: no new associations or evidence "
            "claims without governed references, claim mappings and review."
        )


def main() -> int:
    try:
        validate(PAGE.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        print(f"SIDDHIS BOUNDARY FAIL: {exc}")
        return 1
    print("SIDDHIS BOUNDARY PASS: UNRESOLVED; Reddit HOLD; all gates CLOSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
