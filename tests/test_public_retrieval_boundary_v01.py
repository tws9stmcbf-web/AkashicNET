"""Synthetic real-algorithm public boundary tests; no restricted input corpus."""
from __future__ import annotations

import copy
import json
import shutil

import pytest

from test_actual_retrieval_continuity_v01 import (
    ActualCLI, CANARY, CONCEPT, DEDUP, GRAPH, QUERY, ids,
)


@pytest.fixture
def cli(tmp_path):
    return ActualCLI(tmp_path)


def public_snapshot(cli):
    data = copy.deepcopy(cli.data)

    def mark(row, record_id):
        row.setdefault("public_safe", True)
        row.setdefault("metadata_eligible", True)
        old = row.get("provenance", {})
        row["provenance"] = {"artifact_id": "artifact:synthetic-fixture",
                             "record_id": record_id, "independence_key": "source:synthetic-fixture",
                             "public_safe": old.get("public_safe", True)}

    for row in data[GRAPH]["nodes"] + data[CONCEPT]["concept_nodes"]:
        mark(row, row["node_id"])
    for row in data[CONCEPT]["reddit_edges"] + data[CONCEPT]["library_edges"]:
        mark(row, row["review_id"])
        for rep in row.get("representation_sources", []):
            mark(rep, rep["review_id"])
    for row in data[DEDUP]["retrieval_units"]:
        mark(row, row["retrieval_unit_id"])
    return {"schema_version": "public-retrieval-snapshot/0.1", "graph": data[GRAPH],
            "concept": data[CONCEPT], "dedup": data[DEDUP]}


def run_public(cli, snapshot, query=QUERY, *args):
    path = cli.root / "public-snapshot.json"
    path.write_text(json.dumps(snapshot), encoding="utf-8")
    return cli.run(query, "--snapshot", str(path), *args, script="query_public_v01.py")


def response(result):
    assert result.returncode == 0, result.stderr
    assert not result.stderr
    return json.loads(result.stdout)


def targets(snapshot):
    return {
        "concept": snapshot["concept"]["concept_nodes"][0],
        "family": snapshot["graph"]["nodes"][0],
        "reddit": snapshot["concept"]["reddit_edges"][0],
        "library": snapshot["concept"]["library_edges"][0],
        "representation": snapshot["concept"]["library_edges"][0]["representation_sources"][0],
        "unit": snapshot["dedup"]["retrieval_units"][0],
    }


BAD_FLAGS = [False, None, "missing", 0, 1, "true", "false", [], {}, [True]]


@pytest.mark.parametrize("target", ["concept", "family", "reddit", "library", "representation", "unit"])
@pytest.mark.parametrize("flag", ["public_safe", "metadata_eligible", "provenance.public_safe"])
@pytest.mark.parametrize("value", BAD_FLAGS)
def test_affirmative_boolean_eligibility_on_every_public_record(cli, target, flag, value):
    snapshot = public_snapshot(cli)
    row = targets(snapshot)[target]
    holder, key = (row["provenance"], "public_safe") if flag.startswith("provenance.") else (row, flag)
    if value == "missing":
        holder.pop(key)
    else:
        holder[key] = value
    # Place the canary in a field which the real algorithms would read/return.
    if target == "concept":
        row["label"] = QUERY + CANARY
    elif target == "family":
        row["label"] = CANARY
    elif target == "reddit":
        row["basis"] = CANARY
    elif target == "library":
        row["basis_set"] = [CANARY]
    elif target == "representation":
        row["original_source_ref"] = CANARY
    else:
        row["labels"] = [QUERY + CANARY]
    result = run_public(cli, snapshot)
    parsed = response(result)
    assert CANARY not in result.stdout + result.stderr
    if target == "concept":
        assert parsed["results"] == []
        assert parsed["summary"]["matched_concepts"] == []
    elif target in {"family", "library", "representation"}:
        assert "synthetic:hash" not in ids(parsed)
    elif target == "reddit":
        assert "synthetic:r-accept" not in ids(parsed)
    else:
        assert all(not x.get("logical_retrieval_units") for x in parsed["results"]
                   if x["source"].get("family_id") == "synthetic:hash")


