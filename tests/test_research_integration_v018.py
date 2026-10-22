"""Offline adversarial tests. All permissions/reviewers below are explicitly simulated."""
import copy
import hashlib
import json
import subprocess
import sys
from pathlib import Path

import pytest
from jsonschema import ValidationError

from scripts import research_integration_v018 as m

FIX = m.ROOT / 'tests/fixtures/research_integration_v018'


def packet_and_lock():
    data = (FIX / 'prism-synthetic.json').read_bytes()
    return data, json.loads((FIX / 'lock-synthetic.json').read_text())


def repin(packet, lock):
    """Test trust boundary: checksums change only when test explicitly repins."""
    for name, rows in packet['collections'].items():
        packet['table_contracts'][name].update(row_count=len(rows), sha256=m.digest(rows))
    data = m.canonical(packet)
    lock.update(packet_sha256=hashlib.sha256(data).hexdigest(), table_contracts=copy.deepcopy(packet['table_contracts']))
    return data, lock


def sample(approved=False):
    d = m.adapt(*packet_and_lock())
    d['fixture_kind'] = 'SYNTHETIC'
    for source in d['sources']:
        source['visibility'] = 'public'
        for restriction in source['observations'][-1]['restrictions']:
            restriction.update(status='cleared_for_scope', scope='Synthetic fixture only')
    review = d['reviews'][0]
    review['source_bindings'] = m.bindings(d)
    if approved:
        review.update(state='SIMULATED_REVIEW', reviewer='SIMULATED_NOT_A_HUMAN')
        review['disclosures'] = [dict(source_id=s['source_id'], observation_sha256=m.digest(s['observations'][-1]),
                                     scope='LINK_METADATA_ONLY', decision='ALLOW_METADATA_ONLY') for s in d['sources']]
    return d


def approve_current(d):
    prev = d['reviews'][-1]
    review = copy.deepcopy(prev)
    review.update(review_id='SYNTHETIC-REVIEW-2', supersedes=prev['review_id'], recorded_at='2026-10-22',
                  source_bindings=m.bindings(d))
    review['disclosures'] = [dict(source_id=s['source_id'], observation_sha256=m.digest(s['observations'][-1]),
                                scope='LINK_METADATA_ONLY', decision='ALLOW_METADATA_ONLY') for s in d['sources']]
    d['reviews'].append(review)


def test_native_adapter_preserves_ids_scope_and_no_human_review():
    d = m.adapt(*packet_and_lock())
    assert [s['source_id'] for s in d['sources']] == ['https://example.invalid/primary', 'SYNTHETIC-COMMUNITY']
    assert d['sources'][0]['observations'][0]['retrieved_at'] is None
    assert d['sources'][1]['observations'][0]['upstream_assessment_id'] == 1
    assert d['reviews'][0]['reviewer'] is None
    assert set(d['reviews'][0]['perspectives']) == set(m.PERSPECTIVES)
    assert m.project(d)['status'] == 'HOLD'


def test_repeat_runs_identical():
    assert m.canonical(m.project(sample(True))) == m.canonical(m.project(sample(True)))


def test_correction_propagates_with_history_and_invalidates_old_approval():
    d = sample(True)
    before = m.project(d)
    o = copy.deepcopy(d['sources'][0]['observations'][-1])
    o.update(observation_id='SYNTHETIC-CORRECTION-2', supersedes=o['observation_id'],
             observed_at='2026-10-22', url='https://example.invalid/primary-corrected',
             correction_reason='SYNTHETIC locator correction, no evidence change')
    d['sources'][0]['observations'].append(o)
    assert m.project(d)['status'] == 'HOLD'
    approve_current(d)
    after = m.project(d)
    primary = next(s for s in after['sources'] if s['kind'] == 'primary_research')
    assert primary['source_id'] == 'https://example.invalid/primary'
    assert primary['current_url'].endswith('primary-corrected')
    assert len(primary['corrections']) == 2
    assert primary['corrections'][0]['observed_at'] == '2026-10-20'
    assert primary['evidence_status'] == 'unassessed'
    assert after['question_status'] == before['question_status'] == 'UNRESOLVED'
    assert not any(after['promotion_guards'].values())


@pytest.mark.parametrize('category', sorted(m.CATEGORIES))
@pytest.mark.parametrize('status', ['unknown', 'hold', 'denied'])
def test_each_restriction_fails_closed(category, status):
    d = sample(True)
    source = d['sources'][1]
    next(r for r in source['observations'][0]['restrictions'] if r['category'] == category)['status'] = status
    # Even a freshly bound reviewer cannot override an upstream restriction.
    d['reviews'][0]['source_bindings'] = m.bindings(d)
    assert m.project(d)['sources'] == []


@pytest.mark.parametrize('visibility', ['unknown','private','restricted'])
def test_visibility_fails_closed(visibility):
    d = sample(True);d['sources'][1]['visibility'] = visibility
    assert m.project(d)['review'] is None


def test_missing_restriction_rejected():
    d = sample(True);d['sources'][1]['observations'][0]['restrictions'].pop()
    with pytest.raises(ValueError):m.project(d)


def test_missing_source_and_dangling_review_rejected():
    d = sample(True);d['sources'].pop()
    with pytest.raises((ValueError,ValidationError)):m.project(d)
    d = sample(True);d['reviews'][0]['source_bindings']['missing'] = '0'*64
    with pytest.raises(ValueError):m.project(d)


def test_duplicate_identity_rejected_url_match_does_not_merge():
    d = sample(True);d['sources'][1]['source_id'] = d['sources'][0]['source_id']
    with pytest.raises(ValueError):m.project(d)
    d = sample()
    d['sources'][1]['observations'][0]['url'] = d['sources'][0]['observations'][0]['url']
    m.validate(d)
    assert len(d['sources']) == 2 and all(s['work_family'] is None for s in d['sources'])


