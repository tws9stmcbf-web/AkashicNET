"""GAP-04: real CLI permutations and independent frozen identity oracles."""
from __future__ import annotations

import copy
import importlib.util
import itertools
import json
import sys

import pytest

from test_actual_retrieval_continuity_v01 import (
    ActualCLI, CANARY, CONCEPT, DEDUP, GRAPH, QUERY, ROOT, edge, unit,
)
from test_public_retrieval_boundary_v01 import public_snapshot, response, run_public


@pytest.fixture
def cli(tmp_path):
    return ActualCLI(tmp_path)


def execute(cli, public, query=QUERY, *args):
    if public:
        return response(run_public(cli, public_snapshot(cli), query, *args))
    cli.write()
    return cli.query(query, *args)


def tied_fixture(cli, domain, state):
    # Same visible label and source: only the exact target ID distinguishes the
    # logical observations. Larger ID arrives first deliberately.
    cli.data[CONCEPT]['concept_nodes'][1]['label'] = QUERY
    rows = [edge('synthetic:shared', state, library=domain == 'library', concept=target)
            for target in ['synthetic:c2', 'synthetic:c1']]
    for n, row in enumerate(rows):
        row['review_id'] += ':' + str(n)
        if domain == 'library':
            row['representation_sources'][0]['review_id'] = row['review_id']
    cli.data[CONCEPT]['reddit_edges'] = rows if domain == 'reddit' else []
    cli.data[CONCEPT]['library_edges'] = rows if domain == 'library' else []
    cli.data[GRAPH]['nodes'] = [{'node_id': 'synthetic:shared', 'family_id': 'synthetic:shared',
                                'node_type': 'canonical_family', 'label': 'catalogue'}]
    cli.data[DEDUP]['retrieval_units'] = [unit('synthetic:shared', hashed=True)] if domain == 'library' else []


@pytest.mark.parametrize('public,domain,state,limit', list(itertools.product(
    [False, True], ['reddit', 'library'], ['ACCEPTED', 'HOLD'], [1, 2, 100])))
def test_equal_source_keys_use_exact_concept_identity_before_limit(cli, public, domain, state, limit):
    tied_fixture(cli, domain, state)
    before = copy.deepcopy(cli.data)
    args = ('--domain', domain, '--state', 'accepted' if state == 'ACCEPTED' else 'hold',
            '--evidence', 'SOURCE_CLASSIFICATION_ONLY', '--limit', str(limit))
    first = execute(cli, public, QUERY, *args)
    assert [r['concept_hop']['to'] for r in first['results']] == ['synthetic:c1', 'synthetic:c2'][:limit]
    assert first['summary']['results_before_limit'] == 2
    assert all(r['semantic_decision'] == ('ACCEPT' if state == 'ACCEPTED' else 'HOLD') for r in first['results'])
    assert all(r['evidence_profile']['provenance_rank'] == (3 if domain == 'library' else 1 if state == 'ACCEPTED' else 0)
               for r in first['results'])
    cli.data[CONCEPT][domain + '_edges'].reverse()
    cli.data[CONCEPT]['concept_nodes'].reverse()
    assert execute(cli, public, QUERY, *args) == first
    assert sorted(cli.data[CONCEPT][domain + '_edges'], key=lambda r: r['target_concept']) == sorted(
        before[CONCEPT][domain + '_edges'], key=lambda r: r['target_concept'])
    assert all(first['policy'][k] is False for k in
               ['truth_inference_allowed', 'rights_promotion_allowed', 'scientific_evidence_promotion_allowed'])