@pytest.mark.parametrize("flag", ["public_safe", "metadata_eligible", "provenance.public_safe"])
@pytest.mark.parametrize("value", BAD_FLAGS)
def test_direct_route_uses_same_gate_before_matching_and_summary(cli, flag, value):
    snapshot = public_snapshot(cli)
    row = snapshot["dedup"]["retrieval_units"][2]
    holder, key = (row["provenance"], "public_safe") if flag.startswith("provenance.") else (row, flag)
    if value == "missing":
        holder.pop(key)
    else:
        holder[key] = value
    row["labels"] = ["synthetic direct title " + CANARY]
    result = run_public(cli, snapshot, "synthetic direct title")
    parsed = response(result)
    assert parsed["results"] == []
    assert parsed["summary"] == {"matched_concepts": [], "results_before_limit": 0,
        "results_returned": 0, "semantic_decision_counts": {}, "provenance_tier_counts": {}, "domain_counts": {}}
    assert CANARY not in result.stdout + result.stderr


@pytest.mark.parametrize("route", ["concept", "direct"])
@pytest.mark.parametrize("provenance", [None, {}, [], "unsafe", True,
    {"artifact_id": "artifact:ok", "record_id": "wrong", "independence_key": "source:ok", "public_safe": True},
    {"artifact_id": "file:///home/" + CANARY, "record_id": "synthetic:unit:synthetic:hash",
     "independence_key": "source:ok", "public_safe": True},
    {"artifact_id": "artifact:ok", "record_id": "synthetic:unit:synthetic:hash",
     "independence_key": "source:ok", "public_safe": True, "private_filename": CANARY},
])
def test_unsafe_or_unbound_provenance_rejected(cli, route, provenance):
    snapshot = public_snapshot(cli)
    row = snapshot["dedup"]["retrieval_units"][0 if route == "concept" else 2]
    row["provenance"] = provenance
    row["labels"] = [QUERY + CANARY]
    result = run_public(cli, snapshot)
    response(result)
    assert CANARY not in result.stdout + result.stderr
    assert row["retrieval_unit_id"] not in result.stdout


def test_allowlist_drops_arbitrary_fields_and_object_details_on_both_routes(cli):
    snapshot = public_snapshot(cli)
    for rows in (snapshot["graph"]["nodes"], snapshot["concept"]["concept_nodes"],
                 snapshot["concept"]["reddit_edges"], snapshot["concept"]["library_edges"],
                 snapshot["dedup"]["retrieval_units"]):
        for row in rows:
            row.update(private_filename=CANARY, surprise={"secret": CANARY}, error=CANARY)
    for row in snapshot["dedup"]["retrieval_units"]:
        row["sha256"] = CANARY
        row["manifestations"] = [{"private_filename": CANARY, "path": CANARY,
                                   "drive_object_id": CANARY, "public_safe": False}]
    snapshot["graph"]["edges"].append({"private": CANARY})
    snapshot["summary"] = {"private": CANARY}
    for query in (QUERY, "synthetic direct title"):
        result = run_public(cli, snapshot, query)
        parsed = response(result)
        assert parsed["results"]
        assert CANARY not in result.stdout + result.stderr
        for row in parsed["results"]:
            for unit in row.get("logical_retrieval_units", []):
                assert unit["manifestations"] == []
                assert unit["sha256"] is None
                assert "private_filename" not in unit and "surprise" not in unit


@pytest.mark.parametrize("field", ["label", "definition"])
@pytest.mark.parametrize("private_value", ["file:///home/private", "/My Drive/private",
    "https://drive.google.com/open?id=synthetic", "drive:file:synthetic", "AKM-synthetic"])
