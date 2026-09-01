#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / 'references' / 'community' / 'public-knowledge-release-manifest-v0.13.json'

data = json.loads(PATH.read_text(encoding='utf-8'))
assert data['target_version'] == '0.13.0-beta.1'
assert data['release_name'] == 'Public Knowledge Beta'
assert data['manifest_state'] in {'CANDIDATE', 'SEALED'}
assert data['integration_baseline_commit'] == 'baa5e3e5b62c698b578398976ca6946dbb1e4f1e'
assert data['public_safe_counts']['registered_big_questions'] >= 1
assert data['public_safe_counts']['evidence_taxonomy_labels'] == 5
for rel in data['required_artifacts']:
    assert (ROOT / rel).is_file(), f'missing manifest artifact: {rel}'
if data['manifest_state'] == 'SEALED':
    commit = data['validated_release_commit']
    assert isinstance(commit, str) and len(commit) == 40 and all(c in '0123456789abcdef' for c in commit)
else:
    assert data['validated_release_commit'] is None
assert 'never silently retarget' in data['seal_rule']
assert 'private Drive' in data['privacy_rule']
print('PUBLIC KNOWLEDGE RELEASE MANIFEST v0.13 PASS:', data['manifest_state'])
