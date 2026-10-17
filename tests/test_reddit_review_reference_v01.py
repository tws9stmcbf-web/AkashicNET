"""GAP-03: authoritative Reddit review references through the real CLI paths."""
from __future__ import annotations

import copy
import json

import pytest

from test_actual_retrieval_continuity_v01 import ActualCLI, CANARY, CONCEPT, QUERY, edge
from test_public_retrieval_boundary_v01 import public_snapshot, response, run_public


STAGES = ["multihop_v022", "ranked_v023", "unified_v024", "api_v025", "public_v01"]


@pytest.fixture
def cli(tmp_path):
    return ActualCLI(tmp_path)


def query_stage(cli, stage, *args):
    if stage == "public_v01":
        return response(run_public(cli, public_snapshot(cli), QUERY, *args))
    return response(cli.run(QUERY, *args, script="query_" + stage + ".py"))


def reddit_rows(result):
    return [row for row in result["results"] if row["domain"] == "reddit"]


@pytest.mark.parametrize("stage", STAGES)
def test_review_ids_are_forwarded_verbatim_with_decisions_and_evidence(cli, stage):
    # IDs deliberately differ from source refs and each other, including case.
    expected = [
        ("synthetic:r-accept", "Review:Z.Accept_47", "ACCEPTED", "ACCEPT", 1, "UNASSESSED"),
        ("synthetic:r-hold", "Review:a.Hold_7", "HOLD", "HOLD", 0, "SOURCE_CLASSIFICATION_ONLY"),
        ("synthetic:r-reject", "Review:M.Reject_13", "REJECT", "REJECT", 0, "NOT_APPLICABLE"),
    ]
    for item, (_, review, _, _, _, evidence) in zip(cli.data[CONCEPT]["reddit_edges"], expected):
        item.update(review_id=review, evidence=evidence)
    cli.write()
    before = cli.snapshot()
    result = query_stage(cli, stage)
    rows = reddit_rows(result)
    assert [r["source"]["ref"] for r in rows] == [x[0] for x in expected]
    for actual, (source, review, state, decision, rank, evidence) in zip(rows, expected):
        assert actual["concept_hop"] == {
            "from": source, "relationship": "ABOUT" if state == "ACCEPTED" else "ABOUT_CANDIDATE",
            "to": "synthetic:c1", "review_state": state, "decision": decision,
            "basis": "synthetic human decision", "review_id": review, "not_truth_claim": True,
        }
        assert actual["evidence_classification"] == evidence
        assert actual["source"]["rights_status"] == "LINK_ONLY_METADATA"
        assert actual["source"]["scientific_evidence_default"] is False
        if stage != "multihop_v022":
            assert actual["evidence_profile"]["provenance_rank"] == rank
        if stage in {"unified_v024", "api_v025", "public_v01"}:
            assert actual["semantic_decision"] == decision
    assert cli.snapshot() == before


@pytest.mark.parametrize("stage,limit", [("ranked_v023", 100)] + [
    (stage, limit) for stage in STAGES[2:] for limit in [1, 2, 100]
])
@pytest.mark.parametrize("state", ["ACCEPTED", "HOLD"])
def test_distinct_reviews_of_same_source_survive_stable_order_and_limits(cli, stage, state, limit):
    rows = [edge("synthetic:same-source", state) for _ in range(2)]
    for row, ref in zip(rows, ["synthetic:review:z", "synthetic:review:a"]):
        row["review_id"] = ref
    cli.data[CONCEPT]["reddit_edges"] = rows
    cli.data[CONCEPT]["library_edges"] = []
    cli.write()
    args = () if stage == "ranked_v023" else (
        "--domain", "reddit", "--state", "accepted" if state == "ACCEPTED" else "hold",
        "--evidence", "SOURCE_CLASSIFICATION_ONLY", "--limit", str(limit),
    )
    first = query_stage(cli, stage, *args)
    expected = ["synthetic:review:a", "synthetic:review:z"]
    if stage != "ranked_v023":
        expected = expected[:limit]
        assert first["summary"]["results_before_limit"] == 2
    assert [r["concept_hop"]["review_id"] for r in first["results"]] == expected
    assert all(r["evidence_profile"]["provenance_rank"] == (1 if state == "ACCEPTED" else 0)
               for r in first["results"])
    cli.data[CONCEPT]["reddit_edges"].reverse()
    cli.write()
    assert query_stage(cli, stage, *args) == first


