"""Run the real v0.25 -> v0.24 -> v0.23 -> v0.22 CLI on synthetic data.

No production corpus, mocked subprocess, alternate ranker, or SQLite adapter.
The original gap contracts are ordinary regressions after their bounded fixes.
"""
from __future__ import annotations

import copy
import json
import os
from pathlib import Path
import random
import shutil
import subprocess
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = (
    "retrieval_evidence_v01.py", "query_api_v025.py", "query_unified_v024.py", "query_ranked_v023.py",
    "query_multihop_v022.py", "normalise_semantic_representations_v022.py",
    "query_public_v01.py", "public_retrieval_snapshot_v01.py", "check_public_data_boundary.py",
)
GRAPH = "knowledge-graph-v0.16.json"
CONCEPT = "concept-layer-v0.22.json"
DEDUP = "dedup-retrieval-view-v0.17.json"
QUERY = "synthetic rare concept"
CANARY = "SYNTHETIC_PRIVATE_CANARY_DO_NOT_RETURN"


def edge(source, state, *, library=False, concept="synthetic:c1"):
    row = {
        "target_concept": concept, "source_ref": source,
        "relationship": "ABOUT" if state == "ACCEPTED" else "ABOUT_CANDIDATE",
        "review_state": state, "accepted_edge": state == "ACCEPTED",
        "basis": "synthetic human decision", "review_id": "synthetic:review:" + source,
        "public_safe": True, "metadata_eligible": True,
        "evidence": "SOURCE_CLASSIFICATION_ONLY",
        "provenance": {"record_id": source, "public_safe": True},
    }
    if library:
        row.update(logical_family_id=source, basis_set=[row["basis"]],
                   representation_count=1, representation_sources=[{
                       "original_source_ref": source, "review_id": row["review_id"],
                       "review_state": state, "accepted_edge": row["accepted_edge"],
                   }])
    else:
        row["v021_decision"] = "ACCEPT" if state == "ACCEPTED" else state
    return row


def unit(family, *, hashed=False, label="synthetic catalogue title"):
    return {
        "retrieval_unit_id": "synthetic:unit:" + family,
        "family_ids": [family], "labels": [label],
        "collapse_basis": "SHA256_MATCH_VERIFIED" if hashed else "NOT_COLLAPSED_NO_HASH_IDENTITY",
        "deduplicated": False, "physical_manifestation_count": 1,
        "sha256": "a" * 64 if hashed else None,
        "manifestations": [{"manifestation_id": "synthetic:manifest:" + family}],
        "rights_states": ["UNKNOWN_UNVERIFIED"],
        "public_safe": True, "metadata_eligible": True,
        "provenance": {"record_id": family, "public_safe": True},
        "evidence": "UNASSESSED",
        "not_truth_claim": True, "rights_promotion_allowed": False,
        "scientific_evidence_promotion_allowed": False,
    }


def fixture_data():
    families = ["synthetic:hash", "synthetic:plain", "synthetic:unresolved", "synthetic:direct"]
    return {
        GRAPH: {"nodes": [{"node_id": f, "family_id": f, "node_type": "canonical_family",
                           "label": "synthetic catalogue title"} for f in families],
                "edges": [
                    {"id": "synthetic:proposal", "review_state": "REVIEW_REQUIRED", "accepted_edge": False},
                    {"id": "synthetic:human-child", "parent": "synthetic:proposal",
                     "review_state": "ACCEPTED", "adjudication_ref": "synthetic:human-decision"},
                ]},
        CONCEPT: {
            "concept_nodes": [
                {"node_id": "synthetic:c1", "label": QUERY, "definition": "synthetic target"},
                {"node_id": "synthetic:c2", "label": "synthetic other concept", "definition": "unrelated"},
            ],
            "reddit_edges": [edge("synthetic:r-accept", "ACCEPTED"),
                             edge("synthetic:r-hold", "HOLD"), edge("synthetic:r-reject", "REJECT"),
                             edge("synthetic:r-other", "ACCEPTED", concept="synthetic:c2")],
            "library_edges": [edge("synthetic:hash", "HOLD", library=True),
                              edge("synthetic:plain", "ACCEPTED", library=True),
                              edge("synthetic:unresolved", "HOLD", library=True)],
        },
        DEDUP: {"retrieval_units": [unit("synthetic:hash", hashed=True), unit("synthetic:plain"),
                                   unit("synthetic:direct", hashed=True, label="synthetic direct title")]},
    }