@pytest.mark.parametrize('public', [False, True])
@pytest.mark.parametrize('limit', [1, 2, 100])
def test_direct_units_with_same_family_and_label_keep_distinct_identity(cli, public, limit):
    cli.data[DEDUP]['retrieval_units'] = [unit('synthetic:direct') for _ in range(2)]
    for row, suffix in zip(cli.data[DEDUP]['retrieval_units'], ['z', 'a']):
        row['retrieval_unit_id'] += ':' + suffix
        row['labels'] = ['synthetic direct title']
    args = ('--state', 'accepted', '--limit', str(limit))
    first = execute(cli, public, 'synthetic direct title', *args)
    assert [r['logical_retrieval_units'][0]['retrieval_unit_id'] for r in first['results']] == [
        'synthetic:unit:synthetic:direct:a', 'synthetic:unit:synthetic:direct:z'][:limit]
    assert first['summary']['results_before_limit'] == 2
    assert all(r['semantic_decision'] == 'DIRECT_METADATA_LOOKUP' for r in first['results'])
    cli.data[DEDUP]['retrieval_units'].reverse()
    assert execute(cli, public, 'synthetic direct title', *args) == first


@pytest.mark.parametrize('public', [False, True])
def test_duplicate_observations_are_not_merged_or_overwritten(cli, public):
    tied_fixture(cli, 'reddit', 'ACCEPTED')
    base = cli.data[CONCEPT]['reddit_edges'][1]
    other = copy.deepcopy(base)
    other.update(basis='zzz independent human rationale', review_id='synthetic:review:other')
    exact = copy.deepcopy(base)
    cli.data[CONCEPT]['reddit_edges'] = [other, exact, base]
    first = execute(cli, public, QUERY, '--domain', 'reddit', '--limit', '100')
    assert len(first['results']) == 3
    assert [r['concept_hop']['basis'] for r in first['results']] == [base['basis'], base['basis'], other['basis']]
    assert first['results'][0] == first['results'][1]
    cli.data[CONCEPT]['reddit_edges'].reverse()
    assert execute(cli, public, QUERY, '--domain', 'reddit', '--limit', '100') == first
    assert execute(cli, public, QUERY, '--domain', 'reddit', '--limit', '1')['results'] == first['results'][:1]


def test_legacy_direct_duplicate_suppression_selects_repeatable_payload(cli):
    first = unit('synthetic:direct', label='synthetic direct title z')
    second = copy.deepcopy(first)
    second['labels'] = ['synthetic direct title a']
    cli.data[DEDUP]['retrieval_units'] = [first, second, copy.deepcopy(second)]
    result = execute(cli, False, 'synthetic direct title')
    assert result['summary']['results_before_limit'] == 1
    assert result['results'][0]['source']['label'] == second['labels'][0]
    cli.data[DEDUP]['retrieval_units'].reverse()
    assert execute(cli, False, 'synthetic direct title') == result
    # Public duplicate unit IDs retain the existing fail-closed behavior.
    failed = run_public(cli, public_snapshot(cli), 'synthetic direct title')
    assert failed.returncode != 0 and not failed.stdout
    assert failed.stderr == 'Public retrieval unavailable: invalid snapshot\n'


@pytest.mark.parametrize('flag', ['public_safe', 'metadata_eligible', 'provenance.public_safe'])
def test_public_rejected_tied_candidate_cannot_affect_top_one_or_counts(cli, flag):
    tied_fixture(cli, 'reddit', 'ACCEPTED')
    baseline = execute(cli, True, QUERY, '--limit', '1')
    rejected = copy.deepcopy(cli.data[CONCEPT]['reddit_edges'][1])
    rejected['target_concept'] = 'synthetic:c0'
    rejected['basis'] = CANARY
    holder, key = (rejected['provenance'], 'public_safe') if flag.startswith('provenance.') else (rejected, flag)
    holder[key] = False
    cli.data[CONCEPT]['reddit_edges'].insert(0, rejected)
    result = run_public(cli, public_snapshot(cli), QUERY, '--limit', '1')
    assert response(result) == baseline
    assert CANARY not in result.stdout + result.stderr
    cli.data[CONCEPT]['reddit_edges'].reverse()
    assert execute(cli, True, QUERY, '--limit', '1') == baseline


