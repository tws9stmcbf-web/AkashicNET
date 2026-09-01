#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARCH = ROOT / "references" / "big-questions" / "architecture-v0.1.json"


def main() -> int:
    payload = json.loads(ARCH.read_text(encoding="utf-8"))
    assert payload.get("canonical_root") == "references/big-questions"
    rules = payload.get("rules", {})
    assert rules.get("one_canonical_tree_per_question") is True
    assert rules.get("new_question_evidence_outside_canonical_root_allowed") is False
    questions = payload.get("questions")
    assert isinstance(questions, dict) and questions, "questions registry must be non-empty"
    for qid, record in questions.items():
        assert qid.startswith("BQ") and len(qid) == 5 and qid[2:].isdigit(), f"invalid question id: {qid}"
        assert record.get("canonical_path") == f"references/big-questions/{qid}"
        assert (ROOT / record["canonical_path"]).is_dir()
        assert (ROOT / record["spec"]).is_file()
    print(f"BIG QUESTIONS REGISTRY v0.13 PASS: extensible registry with {len(questions)} registered question(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