class ActualCLI:
    """Test-only CWD adapter: production scripts are copied byte-for-byte."""

    def __init__(self, root):
        self.root = root
        (root / "scripts").mkdir()
        (root / "data").mkdir()
        (root / "bin").mkdir()
        # The legacy subprocess chain invokes literal `python` at each hop.
        (root / "bin/python").symlink_to(sys.executable)
        self.env = {"PATH": str(root / "bin") + os.pathsep + os.defpath,
                    "PYTHONDONTWRITEBYTECODE": "1", "PYTHONIOENCODING": "utf-8"}
        for name in SCRIPTS:
            source = ROOT / "scripts" / name
            target = root / "scripts" / name
            shutil.copyfile(source, target)
            assert target.read_bytes() == source.read_bytes()
        self.data = fixture_data()
        self.write()

    def write(self):
        for name, payload in self.data.items():
            (self.root / "data" / name).write_text(json.dumps(payload), encoding="utf-8")

    def snapshot(self):
        return {str(p.relative_to(self.root)): p.read_bytes()
                for folder in ("data", "scripts") for p in (self.root / folder).rglob("*") if p.is_file()}

    def run(self, query=QUERY, *args, script="query_api_v025.py"):
        return subprocess.run([sys.executable, "scripts/" + script, query, *args],
                              cwd=self.root, env=self.env, capture_output=True, text=True, timeout=15)

    def query(self, query=QUERY, *args):
        result = self.run(query, *args)
        assert result.returncode == 0, result.stderr
        return json.loads(result.stdout)


@pytest.fixture
def cli(tmp_path):
    return ActualCLI(tmp_path)


def ids(response):
    return [r["source"].get("family_id") or r["source"]["ref"] for r in response["results"]]


def test_real_chain_wraps_upstream_without_changing_results(cli):
    api = cli.query()
    upstream = cli.run(script="query_unified_v024.py")
    assert upstream.returncode == 0
    unified = json.loads(upstream.stdout)
    assert api["api"] == "AKASHICNET_RETRIEVAL_API"
    assert api["api_version"] == "0.25"
    assert api["schema_id"] == "akashicnet://schemas/retrieval/v0.25"
    for key in ("request", "policy", "summary", "results"):
        assert api[key] == unified[key]
    assert api["compatibility"]["source_contract_version"] == "0.24"


@pytest.mark.parametrize("domain,state,expected", [
    ("all", "all", ["hash", "plain", "r-accept", "unresolved", "r-hold", "r-reject"]),
    ("reddit", "all", ["r-accept", "r-hold", "r-reject"]),
    ("library", "all", ["hash", "plain", "unresolved"]),
    ("all", "accepted", ["plain", "r-accept"]),
    ("all", "hold", ["hash", "unresolved", "r-hold"]),
    ("reddit", "accepted", ["r-accept"]),
    ("reddit", "hold", ["r-hold"]),
    ("library", "accepted", ["plain"]),
    ("library", "hold", ["hash", "unresolved"]),
])
def test_domain_state_filters_have_frozen_expected_sources(cli, domain, state, expected):
    response = cli.query(QUERY, "--domain", domain, "--state", state)
    assert ids(response) == ["synthetic:" + x for x in expected]
    assert response["summary"]["matched_concepts"] == ["synthetic:c1"]
    assert response["summary"]["results_before_limit"] == len(expected)


def test_filter_precedes_limit_after_many_higher_ranked_distractors(cli):
    cli.data[CONCEPT]["library_edges"] = [edge("synthetic:unresolved", "HOLD", library=True)]
    cli.data[CONCEPT]["reddit_edges"] = [edge(f"synthetic:distractor:{n:03}", "ACCEPTED") for n in range(150)]
    cli.write()
    response = cli.query(QUERY, "--domain", "library", "--state", "hold", "--limit", "1")
    assert ids(response) == ["synthetic:unresolved"]
    assert response["summary"]["results_before_limit"] == 1


