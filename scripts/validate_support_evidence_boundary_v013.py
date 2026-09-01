#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / 'references' / 'community' / 'support-evidence-boundary-v0.13.json'

data = json.loads(PATH.read_text(encoding='utf-8'))
policy = data['policy']
assert policy['public_knowledge_remains_freely_accessible'] is True
assert policy['support_is_voluntary'] is True
for key in [
    'support_purchases_scientific_certainty',
    'support_purchases_privileged_conclusions',
    'support_may_influence_evidence_classification',
    'support_may_influence_confidence',
    'support_may_override_provenance',
]:
    assert policy[key] is False, f'{key} must remain false'
assert policy['fund_the_question_not_the_answer'] is True
assert 'not evidence' in data['evidence_boundary'].lower()
print('SUPPORT/EVIDENCE BOUNDARY v0.13 PASS')