def test_known_private_markers_in_allowlisted_text_are_rejected(cli, field, private_value):
    snapshot = public_snapshot(cli)
    snapshot["concept"]["concept_nodes"][0][field] = QUERY + private_value
    assert response(run_public(cli, snapshot))["summary"]["matched_concepts"] == []


@pytest.mark.parametrize("mutation", ["decision", "rights", "scientific", "truth", "representation", "parent"])
def test_conflicting_controls_fail_closed_without_promoting_decisions(cli, mutation):
    snapshot = public_snapshot(cli)
    row = snapshot["concept"]["library_edges"][0]
    if mutation == "decision":
        row["accepted_edge"] = True
    elif mutation == "representation":
        row["representation_sources"][0]["accepted_edge"] = True
    elif mutation == "parent":
        row.update(accepted_edge=True, review_state="ACCEPTED", relationship="ABOUT")
    else:
        key = {"rights": "rights_promotion_allowed", "scientific": "scientific_evidence_promotion_allowed",
               "truth": "truth_inference_allowed"}[mutation]
        row[key] = True
    result = response(run_public(cli, snapshot))
    assert "synthetic:hash" not in ids(result)


def test_public_results_preserve_ranking_rights_states_and_private_interface(cli):
    private = cli.query()
    snapshot = public_snapshot(cli)
    before = cli.snapshot()
    public = response(run_public(cli, snapshot))
    assert ids(public) == ids(private)
    for actual, original in zip(public["results"], private["results"]):
        assert actual["semantic_decision"] == original["semantic_decision"]
        assert actual["evidence_profile"] == original["evidence_profile"]
        assert actual["contract_guards"] == original["contract_guards"]
        assert [u["rights_states"] for u in actual.get("logical_retrieval_units", [])] == [u["rights_states"] for u in original.get("logical_retrieval_units", [])]
    assert cli.snapshot() == before
    assert cli.query() == private
    assert public["policy"]["rights_promotion_allowed"] is False
    assert public["policy"]["scientific_evidence_promotion_allowed"] is False
    assert public["policy"]["truth_inference_allowed"] is False


def test_public_interface_never_reads_legacy_corpus_or_changes_its_input(cli):
    snapshot = public_snapshot(cli)
    first = response(run_public(cli, snapshot))
    path = cli.root / "public-snapshot.json"
    before = path.read_bytes()
    shutil.rmtree(cli.root / "data")
    second = cli.run(QUERY, "--snapshot", str(path), script="query_public_v01.py")
    assert response(second) == first
    assert path.read_bytes() == before


def test_private_local_canary_visibility_is_retained_as_an_explicit_trust_boundary(cli):
    row = cli.data[DEDUP]["retrieval_units"][0]
    row.update(public_safe=False, metadata_eligible=False)
    row["manifestations"][0]["private_filename"] = CANARY
    cli.write()
    assert CANARY in json.dumps(cli.query())
    result = run_public(cli, public_snapshot(cli))
    response(result)
    assert CANARY not in result.stdout + result.stderr


@pytest.mark.parametrize("kind", ["missing", "bad-json", "bad-shape", "duplicate-key", "nonfinite", "duplicate-id"])
def test_invalid_snapshots_have_constant_errors_no_payload_or_legacy_fallback(cli, kind):
    path = cli.root / (CANARY + ".json")
    if kind == "bad-json":
        path.write_text('{"' + CANARY)
    elif kind == "bad-shape":
        path.write_text(json.dumps({"schema_version": "public-retrieval-snapshot/0.1", "graph": CANARY}))
    elif kind == "duplicate-key":
        path.write_text('{"private": "' + CANARY + '", "private": true}')
    elif kind == "nonfinite":
        path.write_text('{"private": "' + CANARY + '", "value": NaN}')
    elif kind == "duplicate-id":
        snapshot = public_snapshot(cli)
        snapshot["concept"]["concept_nodes"].append(copy.deepcopy(snapshot["concept"]["concept_nodes"][0]))
        path.write_text(json.dumps(snapshot))
    result = cli.run(QUERY, "--snapshot", str(path), script="query_public_v01.py")
    assert result.returncode == 1
    assert result.stdout == ""
    assert result.stderr == "Public retrieval unavailable: invalid snapshot\n"
    assert CANARY not in result.stdout + result.stderr