def test_provenance_rank_preserves_adjudication_rights_and_source_lineage(cli):
    response = cli.query()
    rows = response["results"]
    assert [r["evidence_profile"]["provenance_rank"] for r in rows] == [3, 2, 1, 0, 0, 0]
    assert [r["semantic_decision"] for r in rows] == ["HOLD", "ACCEPT", "ACCEPT", "HOLD", "HOLD", "REJECT"]
    # Strong byte-identity provenance does not accept the held topical relation.
    assert rows[0]["concept_hop"]["representation_sources"] == cli.data[CONCEPT]["library_edges"][0]["representation_sources"]
    assert rows[0]["logical_retrieval_units"][0]["manifestations"] == cli.data[DEDUP]["retrieval_units"][0]["manifestations"]
    assert rows[0]["logical_retrieval_units"][0]["rights_states"] == ["UNKNOWN_UNVERIFIED"]
    for row in rows:
        assert row["contract_guards"] == {
            "ranking_changes_semantic_decision": False, "not_truth_claim": True,
            "not_scientific_evidence_claim": True, "not_rights_clearance_claim": True,
            "not_safety_or_efficacy_claim": True,
        }
        for guard in ("not_truth_score", "not_scientific_evidence_score", "not_rights_score", "not_safety_or_efficacy_score"):
            assert row["evidence_profile"][guard] is True
    for guard in ("truth_inference_allowed", "rights_promotion_allowed", "scientific_evidence_promotion_allowed", "ranking_changes_semantic_decision"):
        assert response["policy"][guard] is False
    for row in rows:
        if row["domain"] == "reddit":
            assert row["source"]["rights_status"] == "LINK_ONLY_METADATA"
            assert row["source"]["scientific_evidence_default"] is False


def test_direct_title_lookup_does_not_create_semantic_acceptance(cli):
    response = cli.query("synthetic direct title", "--state", "accepted")
    assert ids(response) == ["synthetic:direct"]
    assert response["results"][0]["semantic_decision"] == "DIRECT_METADATA_LOOKUP"
    assert response["results"][0]["not_semantic_inference"] is True
    assert cli.query("synthetic direct title", "--state", "hold")["results"] == []


def test_fresh_process_reopen_preserves_data_proposals_and_human_decisions(cli):
    before = cli.snapshot()
    first = cli.query()
    assert cli.query() == first
    assert cli.snapshot() == before


def test_unreferenced_synthetic_private_store_is_not_searched(cli):
    (cli.root / "data/synthetic-private-store.json").write_text(
        json.dumps({"label": QUERY, "private_filename": CANARY}), encoding="utf-8")
    response = cli.query()
    assert CANARY not in json.dumps(response)
    assert len(response["results"]) == 6


@pytest.mark.parametrize("seed", [7, 47, 400])
def test_distinct_rank_keys_survive_input_order(cli, seed):
    expected = cli.query()
    rng = random.Random(seed)
    for values in (cli.data[GRAPH]["nodes"], cli.data[CONCEPT]["reddit_edges"],
                   cli.data[CONCEPT]["library_edges"], cli.data[DEDUP]["retrieval_units"]):
        rng.shuffle(values)
    cli.write()
    assert cli.query() == expected


def test_representation_count_does_not_increase_rank_or_acceptance(cli):
    first = cli.query()
    cli.data[CONCEPT]["library_edges"][0]["representation_count"] = 47
    cli.write()
    second = cli.query()
    assert ids(second) == ids(first)
    assert second["results"][0]["evidence_profile"] == first["results"][0]["evidence_profile"]
    assert second["results"][0]["semantic_decision"] == "HOLD"


def test_semantic_rebuild_retains_human_representation_decisions(cli):
    raw = copy.deepcopy(cli.data[CONCEPT])
    raw["library_edges"].append(copy.deepcopy(raw["library_edges"][0]))
    source = cli.root / "data/concept-layer-v0.21.json"
    source.write_text(json.dumps(raw), encoding="utf-8")
    protected = {name: (cli.root / "data" / name).read_bytes() for name in (GRAPH, DEDUP, source.name)}
    result = cli.run(script="normalise_semantic_representations_v022.py")
    assert result.returncode == 0, result.stderr
    first = cli.query()
    rebuilt = (cli.root / "data" / CONCEPT).read_bytes()
    result = cli.run(script="normalise_semantic_representations_v022.py")
    assert result.returncode == 0
    assert (cli.root / "data" / CONCEPT).read_bytes() == rebuilt
    assert cli.query() == first
    assert ids(first) == ["synthetic:" + x for x in ["hash", "plain", "r-accept", "unresolved", "r-hold", "r-reject"]]
    assert first["results"][0]["concept_hop"]["representation_count"] == 1
    assert first["results"][0]["concept_hop"]["representation_sources"][0]["review_id"] == "synthetic:review:synthetic:hash"
    assert first["results"][0]["semantic_decision"] == "HOLD"
    for name, payload in protected.items():
        assert (cli.root / "data" / name).read_bytes() == payload