def test_ranked_source_dictionary_insertion_order_is_not_a_key():
    # v022 constructs dictionaries in one fixed order; exercise the callable
    # ranker too, where equivalent caller dictionaries may arrive differently.
    sys.path.insert(0, str(ROOT / 'scripts'))
    try:
        spec = importlib.util.spec_from_file_location('tie_ranker', ROOT / 'scripts/query_ranked_v023.py')
        ranked = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(ranked)
    finally:
        sys.path.pop(0)
    a = {'domain': 'reddit', 'source': {'ref': 'synthetic:a', 'type': 'reddit_record'},
         'concept_hop': {'to': 'synthetic:c1', 'review_state': 'ACCEPTED'}}
    z = copy.deepcopy(a)
    z['source'] = {'type': 'reddit_record', 'ref': 'synthetic:z'}
    expected = ranked.retrieve(QUERY, {'results': [z, a], 'matched_concepts': []}, {'retrieval_units': []})
    assert [r['source']['ref'] for r in expected['results']] == ['synthetic:a', 'synthetic:z']
    a['source'] = dict(reversed(list(a['source'].items())))
    z['source'] = dict(reversed(list(z['source'].items())))
    assert ranked.retrieve(QUERY, {'results': [a, z], 'matched_concepts': []}, {'retrieval_units': []}) == expected


@pytest.mark.parametrize('script', ['query_multihop_v022.py', 'query_ranked_v023.py', 'query_unified_v024.py'])
def test_stage_contract_preserves_candidates_and_ranker_orders_them(cli, script):
    tied_fixture(cli, 'reddit', 'ACCEPTED')
    cli.write()
    result = cli.run(script=script)
    assert result.returncode == 0, result.stderr
    targets = [r['concept_hop']['to'] for r in json.loads(result.stdout)['results']]
    # Multihop is a candidate builder, not a ranker. Ordering begins at v023.
    assert targets == (['synthetic:c2', 'synthetic:c1'] if script == 'query_multihop_v022.py'
                       else ['synthetic:c1', 'synthetic:c2'])


@pytest.mark.parametrize('public', [False, True])
def test_multiple_units_on_one_concept_have_stable_order_without_changing_lineage(cli, public):
    tied_fixture(cli, 'library', 'HOLD')
    first = cli.data[DEDUP]['retrieval_units'][0]
    second = copy.deepcopy(first)
    second['retrieval_unit_id'] += ':other'
    cli.data[DEDUP]['retrieval_units'].insert(0, second)
    baseline = execute(cli, public)
    assert all([u['retrieval_unit_id'] for u in row['logical_retrieval_units']] ==
               [first['retrieval_unit_id'], second['retrieval_unit_id']] for row in baseline['results'])
    assert all(row['evidence_profile']['provenance_rank'] == 3 and row['semantic_decision'] == 'HOLD'
               for row in baseline['results'])
    protected = copy.deepcopy(cli.data)
    cli.data[DEDUP]['retrieval_units'].reverse()
    cli.data[CONCEPT]['library_edges'].reverse()
    assert execute(cli, public) == baseline
    assert cli.data[CONCEPT]['library_edges'] == list(reversed(protected[CONCEPT]['library_edges']))
    assert cli.data[DEDUP]['retrieval_units'] == list(reversed(protected[DEDUP]['retrieval_units']))


def test_negative_control_detects_removed_tie_break_after_successful_execution(cli):
    tied_fixture(cli, 'reddit', 'ACCEPTED')
    path = cli.root / 'scripts/query_ranked_v023.py'
    code = path.read_text()
    old = 'canonical_json(r.get(\'source\',{})),stable_result_identity(r),canonical_json(r)'
    assert code.count(old) == 1
    path.write_text(code.replace(old, "canonical_json(r.get('source',{}))"))
    first = execute(cli, False, QUERY, '--limit', '1')
    cli.data[CONCEPT]['reddit_edges'].reverse()
    second = execute(cli, False, QUERY, '--limit', '1')
    assert first['results'] != second['results']
