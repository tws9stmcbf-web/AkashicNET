import importlib.util
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'scripts' / 'validate_big_question_architecture_v01.py'
spec = importlib.util.spec_from_file_location('big_question_architecture_v01', SCRIPT)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def make_batch_tree(tmp_path: Path):
    canonical = tmp_path / 'references' / 'big-questions' / 'BQ001'
    canonical.mkdir(parents=True)
    batch1 = canonical / 'evidence-batch1-v0.1.json'
    batch1.write_text('{}', encoding='utf-8')
    registered = ['references/big-questions/BQ001/evidence-batch1-v0.1.json']
    return canonical, registered


def test_current_big_question_architecture_passes():
    assert mod.main() == 0


def test_exact_canonical_batch_registry_passes(tmp_path):
    canonical, registered = make_batch_tree(tmp_path)
    mod.assert_canonical_batch_registry('BQ001', canonical, registered, tmp_path)


def test_unregistered_canonical_batch_fails_closed(tmp_path):
    canonical, registered = make_batch_tree(tmp_path)
    (canonical / 'evidence-batch2-v0.1.json').write_text('{}', encoding='utf-8')
    with pytest.raises(AssertionError, match='registry drift'):
        mod.assert_canonical_batch_registry('BQ001', canonical, registered, tmp_path)


def test_registered_but_missing_canonical_batch_fails_closed(tmp_path):
    canonical, registered = make_batch_tree(tmp_path)
    registered.append('references/big-questions/BQ001/evidence-batch2-v0.1.json')
    with pytest.raises(AssertionError, match='registry drift'):
        mod.assert_canonical_batch_registry('BQ001', canonical, registered, tmp_path)


def test_non_evidence_artifacts_do_not_count_as_batches(tmp_path):
    canonical, registered = make_batch_tree(tmp_path)
    (canonical / 'PUBLIC_SYNTHESIS.md').write_text('UNRESOLVED', encoding='utf-8')
    (canonical / 'public-synthesis-v0.1.json').write_text('{}', encoding='utf-8')
    mod.assert_canonical_batch_registry('BQ001', canonical, registered, tmp_path)


def test_unregistered_review_candidate_fails_closed(tmp_path):
    canonical = tmp_path / 'references' / 'big-questions' / 'BQ002'
    canonical.mkdir(parents=True)
    atlas = canonical / 'evidence-atlas-level5-review-candidate-v0.1.json'
    atlas.write_text(json.dumps({"status": "REVIEW_CANDIDATE"}), encoding='utf-8')
    with pytest.raises(AssertionError, match='review-artifact registry drift'):
        mod.assert_review_artifact_registry('BQ002', canonical, [], tmp_path)
