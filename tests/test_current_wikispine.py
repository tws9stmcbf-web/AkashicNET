import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "validate_current_wikispine.py"
spec = importlib.util.spec_from_file_location("current_wikispine", SCRIPT)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def write_aggregate(directory: Path, version: str):
    path = directory / f"wikispine-entity-aggregate-v{version}.json"
    path.write_text(json.dumps({"version": version}), encoding="utf-8")
    return path


def test_repository_resolves_current_wikispine_v0718():
    aggregate, validator, version = mod.resolve_current()
    assert version == (0, 7, 18)
    assert aggregate.name == "wikispine-entity-aggregate-v0.7.18.json"
    assert validator.name == "validate_wikispine_v0718.py"


def test_semantic_version_selection_beats_lexical_order(tmp_path):
    write_aggregate(tmp_path, "0.7.9")
    latest = write_aggregate(tmp_path, "0.7.18")
    assert mod.latest_aggregate(tmp_path) == latest


def test_missing_matching_validator_fails_closed(tmp_path):
    aggregates = tmp_path / "community"
    scripts = tmp_path / "scripts"
    aggregates.mkdir()
    scripts.mkdir()
    write_aggregate(aggregates, "0.7.99")
    try:
        mod.resolve_current(aggregates, scripts)
    except ValueError as exc:
        assert "lacks matching validator" in str(exc)
    else:
        raise AssertionError("expected missing current WikiSpine validator to fail closed")


def test_filename_content_version_mismatch_fails_closed(tmp_path):
    aggregates = tmp_path / "community"
    scripts = tmp_path / "scripts"
    aggregates.mkdir()
    scripts.mkdir()
    path = aggregates / "wikispine-entity-aggregate-v0.7.20.json"
    path.write_text(json.dumps({"version": "0.7.19"}), encoding="utf-8")
    (scripts / "validate_wikispine_v0720.py").write_text("", encoding="utf-8")
    try:
        mod.resolve_current(aggregates, scripts)
    except ValueError as exc:
        assert "filename/content version mismatch" in str(exc)
    else:
        raise AssertionError("expected aggregate filename/content mismatch to fail closed")


def test_validator_filename_mapping():
    assert mod.validator_name((0, 7, 18)) == "validate_wikispine_v0718.py"
    assert mod.validator_name((1, 2, 3)) == "validate_wikispine_v1203.py"