def test_broken_source_and_review_history_rejected():
    d = sample(True);d['sources'][0]['observations'][0]['supersedes'] = 'missing'
    with pytest.raises(ValueError):m.project(d)
    d = sample(True);d['reviews'][0]['supersedes'] = 'missing'
    with pytest.raises(ValueError):m.project(d)


def test_relationships_referential_integrity_and_no_canonical_promotion():
    d = sample(True)
    d['sources'][0]['relationships'] = [dict(target_id='missing',relation='CITES_CANDIDATE',state='NOT_ADJUDICATED')]
    with pytest.raises(ValueError):m.project(d)
    d['sources'][0]['relationships'][0].update(target_id=d['sources'][1]['source_id'],state='ACCEPTED')
    with pytest.raises(ValidationError):m.project(d)


def test_packet_tamper_and_missing_source():
    data, lock = packet_and_lock()
    with pytest.raises(ValueError):m.adapt(data+b' ',lock)
    p = json.loads(data);p['collections']['source_metadata'] = []
    data,lock=repin(p,lock)
    with pytest.raises(ValueError):m.adapt(data,lock)


@pytest.mark.parametrize('mutation', ['pk','fk','cycle','current','restrictions','context'])
def test_native_packet_integrity_even_if_test_repins(mutation):
    data,lock=packet_and_lock();p=json.loads(data);c=p['collections']
    if mutation=='pk':c['records'].append(copy.deepcopy(c['records'][0]))
    if mutation=='fk':c['assessments'][0]['record_id']='missing'
    if mutation=='cycle':c['assessments'][0]['supersedes']=1
    if mutation=='current':c['current_assessments']=[]
    if mutation=='restrictions':c['restrictions'].pop()
    if mutation=='context':c['record_context']=[]
    data,lock=repin(p,lock)
    with pytest.raises(ValueError):m.adapt(data,lock)


def test_synthetic_cannot_be_mistaken_for_real_human_review():
    d = sample(True);d['fixture_kind']='REAL_PRIVATE_INPUT'
    with pytest.raises(ValueError):m.project(d)
    d = sample();d['fixture_kind']='REAL_PRIVATE_INPUT';d['reviews'][0]['state']='HUMAN_REVIEWED'
    with pytest.raises(ValueError):m.project(d)


def test_no_free_text_or_private_sentinel_in_export():
    d=sample(True)
    for s in d['sources']:
        for o in s['observations']:
            o.update(provenance='PRIVATE_SENTINEL', access_scope='PRIVATE_SENTINEL',rationale='PRIVATE_SENTINEL',uncertainty='PRIVATE_SENTINEL')
    d['reviews'][0]['direct_evidence']=['PRIVATE_SENTINEL']
    d['reviews'][0]['reviewer']='PRIVATE_SENTINEL'
    d['reviews'][0]['source_bindings']=m.bindings(d)
    d['reviews'][0]['disclosures']=[dict(source_id=s['source_id'],observation_sha256=m.digest(s['observations'][0]),scope='LINK_METADATA_ONLY',decision='ALLOW_METADATA_ONLY') for s in d['sources']]
    assert 'PRIVATE_SENTINEL' not in json.dumps(m.project(d))
    d['sources'][1]['visibility']='private'
    out=m.project(d)
    assert out['sources']==[] and out['review'] is None
    assert 'input_sha256' not in out


@pytest.mark.parametrize('url',['https://user:password@example.invalid/a','https://example.invalid/a?secret=x','http://example.invalid/a'])
def test_sensitive_locators_rejected(url):
    d=sample();d['sources'][0]['observations'][0]['url']=url
    with pytest.raises(ValueError):m.project(d)


def test_unknown_fields_and_promotion_rejected():
    d=sample();d['posting_account']='PRIVATE_SENTINEL'
    with pytest.raises(ValidationError):m.project(d)
    d=sample();d['promotion_guards']['rights']=True
    with pytest.raises(ValidationError):m.project(d)


def test_foundation_pin_and_cli_removes_stale_output(tmp_path):
    lock=json.loads(m.LOCK.read_text());m.verify_foundations(lock)
    lock['foundation_pins']['tools/search_reddit.py']['sha256']='0'*64
    with pytest.raises(ValueError):m.verify_foundations(lock)
    source=tmp_path/'bad.json';source.write_text('{}')
    output=tmp_path/'public.json';output.write_text('STALE_ALLOWED_PREVIEW')
    run=subprocess.run([sys.executable,str(m.ROOT/'scripts/research_integration_v018.py'),'--contract',str(source),'--public-out',str(output)],capture_output=True)
    assert run.returncode != 0 and not output.exists()


def test_cli_never_overwrites_input(tmp_path):
    source=tmp_path/'input.json';source.write_text('{}')
    run=subprocess.run([sys.executable,str(m.ROOT/'scripts/research_integration_v018.py'),'--contract',str(source),'--public-out',str(source)],capture_output=True)
    assert run.returncode != 0 and source.read_text()=='{}'


def test_historical_observation_edit_invalidates_approval():
    d=json.loads((FIX/'after.json').read_text())
    assert m.project(d)['sources']
    d['sources'][0]['observations'][0]['url']='https://example.invalid/unapproved-old-url'
    assert m.project(d)['status']=='HOLD'


def test_promotion_guards_are_not_shared_between_runs():
    d=sample();d['promotion_guards']['rights']=True
    assert m.GUARDS['rights'] is False
    assert sample()['promotion_guards']['rights'] is False
    out=m.project(sample());out['promotion_guards']['rights']=True
    assert m.project(sample())['promotion_guards']['rights'] is False
