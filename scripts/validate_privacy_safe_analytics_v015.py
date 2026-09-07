#!/usr/bin/env python3
"""Validate the opt-in privacy-safe analytics integration for v0.15."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMPONENT = ROOT / "website/app/components/PrivacyAnalytics.tsx"
LAYOUT = ROOT / "website/app/layout.tsx"
PRIVACY = ROOT / "website/ANALYTICS_PRIVACY.md"
WEBSITE = ROOT / "website"
TOKEN_NAME = "NEXT_PUBLIC_CLOUDFLARE_ANALYTICS_TOKEN"
BEACON_HOST = "static.cloudflareinsights.com/beacon.min.js"


def fail(message: str) -> None:
    raise SystemExit(f"FAIL: {message}")


for path in (COMPONENT, LAYOUT, PRIVACY):
    if not path.is_file():
        fail(f"missing required analytics file: {path.relative_to(ROOT)}")

component = COMPONENT.read_text(encoding="utf-8")
layout = LAYOUT.read_text(encoding="utf-8")
privacy = PRIVACY.read_text(encoding="utf-8")

if component.count(TOKEN_NAME) != 1:
    fail("analytics component must reference the opt-in environment variable exactly once")
if component.count(BEACON_HOST) != 2:
    fail("analytics component must define one beacon source and one duplicate-detection selector")
if "document.querySelector(BEACON_SELECTOR)" not in component:
    fail("analytics component must check for an existing beacon")
if 'if (!token || document.querySelector(BEACON_SELECTOR)) return;' not in component:
    fail("missing fail-closed opt-in and duplicate-beacon guard")
if layout.count('import PrivacyAnalytics from "./components/PrivacyAnalytics";') != 1:
    fail("layout must import PrivacyAnalytics exactly once")
if layout.count("<PrivacyAnalytics />") != 1:
    fail("layout must render PrivacyAnalytics exactly once")

source_files = [
    path for path in WEBSITE.rglob("*")
    if path.is_file() and path.suffix in {".js", ".jsx", ".ts", ".tsx", ".html"}
]
beacon_files = [
    path.relative_to(ROOT).as_posix()
    for path in source_files
    if BEACON_HOST in path.read_text(encoding="utf-8", errors="ignore")
]
if beacon_files != ["website/app/components/PrivacyAnalytics.tsx"]:
    fail(f"Cloudflare beacon must be owned by exactly one component: {beacon_files}")

required_privacy_phrases = [
    "operational telemetry",
    "not scientific evidence",
    "cross-site profiling",
    "Fingerprinting",
    "Visitor-level public logs",
    "Private Drive identifiers",
    "duplicate",
    "unverified",
]
for phrase in required_privacy_phrases:
    if phrase.lower() not in privacy.lower():
        fail(f"analytics privacy boundary missing: {phrase}")

for path in source_files:
    text = path.read_text(encoding="utf-8", errors="ignore")
    for line in text.splitlines():
        if TOKEN_NAME in line and "=" in line and "process.env." not in line:
            fail(f"possible committed analytics token assignment: {path.relative_to(ROOT)}")

print("PASS: v0.15 analytics integration is opt-in, single-beacon and privacy-governed")
