"""GAP-02: execute the real private/public CLIs using synthetic records only."""
from __future__ import annotations

import ast
import copy
import itertools
import json
import shutil

import pytest
from jsonschema import validate

from test_actual_retrieval_continuity_v01 import ActualCLI, CANARY, CONCEPT, DEDUP, GRAPH, QUERY, ROOT, edge, ids
from test_public_retrieval_boundary_v01 import public_snapshot, response, run_public

STATUSES = ["NOT_APPLICABLE", "UNASSESSED", "SOURCE_CLASSIFICATION_ONLY"]


@pytest.fixture
def cli(tmp_path):
    return ActualCLI(tmp_path)


def execute(cli, public, query=QUERY, *args):
    if public:
        return response(run_public(cli, public_snapshot(cli), query, *args))
    cli.write()
    return cli.query(query, *args)


def set_class(row, status):
    row.pop("evidence", None)
    row["evidence_status"] = status


def test_vocabulary_matches_authoritative_endpoint_validator():
    tree = ast.parse((ROOT / "scripts/validate_public_safe_endpoint_registry_v014.py").read_text())
    enums = [{x.value for x in node.elts} for node in ast.walk(tree)
             if isinstance(node, ast.Set) and all(isinstance(x, ast.Constant) for x in node.elts)]
    assert set(STATUSES) in enums
    schema = json.loads((ROOT / "references/community/unified-retrieval-schema-v0.25.json").read_text())
    assert set(schema["properties"]["request"]["properties"]["evidence"]["enum"]) == set(STATUSES)


@pytest.mark.parametrize("public,status,route,field", list(itertools.product(
    [False, True], STATUSES, ["reddit", "library", "direct"], ["evidence", "evidence_status"])))
def test_supported_statuses_on_every_route(cli, public, status, route, field):
    row = (cli.data[DEDUP]["retrieval_units"][2] if route == "direct" else
           cli.data[CONCEPT]["reddit_edges" if route == "reddit" else "library_edges"][0])
    row.pop("evidence", None)
    row[field] = status
    query = "synthetic direct title" if route == "direct" else QUERY
    parsed = execute(cli, public, query, "--evidence", status)
    target = {"reddit": "synthetic:r-accept", "library": "synthetic:hash", "direct": "synthetic:direct"}[route]
    assert target in ids(parsed)
    assert all(x["evidence_classification"] == status for x in parsed["results"])
    assert parsed["request"]["evidence"] == status
    if route == "direct":
        assert parsed["results"][0]["semantic_decision"] == "DIRECT_METADATA_LOOKUP"
    if not public:
        schema = json.loads((ROOT / "references/community/unified-retrieval-schema-v0.25.json").read_text())
        validate(parsed, schema)


BAD = [{}, {"evidence": None}, {"evidence": ""}, {"evidence": " UNASSESSED "},
       {"evidence": "unassessed"}, {"evidence": []}, {"evidence": {}}, {"evidence": True},
       {"evidence": ["UNASSESSED", "SOURCE_CLASSIFICATION_ONLY"]},
       {"evidence": CANARY}, {"evidence": "EMPIRICAL_REFERENCE"},
       {"evidence": "Established Evidence"},
       {"evidence": "UNASSESSED", "evidence_status": "SOURCE_CLASSIFICATION_ONLY"},
       {"evidence": "UNASSESSED", "evidence_status": None}]


@pytest.mark.parametrize("public,route,bad", list(itertools.product([False, True], ["reddit", "library", "direct"], BAD)))
def test_missing_or_ambiguous_classification_matches_no_explicit_filter(cli, public, route, bad):
    row = (cli.data[DEDUP]["retrieval_units"][2] if route == "direct" else
           cli.data[CONCEPT]["reddit_edges" if route == "reddit" else "library_edges"][0])
    row.pop("evidence", None)
    row.update(copy.deepcopy(bad))
    query = "synthetic direct title" if route == "direct" else QUERY
    target = {"reddit": "synthetic:r-accept", "library": "synthetic:hash", "direct": "synthetic:direct"}[route]
    baseline = execute(cli, public, query)
    assert target in ids(baseline)
    assert "evidence" not in baseline["request"]
    if public:
        assert CANARY not in json.dumps(baseline)
    for status in STATUSES:
        assert target not in ids(execute(cli, public, query, "--evidence", status))


@pytest.mark.parametrize("public,domain,state", list(itertools.product([False, True], ["all", "reddit", "library"], ["all", "accepted", "hold"])))
def test_combined_filters_select_subsequence_and_preserve_controls(cli, public, domain, state):
    set_class(cli.data[CONCEPT]["reddit_edges"][1], "UNASSESSED")
    set_class(cli.data[CONCEPT]["library_edges"][0], "UNASSESSED")
    original = execute(cli, public, QUERY, "--domain", domain, "--state", state)
    before = cli.snapshot()
    filtered = execute(cli, public, QUERY, "--domain", domain, "--state", state, "--evidence", "UNASSESSED")
    expected = [r for r in original["results"] if r["source"].get("family_id", r["source"].get("ref"))
                in {"synthetic:hash", "synthetic:r-hold"}]
    assert filtered["results"] == expected
    assert filtered["summary"]["results_before_limit"] == len(expected)
    assert filtered["policy"] == original["policy"]
    assert cli.snapshot() == before


