#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "references/community/public-status-consistency-v0.15.json"
STATUS = ROOT / "references/community/public-status-v0.14.json"
LEDGER = ROOT / "references/community/release-ledger-v0.14.json"
HOME = ROOT / "website/app/page.tsx"
CHANGELOG = ROOT / "CHANGELOG.md"
HANDOFF = ROOT / "docs/V014_PUBLIC_SYNC.md"
V014 = "7b6cfd89de570c4b945d574dad570c37825645fe"


def fail(msg):
    raise SystemExit(f"FAIL: {msg}")

for p in (CONTRACT, STATUS, LEDGER, HOME, CHANGELOG, HANDOFF):
    if not p.is_file():
        fail(f"missing required surface: {p.relative_to(ROOT)}")

c = json.loads(CONTRACT.read_text())
s = json.loads(STATUS.read_text())
l = json.loads(LEDGER.read_text())
home = HOME.read_text()
changelog = CHANGELOG.read_text()
handoff = HANDOFF.read_text()

if c.get("target_version") != "0.15.0-beta.1" or c.get("status") != "IN_DEVELOPMENT":
    fail("v0.15 consistency contract state invalid")
canon = c.get("canonical_current_release", {})
if canon.get("version") != "0.14.0-beta.1" or canon.get("validated_release_commit") != V014:
    fail("canonical v0.14 release changed")
if s.get("version") != canon.get("version") or s.get("state") != "SEALED" or s.get("validated_release_commit") != V014:
    fail("public-status record disagrees with canonical release")
r14 = next((r for r in l.get("releases", []) if r.get("version") == "0.14.0-beta.1"), None)
if not r14 or r14.get("validated_release_commit") != V014 or r14.get("retargetable") is not False:
    fail("release ledger does not preserve immutable v0.14")

for needle in c.get("homepage_requirements", {}).get("must_contain", []):
    if needle not in home:
        fail(f"homepage snapshot missing current status token: {needle}")
for needle in c.get("homepage_requirements", {}).get("must_not_present_as_current", []):
    if needle in home:
        fail(f"homepage snapshot still presents stale current status: {needle}")

for needle in ["v0.14.0-beta.1", "Automation & Reproducibility Beta", "2026-09-02"]:
    if needle not in changelog:
        fail(f"changelog missing v0.14 release token: {needle}")
for needle in ["v0.14.0-beta.1", "AUTOMATION & REPRODUCIBILITY BETA", "READY / SEALED", V014]:
    if needle not in handoff:
        fail(f"public handoff missing release token: {needle}")

live = c.get("live_surface_verification", {})
if live.get("state") != "REQUIRED_BEFORE_V015_SEAL" or live.get("repository_snapshot_is_not_live_deployment_proof") is not True:
    fail("live-site verification boundary weakened")

inv = c.get("invariants", {})
for key, value in inv.items():
    if value is not False:
        fail(f"invariant must remain false: {key}")

print("PASS: repository-addressable public status surfaces agree on sealed v0.14; live deployment verification remains separately required")
