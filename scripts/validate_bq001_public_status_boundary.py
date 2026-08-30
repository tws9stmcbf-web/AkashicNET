#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "website" / "app" / "big-questions" / "bq001" / "page.tsx"

REQUIRED = (
    "BIG QUESTION 001 · PUBLIC INVESTIGATION",
    "CURRENT STATUS · UNRESOLVED",
    "Established Evidence · Interpretation · Lived Experience/Testimony · Hypothesis · Speculation",
    ">Biological dependence<",
    ">Continuity<",
    "AkashicNET PRE-ALPHA v0.10.x engine",
)

FORBIDDEN = (
    "PUBLIC BETA INVESTIGATION",
    "CURRENT STATUS · RESOLVED",
    "CURRENT CONCLUSION · RESOLVED",
)


def validate(text: str) -> bool:
    for phrase in REQUIRED:
        assert phrase in text, f"missing BQ001 public boundary: {phrase}"
    for phrase in FORBIDDEN:
        assert phrase not in text, f"forbidden BQ001 public status phrase: {phrase}"
    assert text.count("UNRESOLVED") >= 4, "BQ001 unresolved state must remain visible across status/model/conclusion surfaces"
    return True


def main() -> int:
    text = PAGE.read_text(encoding="utf-8")
    validate(text)
    print("AKASHICNET BQ001 PUBLIC STATUS BOUNDARY PASS", {
        "public_label": "PUBLIC INVESTIGATION",
        "project_status": "PRE-ALPHA v0.10.x",
        "question_status": "UNRESOLVED",
    })
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