@pytest.mark.parametrize("name", [GRAPH, CONCEPT, DEDUP])
@pytest.mark.parametrize("failure", ["absent", "malformed"])
def test_missing_or_malformed_inputs_emit_no_success_response_or_writes(cli, name, failure):
    path = cli.root / "data" / name
    if failure == "absent":
        path.unlink()
    else:
        path.write_text("{", encoding="utf-8")
    before = cli.snapshot()
    result = cli.run()
    assert result.returncode != 0
    assert not result.stdout.strip()
    assert cli.snapshot() == before


@pytest.mark.parametrize("args", [
    ("--domain", "unknown"), ("--state", "approve"), ("--limit", "0"),
    ("--limit", "-1"), ("--evidence", "UNKNOWN_CLASSIFICATION"), ("--source", "library"),
])
def test_unsupported_or_invalid_requests_are_rejected_before_data_access(cli, args):
    shutil.rmtree(cli.root / "data")
    result = cli.run(QUERY, *args)
    assert result.returncode == 2
    assert "usage:" in result.stderr
    assert not result.stdout.strip()
    assert "Traceback" not in result.stderr


@pytest.mark.parametrize("mutation", ["domain", "adjudication", "rank"])
def test_oracles_detect_controlled_regressions_in_isolated_script_copies(cli, mutation):
    # These are deliberate negative controls; tracked production files stay intact.
    if mutation == "rank":
        script = "query_ranked_v023.py"
        old, new = "-r['evidence_profile']['provenance_rank']", "r['evidence_profile']['provenance_rank']"
    elif mutation == "adjudication":
        script = "query_unified_v024.py"
        old, new = "x['semantic_decision']=decision", "x['semantic_decision']='ACCEPT'"
    else:
        script = "query_unified_v024.py"
        old = "if domain!='all' and r.get('domain')!=domain: continue"
        new = "# deliberately omitted domain filter"
    path = cli.root / "scripts" / script
    code = path.read_text(encoding="utf-8")
    assert code.count(old) == 1
    path.write_text(code.replace(old, new), encoding="utf-8")
    # First require successful execution, so a syntax/import error cannot count as detection.
    cli.query()
    with pytest.raises(AssertionError):
        if mutation == "domain":
            test_domain_state_filters_have_frozen_expected_sources(
                cli, "reddit", "all", ["r-accept", "r-hold", "r-reject"])
        else:
            test_provenance_rank_preserves_adjudication_rights_and_source_lineage(cli)


@pytest.mark.parametrize("route", ["concept", "direct"])
def test_contract_private_canary_must_be_excluded_on_both_routes(cli, route):
    item = cli.data[DEDUP]["retrieval_units"][0 if route == "concept" else 2]
    item.update(public_safe=False, metadata_eligible=False)
    item["provenance"]["public_safe"] = False
    item["manifestations"][0]["private_filename"] = CANARY
    cli.write()
    from test_public_retrieval_boundary_v01 import public_snapshot, run_public
    response = run_public(cli, public_snapshot(cli), QUERY if route == "concept" else "synthetic direct title")
    assert response.returncode == 0, response.stderr
    assert CANARY not in response.stdout + response.stderr


def test_contract_evidence_filter_must_be_executable_and_independent_of_provenance(cli):
    result = cli.run(QUERY, "--evidence", "SOURCE_CLASSIFICATION_ONLY", "--domain", "reddit")
    assert result.returncode == 0, "Evidence filter is not executable"
    assert ids(json.loads(result.stdout)) == ["synthetic:r-accept", "synthetic:r-hold", "synthetic:r-reject"]


def test_contract_reddit_adjudication_reference_must_reach_response(cli):
    row = cli.query(QUERY, "--domain", "reddit", "--state", "accepted")["results"][0]
    assert row["concept_hop"].get("review_id") == "synthetic:review:synthetic:r-accept"


def test_contract_equal_rank_keys_require_stable_tie_break(cli):
    second = edge("synthetic:r-accept", "ACCEPTED", concept="synthetic:c2")
    cli.data[CONCEPT]["reddit_edges"].append(second)
    cli.data[CONCEPT]["concept_nodes"][1]["label"] = QUERY + " second"
    cli.write()
    first = cli.query(QUERY, "--domain", "reddit", "--state", "accepted", "--limit", "1")
    cli.data[CONCEPT]["reddit_edges"].reverse()
    cli.write()
    assert cli.query(QUERY, "--domain", "reddit", "--state", "accepted", "--limit", "1") == first
