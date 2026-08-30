import importlib.util
from pathlib import Path
import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "validate_bq001_public_status_boundary.py"
spec = importlib.util.spec_from_file_location("bq001_status", SCRIPT)
bq001_status = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bq001_status)

PAGE_TEXT = (ROOT / "website" / "app" / "big-questions" / "bq001" / "page.tsx").read_text(encoding="utf-8")


def test_current_page_passes():
    assert bq001_status.validate(PAGE_TEXT)


@pytest.mark.parametrize("required", bq001_status.REQUIRED)
def test_required_boundaries_fail_closed(required):
    mutated = PAGE_TEXT.replace(required, "REMOVED_BOUNDARY", 1)
    with pytest.raises(AssertionError):
        bq001_status.validate(mutated)


@pytest.mark.parametrize("forbidden", bq001_status.FORBIDDEN)
def test_forbidden_status_phrases_fail_closed(forbidden):
    mutated = PAGE_TEXT + f"\n{forbidden}\n"
    with pytest.raises(AssertionError):
        bq001_status.validate(mutated)


def test_unresolved_visibility_cannot_be_collapsed():
    mutated = PAGE_TEXT.replace("UNRESOLVED", "OPEN", 2)
    with pytest.raises(AssertionError):
        bq001_status.validate(mutated)
