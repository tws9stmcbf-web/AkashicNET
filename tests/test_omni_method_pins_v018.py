"""Adversarial checks for the provenance lock; no network or human review."""
import copy
import hashlib
import json
from pathlib import Path
import shutil
import subprocess

import pytest

from scripts import verify_omni_method_pins_v018 as v


@pytest.fixture
def workspace(tmp_path):
    """Copy only the bounded verification inputs, never private packet bytes."""
    lock = json.loads((v.ROOT / v.LOCK_PATH).read_bytes())
    manifest = json.loads((v.ROOT / v.MANIFEST_PATH).read_bytes())
    paths = [v.LOCK_PATH, v.MANIFEST_PATH, 'scripts/research_integration_v018.py']
    paths.extend(p['bundled_path'] for p in manifest['http_assets'] if p.get('bundled_path'))
    for relative in paths:
        target = tmp_path / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(v.ROOT / relative, target)
    return tmp_path, lock, manifest


def repin(root, lock, manifest):
    """Model an authored lock change, so content-level boundaries are exercised."""
    raw = (json.dumps(manifest, indent=2, ensure_ascii=False) + '\n').encode()
    (root / v.MANIFEST_PATH).write_bytes(raw)
    lock['manual_method']['provenance_manifest']['sha256'] = hashlib.sha256(raw).hexdigest()
    (root / v.LOCK_PATH).write_text(json.dumps(lock))


def test_offline_verification_does_not_claim_external_reinspection():
    result = v.verify_repository()
    assert result['bundled_http_bodies_verified'] == 4
    assert result['http_descriptors'] == 11
    assert result['external_http_bodies_verified'] == result['sites_source_blobs_verified'] == 0
    assert result['component_bundles_complete'] is result['method_pin_gate_complete'] is False
    assert result['real_pilot_status'] == 'HOLD'
    assert result['question_status'] == 'UNRESOLVED'


def test_changed_manifest_fails_lock(workspace):
    root, _, _ = workspace
    with (root / v.MANIFEST_PATH).open('ab') as f:
        f.write(b' ')
    with pytest.raises(ValueError, match='manifest checksum'):
        v.verify_repository(root)


def test_changed_original_html_fails_hash(workspace):
    root, _, manifest = workspace
    path = root / manifest['http_assets'][0]['bundled_path']
    raw = path.read_bytes()
    path.write_bytes(raw.replace(b'v0.5.0', b'v0.9.9', 1))
    with pytest.raises(ValueError, match='SHA-256'):
        v.verify_repository(root)


def test_missing_bundled_asset_fails(workspace):
    root, _, manifest = workspace
    (root / next(a['bundled_path'] for a in manifest['http_assets'] if a['id'] == 'gap-card')).unlink()
    with pytest.raises(FileNotFoundError):
        v.verify_repository(root)


@pytest.mark.parametrize('field', ['components_individually_pinned', 'method_pin_gate_complete'])
def test_partial_inventory_cannot_clear_method_gate(workspace, field):
    root, lock, manifest = workspace
    manifest['gates'][field] = True
    repin(root, lock, manifest)
    with pytest.raises(ValueError, match='incomplete method gate'):
        v.verify_repository(root)


def test_registry_locator_cannot_drift_from_original_html(workspace):
    root, lock, manifest = workspace
    manifest['component_register'][0]['references'][1]['url'] += 'changed'
    repin(root, lock, manifest)
    with pytest.raises(ValueError, match='version/locator'):
        v.verify_repository(root)


def test_registry_version_cannot_drift_from_original_html(workspace):
    root, lock, manifest = workspace
    manifest['component_register'][0]['references'][0]['version_label'] = 'v3.0'
    repin(root, lock, manifest)
    with pytest.raises(ValueError, match='version/locator'):
        v.verify_repository(root)


def test_uninspected_addendum_cannot_acquire_checksum(workspace):
    root, lock, manifest = workspace
    manifest['component_register'][0]['references'][0]['original_bytes_sha256'] = 'a' * 64
    repin(root, lock, manifest)
    with pytest.raises(ValueError, match='unverified component promoted'):
        v.verify_repository(root)


def test_shared_addendum_remains_one_locator():
    manifest = json.loads((v.ROOT / v.MANIFEST_PATH).read_bytes())
    refs = [r['url'] for c in manifest['component_register'] for r in c['references']]
    assert len(refs) == 14 and len(set(refs)) == 13
    actc = next(c for c in manifest['component_register'] if c['component'] == 'ACTC')
    pp = next(c for c in manifest['component_register'] if c['component'] == 'PP')
    assert actc['references'][1]['url'] == pp['references'][1]['url']


@pytest.mark.parametrize('field,value', [('question_status', 'RESOLVED'), ('real_pilot_status', 'PASS')])
def test_provenance_cannot_promote_research_outcome(workspace, field, value):
    root, lock, manifest = workspace
    manifest['gates'][field] = value
    repin(root, lock, manifest)
    with pytest.raises(ValueError, match='review/release boundary'):
        v.verify_repository(root)


def test_capture_path_cannot_escape_supplied_directory(workspace, tmp_path):
    root, lock, manifest = workspace
    manifest['http_assets'][0]['capture_filename'] = '../outside.html'
    repin(root, lock, manifest)
    with pytest.raises(ValueError, match='outside supplied root'):
        v.verify_repository(root, capture_directory=tmp_path)


def test_source_verification_uses_immutable_commit_not_head(tmp_path):
    root = tmp_path / 'source'
    root.mkdir()
    def git(*args):
        return subprocess.check_output(['git', *args], cwd=root, stderr=subprocess.DEVNULL).decode().strip()
    git('init')
    git('config', 'user.name', 'Synthetic fixture')
    git('config', 'user.email', 'fixture@example.invalid')
    raw = b'SYNTHETIC METHOD REVISION ONE\n'
    (root / 'method.txt').write_bytes(raw)
    git('add', 'method.txt')
    git('commit', '-m', 'synthetic baseline')
    first = git('rev-parse', 'HEAD')
    (root / 'method.txt').write_bytes(b'SYNTHETIC METHOD REVISION TWO\n')
    git('commit', '-am', 'synthetic later revision')
    pin = {'path': 'method.txt', 'size_bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest(),
           'git_blob_sha': hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()}
    manifest = {'source_provenance': {'commit_sha': first}, 'source_pins': [pin]}
    assert v.verify_source_checkout(root, manifest) == 1
    manifest['source_provenance']['commit_sha'] = git('rev-parse', 'HEAD')
    with pytest.raises(ValueError):
        v.verify_source_checkout(root, manifest)
