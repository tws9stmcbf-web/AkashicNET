from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Mapping

CANONICAL_13D = [
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
WINDOW_HOURS = 24
REQUIRED_PAGE_STRINGS = [
    "AKASHICNET INSIGHTS NEWSROOM",
    "Amplitude ≠ frequency",
    "Correlation ≠ causation",
    "AkashicONE is a coherent assessment within it, not a higher evidence tier.",
]
REQUIRED_COMPONENT_STRINGS = [
    'window.matchMedia("(prefers-reduced-motion: reduce)")',
    "AKN24",
    'aria-label="AkashicNET News 24"',
    "AkashicNET News 24",
    "LATEST 24 HOURS",
    "Pause newsroom strip",
    "Play newsroom strip",
    'aria-hidden="true"',
    'onMouseEnter={() => setIsInteracting(true)}',
    'onFocusCapture={() => setIsInteracting(true)}',
    'Kindness Across Species',
    'Habitat Restored',
    'Wildlife Rescued',
    'Communities Cooperating',
    'BQ001 remains UNRESOLVED',
    'AkashicONE is a coherent assessment within it, not a higher evidence tier.',
]
REQUIRED_REGISTRY_STRINGS = [
    '"Global Challenges"',
    '"AI & Technology"',
    '"Earth-Space Weather"',
    '"Evidence Desk"',
    '"Kindness Across Species"',
    'status !== "PUBLIC"',
    'publishedMs < windowStart || updatedMs < windowStart',
]
REQUIRED_ITEM_FIELDS = [
    "headline",
    "shortSummary",
    "category",
    "sourceUrl",
    "sourceTimestamp",
    "publishedAt",
    "updatedAt",
    "evidenceLabel",
    "status",
]


def parse_utc(value: str) -> datetime | None:
    if not isinstance(value, str) or not value.endswith("Z"):
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(timezone.utc)
    except ValueError:
        return None


def is_public_https_url(value: str) -> bool:
    return isinstance(value, str) and value.startswith("https://") and "." in value.split("//", 1)[1]


def is_publishable_newsroom_item(item: Mapping[str, str], now_timestamp: str) -> bool:
    if item.get("status") != "PUBLIC":
        return False
    if any(not item.get(field, "").strip() for field in REQUIRED_ITEM_FIELDS):
        return False
    if not is_public_https_url(item["sourceUrl"]):
        return False

    source = parse_utc(item["sourceTimestamp"])
    published = parse_utc(item["publishedAt"])
    updated = parse_utc(item["updatedAt"])
    now = parse_utc(now_timestamp)
    if not all([source, published, updated, now]):
        return False
    if source > published or published > updated or updated > now:
        return False

    window_start = now - timedelta(hours=WINDOW_HOURS)
    return published >= window_start and updated >= window_start


def validate(page_text: str, component_text: str, registry_text: str) -> bool:
    for required in REQUIRED_PAGE_STRINGS:
        assert required in page_text, f"missing page boundary: {required}"
    for required in REQUIRED_COMPONENT_STRINGS:
        assert required in component_text, f"missing component boundary: {required}"
    for required in REQUIRED_REGISTRY_STRINGS:
        assert required in registry_text, f"missing registry contract: {required}"
    assert "aria-live" not in component_text, "news ticker must not use aria-live"

    start = registry_text.index("export const CANONICAL_13D_SEQUENCE = [")
    end = registry_text.index("] as const;", start)
    block = registry_text[start:end]
    extracted = [line.strip().strip('",') for line in block.splitlines()[1:] if '"' in line]
    assert extracted == CANONICAL_13D, "canonical 13D labels must remain exact"

    for field in REQUIRED_ITEM_FIELDS:
        assert f"readonly {field}:" in registry_text, f"missing typed newsroom field: {field}"

    return True
