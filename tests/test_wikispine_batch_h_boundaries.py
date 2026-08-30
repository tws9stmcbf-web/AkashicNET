import copy
import importlib.util
import json
from pathlib import Path
import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'scripts' / 'validate_wikispine_batch_h_boundaries.py'
spec = importlib.util.spec_from_file_location('wikispine_h', SCRIPT)
wikispine_h = importlib.util.module_from_spec(spec)
spec.loader.exec_module(wikispine_h)
PAYLOAD = json.loads((ROOT / 'references' / 'community' / 'wikispine-batch-h-works-v0.7.7.json').read_text(encoding='utf-8'))


def test_current_batch_passes_even_with_no_pending_records():
    assert wikispine_h.validate(PAYLOAD)


@pytest.mark.parametrize('key,value', [
    ('candidate_edges_default', 'ACCEPT'),
    ('arbitrary_recursive_crawl', True),
    ('full_article_body_ingestion_default', True),
    ('rights_promotion_allowed', True),
    ('scientific_evidence_promotion_allowed', True),
    ('truth_inference_allowed', True),
    ('drive_access_performed', True),
])
def test_guardrail_mutations_fail_closed(key, value):
    payload = copy.deepcopy(PAYLOAD)
    payload['guardrails'][key] = value
    with pytest.raises(AssertionError):
        wikispine_h.validate(payload)


def pending_payload():
    payload = copy.deepcopy(PAYLOAD)
    payload['pending_records'] = [{
        'akashic_entity': 'Unverified Work',
        'entity_type': 'WORK',
        'resolution_state': 'PENDING_VERIFIED_QID',
        'reason': 'No independently verified QID yet',
    }]
    return payload


def test_explicit_pending_record_is_allowed_without_qid():
    assert wikispine_h.validate(pending_payload())


def test_pending_qid_cannot_be_invented():
    payload = pending_payload()
    payload['pending_records'][0]['wikidata_qid'] = 'Q999999999'
    with pytest.raises(AssertionError):
        wikispine_h.validate(payload)


def test_pending_work_cannot_be_silently_promoted():
    payload = pending_payload()
    payload['pending_records'][0]['resolution_state'] = 'RESOLVED_HIGH_PRECISION'
    with pytest.raises(AssertionError):
        wikispine_h.validate(payload)


def test_resolved_work_remains_identity_only():
    payload = copy.deepcopy(PAYLOAD)
    payload['records'][0]['semantic_decision'] = 'ACCEPT'
    with pytest.raises(AssertionError):
        wikispine_h.validate(payload)