@pytest.mark.parametrize("args", [(), ("--domain", CANARY), ("--state", CANARY),
    ("--limit", CANARY), ("--limit", "0"), ("--evidence", CANARY)])
def test_request_errors_do_not_echo_values_or_open_inputs(cli, args):
    shutil.rmtree(cli.root / "data")
    supplied = args if not args else ("--snapshot", CANARY, *args)
    result = cli.run(QUERY, *supplied, script="query_public_v01.py")
    assert result.returncode == 2
    assert result.stdout == ""
    assert result.stderr == "Invalid public retrieval request\n"


def test_multi_family_unit_cannot_publish_private_family_alias_or_direct_title(cli):
    snapshot = public_snapshot(cli)
    snapshot["graph"]["nodes"][0]["public_safe"] = False
    snapshot["dedup"]["retrieval_units"][2]["family_ids"].append("synthetic:hash")
    result = response(run_public(cli, snapshot, "synthetic direct title"))
    assert result["results"] == []


def test_public_domain_state_filter_and_limit_preserve_direct_metadata_distinction(cli):
    snapshot = public_snapshot(cli)
    parsed = response(run_public(cli, snapshot, QUERY, "--domain", "reddit", "--state", "hold", "--limit", "1"))
    assert ids(parsed) == ["synthetic:r-hold"]
    parsed = response(run_public(cli, snapshot, "synthetic direct title", "--state", "accepted"))
    assert parsed["results"][0]["semantic_decision"] == "DIRECT_METADATA_LOOKUP"
    assert response(run_public(cli, snapshot, "synthetic direct title", "--state", "hold"))["results"] == []


def test_runtime_exception_details_never_reach_public_output(cli):
    path = cli.root / "scripts/query_ranked_v023.py"
    code = path.read_text()
    old = "def retrieve(query, base, dedup, accepted_only=False):"
    assert code.count(old) == 1
    path.write_text(code.replace(old, old + '\n    raise ValueError("' + CANARY + '")'))
    result = run_public(cli, public_snapshot(cli))
    assert result.returncode == 1
    assert result.stdout == ""
    assert result.stderr == "Public retrieval unavailable: invalid snapshot\n"


@pytest.mark.parametrize("mutation", ["truthiness", "raw_manifestations", "raw_summary"])
def test_canary_oracles_detect_deliberate_boundary_regressions(cli, mutation):
    if mutation == "raw_summary":
        path = cli.root / "scripts/query_public_v01.py"
        old = '        response.update(contract="AKASHICNET_PUBLIC_RETRIEVAL", version="0.1")'
        new = old + '\n        response["summary"]["private"] = "' + CANARY + '"'
    else:
        path = cli.root / "scripts/public_retrieval_snapshot_v01.py"
        if mutation == "truthiness":
            old = 'row.get("public_safe") is True and row.get("metadata_eligible") is True'
            new = 'row.get("public_safe") and row.get("metadata_eligible")'
        else:
            old = '"sha256": None, "manifestations": []'
            new = '"sha256": None, "manifestations": row["manifestations"]'
    code = path.read_text()
    assert code.count(old) == 1
    path.write_text(code.replace(old, new))
    # Require a successful process, not a crash/import failure as detection.
    response(run_public(cli, public_snapshot(cli)))
    with pytest.raises(AssertionError):
        if mutation == "truthiness":
            test_affirmative_boolean_eligibility_on_every_public_record(cli, "unit", "public_safe", 1)
        else:
            test_allowlist_drops_arbitrary_fields_and_object_details_on_both_routes(cli)
