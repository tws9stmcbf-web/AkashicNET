import importlib.util
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "validate_insights_news_desk_v01.py"
spec = importlib.util.spec_from_file_location("insights_news_desk_v01", SCRIPT)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

PAGE = (ROOT / "website" / "app" / "insights" / "interstellar-weather-schumann-september-2026" / "page.tsx").read_text(encoding="utf-8")
COMPONENT = (ROOT / "website" / "app" / "insights" / "interstellar-weather-schumann-september-2026" / "NewsDeskTicker.tsx").read_text(encoding="utf-8")
REGISTRY = (ROOT / "website" / "app" / "insights" / "interstellar-weather-schumann-september-2026" / "newsroom.ts").read_text(encoding="utf-8")
NOW = "2026-09-14T13:18:18.794Z"


def valid_item(**overrides):
    base = {
        "headline": "Newsroom headline",
        "shortSummary": "Newsroom summary",
        "category": "Evidence Desk",
        "sourceUrl": "https://akashicnet.org/about",
        "sourceTimestamp": "2026-09-14T09:00:00Z",
        "publishedAt": "2026-09-14T10:00:00Z",
        "updatedAt": "2026-09-14T11:00:00Z",
        "evidenceLabel": "Observation",
        "status": "PUBLIC",
    }
    base.update(overrides)
    return base


def test_insights_news_desk_contract_executes():
    assert mod.validate(PAGE, COMPONENT, REGISTRY)


def test_publishable_item_within_window_passes():
    assert mod.is_publishable_newsroom_item(valid_item(), NOW)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("status", "REVIEW"),
        ("sourceUrl", "http://invalid.example"),
        ("sourceTimestamp", "not-a-date"),
        ("headline", ""),
    ],
)
def test_fail_closed_for_invalid_publication_inputs(field, value):
    assert not mod.is_publishable_newsroom_item(valid_item(**{field: value}), NOW)


def test_stale_publication_fails_closed():
    item = valid_item(
        sourceTimestamp="2026-09-13T08:00:00Z",
        publishedAt="2026-09-13T09:00:00Z",
        updatedAt="2026-09-13T10:00:00Z",
    )
    assert not mod.is_publishable_newsroom_item(item, NOW)


def test_out_of_order_timestamps_fail_closed():
    item = valid_item(sourceTimestamp="2026-09-14T12:00:00Z", publishedAt="2026-09-14T10:00:00Z")
    assert not mod.is_publishable_newsroom_item(item, NOW)


def test_future_updates_fail_closed():
    item = valid_item(updatedAt="2026-09-14T14:00:00Z")
    assert not mod.is_publishable_newsroom_item(item, NOW)


def test_canonical_13d_sequence_is_exact():
    assert mod.CANONICAL_13D == [
        "AWAKEN",
        "HIERATIC",
        "HOMESENSE",
        "ADAPT",
        "REGENERATE",
        "TRANSCEND",
        "#METAD v2.1",
        "ACTC",
        "MultidimensionalCUT · PAST",
        "MultidimensionalCUT · PRESENT",
        "MultidimensionalCUT · FUTURE",
        "UMASC",
        "AKASHICNET",
    ]
