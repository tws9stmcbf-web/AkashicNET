import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "check_public_data_boundary.py"
spec = importlib.util.spec_from_file_location("public_data_boundary", SCRIPT)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def assert_rejected(name: str, text: str | None):
    violations = mod.validate_entry(name, text)
    assert violations, f"expected privacy boundary rejection for {name}"


def test_current_repository_boundary_passes():
    assert mod.main() == 0


def test_private_tracked_path_fails_closed_even_without_text():
    assert_rejected("references/community/canonical-review-queue-private.csv", None)


def test_generated_drive_graph_path_fails_closed_even_without_text():
    assert_rejected("data/knowledge-graph-v0.7.json", None)


def test_live_drive_url_fails_closed():
    synthetic_id = "A" * 24
    assert_rejected(
        "references/community/synthetic.json",
        f'{{"source":"https://drive.google.com/file/d/{synthetic_id}/view"}}',
    )


def test_embedded_drive_object_id_fails_closed():
    synthetic_id = "B" * 24
    assert_rejected(
        "references/community/synthetic.md",
        f"synthetic marker drive:file:{synthetic_id}",
    )


def test_sensitive_csv_column_fails_closed():
    assert_rejected(
        "references/community/synthetic.csv",
        "title,drive_object_id\nExample,SYNTHETIC_ONLY\n",
    )


def test_drive_derived_master_index_row_fails_closed():
    assert_rejected(
        "references/community/akashic-master-index.csv",
        "title,source\nSynthetic,Google Drive\n",
    )


def test_privacy_safe_aggregate_passes():
    assert mod.validate_entry(
        "references/community/synthetic-safe-aggregate.json",
        '{"families":5,"objects":10,"private_object_identifiers_published":false}',
    ) == []