@pytest.mark.parametrize("stage", STAGES[:-1])
@pytest.mark.parametrize("missing", [True, False], ids=["absent", "null"])
def test_legacy_missing_reference_is_null_without_fabrication_or_decision_changes(cli, stage, missing):
    for row in cli.data[CONCEPT]["reddit_edges"]:
        if missing:
            row.pop("review_id")
        else:
            row["review_id"] = None
    cli.write()
    before = cli.snapshot()
    rows = reddit_rows(query_stage(cli, stage))
    assert [r["concept_hop"]["review_id"] for r in rows] == [None, None, None]
    assert [r["concept_hop"]["decision"] for r in rows] == ["ACCEPT", "HOLD", "REJECT"]
    assert cli.snapshot() == before


@pytest.mark.parametrize("state", ["ACCEPTED", "HOLD"])
@pytest.mark.parametrize("mutation", [
    "missing", "null", "empty", "number", "object", "private_path", "private_provider",
    "unbound", "public_safe", "metadata_eligible", "provenance_private", "decision",
])
def test_public_review_rejection_precedes_output_counts_and_limits(cli, state, mutation):
    snapshot = public_snapshot(cli)
    # Add a candidate that would sort before the eligible target if admitted.
    bad = copy.deepcopy(snapshot["concept"]["reddit_edges"][0 if state == "ACCEPTED" else 1])
    bad.update(source_ref="synthetic:000-private", review_id="synthetic:review:" + CANARY)
    bad["provenance"]["record_id"] = bad["review_id"]
    bad["basis"] = CANARY
    if mutation == "missing":
        bad.pop("review_id")
    elif mutation in {"null", "empty", "number", "object", "private_path", "private_provider"}:
        value = {"null": None, "empty": "", "number": 47, "object": {"secret": CANARY},
                 "private_path": "file:///home/" + CANARY,
                 "private_provider": "drive:file:" + CANARY}[mutation]
        bad["review_id"] = bad["provenance"]["record_id"] = value
    elif mutation == "unbound":
        bad["provenance"]["record_id"] = "synthetic:different-review"
    elif mutation in {"public_safe", "metadata_eligible"}:
        bad[mutation] = False
    elif mutation == "provenance_private":
        bad["provenance"]["public_safe"] = False
    else:
        bad["v021_decision"] = "HOLD" if state == "ACCEPTED" else "ACCEPT"
    args = ("--domain", "reddit", "--state", "accepted" if state == "ACCEPTED" else "hold",
            "--evidence", "SOURCE_CLASSIFICATION_ONLY", "--limit", "1")
    expected = response(run_public(cli, snapshot, QUERY, *args))
    snapshot["concept"]["reddit_edges"].insert(0, bad)
    result = run_public(cli, snapshot, QUERY, *args)
    assert response(result) == expected
    assert CANARY not in result.stdout + result.stderr
    assert expected["summary"]["results_before_limit"] == 1
    assert expected["results"][0]["concept_hop"]["review_id"] == (
        "synthetic:review:synthetic:r-accept" if state == "ACCEPTED" else "synthetic:review:synthetic:r-hold")


def test_normalizer_preserves_reddit_references_without_rebinding(cli):
    raw = copy.deepcopy(cli.data[CONCEPT])
    raw["reddit_edges"][0]["review_id"] = "Review:authoritative-A"
    raw["reddit_edges"][1]["review_id"] = "Review:authoritative-H"
    source = cli.root / "data/concept-layer-v0.21.json"
    source.write_text(json.dumps(raw), encoding="utf-8")
    before = source.read_bytes()
    result = cli.run(script="normalise_semantic_representations_v022.py")
    assert result.returncode == 0, result.stderr
    rebuilt = json.loads((cli.root / "data" / CONCEPT).read_text())
    assert rebuilt["reddit_edges"] == raw["reddit_edges"]
    rows = reddit_rows(cli.query())
    assert [r["concept_hop"]["review_id"] for r in rows[:2]] == [
        "Review:authoritative-A", "Review:authoritative-H"]
    assert source.read_bytes() == before


@pytest.mark.parametrize("mutation", ["drop", "fabricate"])
def test_forwarding_oracle_detects_successfully_executed_regressions(cli, mutation):
    path = cli.root / "scripts/query_multihop_v022.py"
    code = path.read_text()
    old = "'review_id':e.get('review_id'),"
    new = "" if mutation == "drop" else "'review_id':e['source_ref'],"
    assert code.count(old) == 1
    path.write_text(code.replace(old, new))
    cli.query()  # A syntax/import failure must not count as regression detection.
    with pytest.raises(AssertionError):
        test_review_ids_are_forwarded_verbatim_with_decisions_and_evidence(cli, "api_v025")
