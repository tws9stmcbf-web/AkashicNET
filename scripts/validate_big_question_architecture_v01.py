#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARCH = ROOT / "references" / "big-questions" / "architecture-v0.1.json"
BQ_ROOT = ROOT / "references" / "big-questions"
COMMUNITY = ROOT / "references" / "community"
BQ_NAME = re.compile(r"^BQ\d{3}$")
COMMUNITY_BQ = re.compile(r"^bq\d{3}.*", re.IGNORECASE)
CANONICAL_BATCH = re.compile(r"^evidence-batch.*\.json$", re.IGNORECASE)


def assert_canonical_batch_registry(question_id: str, canonical: Path, batches: list[str], root: Path) -> None:
    registered = {str((root / batch).resolve()) for batch in batches}
    discovered = {
        str(path.resolve())
        for path in canonical.iterdir()
        if path.is_file() and CANONICAL_BATCH.fullmatch(path.name)
    }
    assert discovered == registered, (
        f"{question_id}: canonical evidence-batch registry drift; "
        f"unregistered={sorted(discovered - registered)}; "
        f"missing={sorted(registered - discovered)}"
    )


def main() -> int:
    architecture = json.loads(ARCH.read_text(encoding="utf-8"))
    assert architecture["canonical_root"] == "references/big-questions"
    rules = architecture["rules"]
    assert rules["one_canonical_tree_per_question"] is True
    assert rules["new_question_evidence_outside_canonical_root_allowed"] is False
    assert rules["legacy_parallel_records_are_read_only"] is True
    assert rules["legacy_records_count_as_incremental_evidence"] is False
    assert rules["legacy_records_may_upgrade_epistemic_state"] is False

    questions = architecture["questions"]
    assert questions, "at least one bounded question must be registered"

    registered_legacy = set()
    for question_id, record in questions.items():
        assert BQ_NAME.fullmatch(question_id), f"invalid question id: {question_id}"
        canonical = ROOT / record["canonical_path"]
        assert canonical.is_dir(), f"missing canonical question tree: {canonical}"
        assert canonical == BQ_ROOT / question_id
        spec = ROOT / record["spec"]
        assert spec.is_file(), f"missing question spec: {spec}"
        spec_payload = json.loads(spec.read_text(encoding="utf-8"))
        assert spec_payload.get("id", spec_payload.get("question_id")) == question_id

        batches = record.get("evidence_batches", [])
        assert batches, f"{question_id}: at least one canonical evidence batch required"
        assert len(batches) == len(set(batches)), f"{question_id}: duplicate canonical batch path"
        for batch_path in batches:
            path = ROOT / batch_path
            assert path.is_file(), f"missing canonical evidence batch: {path}"
            assert path.parent == canonical, f"{question_id}: batch escaped canonical tree"
            payload = json.loads(path.read_text(encoding="utf-8"))
            assert payload.get("question_id") == question_id
        assert_canonical_batch_registry(question_id, canonical, batches, ROOT)

        for legacy in record.get("legacy_parallel_records", []):
            path = legacy["path"]
            registered_legacy.add(path)
            assert legacy["status"] == "LEGACY_PARALLEL_READ_ONLY"
            assert (ROOT / path).is_file(), f"missing declared legacy record: {path}"
            replacement = legacy["canonical_replacement"]
            assert replacement in batches, f"legacy replacement must be a canonical batch: {replacement}"

    # Fail closed if a new BQ-shaped record appears in the community tree.
    # The one known historical duplicate is explicitly registered above and is read-only debt.
    community_bq_paths = {
        str(path.relative_to(ROOT))
        for path in COMMUNITY.iterdir()
        if path.is_file() and COMMUNITY_BQ.match(path.name)
    }
    unexpected = community_bq_paths - registered_legacy
    assert not unexpected, f"unregistered parallel bounded-question records: {sorted(unexpected)}"
    assert registered_legacy <= community_bq_paths, "declared legacy bounded-question record missing"

    invariants = architecture["release_invariants"]
    assert all(value is False for value in invariants.values())

    print(
        "BIG QUESTION ARCHITECTURE v0.1 PASS: "
        f"{len(questions)} canonical question tree(s); "
        f"{len(registered_legacy)} registered read-only legacy parallel record(s)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