@pytest.mark.parametrize("public", [False, True])
def test_evidence_filter_precedes_limit_and_does_not_use_provenance_or_decision(cli, public):
    # P3 HOLD and P1 ACCEPT are explicitly excluded; P0 HOLD is the sole match.
    for row in cli.data[CONCEPT]["library_edges"] + cli.data[CONCEPT]["reddit_edges"]:
        set_class(row, "SOURCE_CLASSIFICATION_ONLY")
    for n in range(150):
        cli.data[CONCEPT]["reddit_edges"].append(edge(f"synthetic:distractor:{n:03}", "ACCEPTED"))
    set_class(cli.data[CONCEPT]["reddit_edges"][1], "UNASSESSED")
    parsed = execute(cli, public, QUERY, "--evidence", "UNASSESSED", "--limit", "1")
    assert ids(parsed) == ["synthetic:r-hold"]
    assert parsed["summary"]["results_before_limit"] == 1
    assert parsed["summary"]["provenance_tier_counts"] == {"P0_TOPICAL_CANDIDATE": 1}
    assert parsed["results"][0]["semantic_decision"] == "HOLD"


@pytest.mark.parametrize("public,mode", list(itertools.product([False, True], ["unanimous", "mixed", "partial", "invalid", "conflicting-edge"])))
def test_representation_aggregation_is_conservative(cli, public, mode):
    row = cli.data[CONCEPT]["library_edges"][0]
    row.pop("evidence")
    rep = row["representation_sources"][0]
    set_class(rep, "UNASSESSED")
    second = copy.deepcopy(rep)
    second["review_id"] += ":second"
    if mode == "mixed": set_class(second, "SOURCE_CLASSIFICATION_ONLY")
    if mode == "partial": second.pop("evidence_status")
    if mode == "invalid": set_class(second, CANARY)
    if mode == "conflicting-edge": set_class(row, "SOURCE_CLASSIFICATION_ONLY")
    row["representation_sources"].append(second)
    row["representation_count"] = 2
    parsed = execute(cli, public, QUERY, "--evidence", "UNASSESSED")
    assert ("synthetic:hash" in ids(parsed)) is (mode == "unanimous")


def test_public_filter_cannot_reveal_rejected_classification_or_private_summaries(cli):
    snap = public_snapshot(cli)
    for row in snap["concept"]["reddit_edges"]:
        row["public_safe"] = False
        row["evidence"] = CANARY
    snap["dedup"]["retrieval_units"][2].update(public_safe=False, evidence="UNASSESSED")
    shutil.rmtree(cli.root / "data")
    for query in (QUERY, "synthetic direct title"):
        result = run_public(cli, snap, query, "--evidence", "UNASSESSED", "--limit", "1")
        parsed = response(result)
        assert parsed["results"] == []
        assert parsed["summary"]["results_before_limit"] == 0
        assert CANARY not in result.stdout + result.stderr


def test_equal_aliases_match_and_private_reddit_extras_do_not_affect_selection(cli):
    snap = public_snapshot(cli)
    row = snap["concept"]["reddit_edges"][0]
    row["evidence_status"] = row["evidence"]
    args = ("--evidence", "SOURCE_CLASSIFICATION_ONLY", "--domain", "reddit")
    original = response(run_public(cli, snap, QUERY, *args))
    assert "synthetic:r-accept" in ids(original)
    row["representation_sources"] = [{"public_safe": False, "evidence": CANARY}]
    assert response(run_public(cli, snap, QUERY, *args)) == original


@pytest.mark.parametrize("script", ["query_api_v025.py", "query_unified_v024.py", "query_public_v01.py"])
@pytest.mark.parametrize("status", [CANARY, "P3_SHA256_IDENTITY_PROVENANCE", "EMPIRICAL_REFERENCE", "all", "unassessed"])
def test_invalid_filter_is_rejected_before_loading_inputs(cli, script, status):
    shutil.rmtree(cli.root / "data")
    args = ("--snapshot", CANARY) if script == "query_public_v01.py" else ()
    result = cli.run(QUERY, *args, "--evidence", status, script=script)
    assert result.returncode == 2
    assert result.stdout == ""
    if script == "query_public_v01.py":
        assert result.stderr == "Invalid public retrieval request\n"


def test_normaliser_preserves_explicit_status_and_never_votes_on_mixed_values(cli):
    original = copy.deepcopy(cli.data[CONCEPT])
    original["library_edges"] = []
    for i, status in enumerate(["UNASSESSED", "SOURCE_CLASSIFICATION_ONLY"]):
        row = edge("synthetic:hash", "HOLD", library=True)
        row["review_id"] += str(i)
        row["evidence"] = status
        original["library_edges"].append(row)
    (cli.root / "data/concept-layer-v0.21.json").write_text(json.dumps(original))
    result = cli.run(script="normalise_semantic_representations_v022.py")
    assert result.returncode == 0, result.stderr
    normalised = json.loads((cli.root / "data" / CONCEPT).read_text())
    row = normalised["library_edges"][0]
    assert row["evidence_status"] is None
    assert [r["evidence"] for r in row["representation_sources"]] == ["UNASSESSED", "SOURCE_CLASSIFICATION_ONLY"]
    assert row["review_state"] == "HOLD" and row["accepted_edge"] is False


def test_oracle_detects_deliberate_unfiltered_provenance_substitute(cli):
    path = cli.root / "scripts/query_unified_v024.py"
    code = path.read_text()
    old = "        if evidence is not None and r.get('evidence_classification') != evidence: continue"
    assert code.count(old) == 1
    path.write_text(code.replace(old, "        # Deliberately skip evidence selection"))
    with pytest.raises(AssertionError):
        test_evidence_filter_precedes_limit_and_does_not_use_provenance_or_decision(cli, False)
