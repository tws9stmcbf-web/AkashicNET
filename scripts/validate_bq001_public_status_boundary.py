#!/usr/bin/env python3
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "website" / "app" / "big-questions" / "bq001" / "page.tsx"
SYNTHESIS = ROOT / "references" / "big-questions" / "BQ001" / "public-synthesis-v0.1.json"

REQUIRED = (
    "BIG QUESTION 001 · PUBLIC INVESTIGATION",
    "Established Evidence · Interpretation · Lived Experience/Testimony · Hypothesis · Speculation",
    ">Biological dependence<",
    ">Continuity<",
    "AkashicNET PRE-ALPHA v0.10.x engine",
)

FORBIDDEN = (
    "PUBLIC BETA INVESTIGATION",
)


def synthesis_status_contract(payload: dict) -> tuple[str, str, list[str]]:
    assert payload.get("question_id") == "BQ001", "public synthesis must identify BQ001"
    status = payload.get("status")
    conclusion = payload.get("conclusion") or {}
    conclusion_status = conclusion.get("status")
    models = payload.get("competing_models")
    assert isinstance(status, str) and status, "BQ001 synthesis requires a status"
    assert isinstance(conclusion_status, str) and conclusion_status, "BQ001 synthesis requires conclusion status"
    assert status == conclusion_status, "BQ001 synthesis status and conclusion must agree"
    assert isinstance(models, list) and len(models) == 2, "BQ001 requires exactly two competing models"
    model_statuses = []
    for model in models:
        model_status = model.get("status")
        assert isinstance(model_status, str) and model_status, "each BQ001 model requires status"
        model_statuses.append(model_status)
    return status, conclusion_status, model_statuses


def validate(text: str, synthesis: dict) -> bool:
    for phrase in REQUIRED:
        assert phrase in text, f"missing BQ001 public boundary: {phrase}"
    for phrase in FORBIDDEN:
        assert phrase not in text, f"forbidden BQ001 public status phrase: {phrase}"

    status, conclusion_status, model_statuses = synthesis_status_contract(synthesis)
    assert f"CURRENT STATUS · {status}" in text, "public page status must match canonical BQ001 synthesis"
    assert f"CURRENT CONCLUSION · {conclusion_status}" in text, "public page conclusion must match canonical BQ001 synthesis"

    required_model_counts = Counter(model_statuses)
    for model_status, expected_count in required_model_counts.items():
        actual = text.count(f"<strong>{model_status}</strong>")
        assert actual >= expected_count, (
            f"public page competing-model statuses must match canonical synthesis: "
            f"{model_status} expected {expected_count}, found {actual}"
        )

    visible_statuses = Counter([status, conclusion_status, *model_statuses])
    for value, expected_count in visible_statuses.items():
        assert text.count(value) >= expected_count, (
            f"BQ001 status {value!r} must remain visible across status/model/conclusion surfaces"
        )
    return True


def main() -> int:
    try:
        text = PAGE.read_text(encoding="utf-8")
        synthesis = json.loads(SYNTHESIS.read_text(encoding="utf-8"))
        validate(text, synthesis)
        status, _, model_statuses = synthesis_status_contract(synthesis)
    except (OSError, json.JSONDecodeError, AssertionError) as exc:
        print(f"AKASHICNET BQ001 PUBLIC STATUS BOUNDARY FAIL: {exc}")
        return 1

    print("AKASHICNET BQ001 PUBLIC STATUS BOUNDARY PASS", {
        "public_label": "PUBLIC INVESTIGATION",
        "engine_provenance": "PRE-ALPHA v0.10.x",
        "question_status": status,
        "model_statuses": model_statuses,
        "synthesis": SYNTHESIS.name,
    })
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
