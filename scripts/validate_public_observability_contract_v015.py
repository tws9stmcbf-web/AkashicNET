#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "references/community/public-observability-contract-v0.15.json"
STATUS = ROOT / "references/community/public-status-v0.14.json"
LEDGER = ROOT / "references/community/release-ledger-v0.14.json"
V014 = "7b6cfd89de570c4b945d574dad570c37825645fe"


def fail(msg):
    raise SystemExit(f"FAIL: {msg}")

for p in (CONTRACT, STATUS, LEDGER):
    if not p.is_file():
        fail(f"missing required file: {p.relative_to(ROOT)}")

c = json.loads(CONTRACT.read_text())
s = json.loads(STATUS.read_text())
l = json.loads(LEDGER.read_text())

if c.get("target_version") != "0.15.0-beta.1": fail("wrong v0.15 target")
if c.get("status") != "IN_DEVELOPMENT": fail("v0.15 must remain IN_DEVELOPMENT")
base = c.get("baseline", {})
if base.get("validated_release_commit") != V014 or base.get("retarget_allowed") is not False:
    fail("v0.14 immutable baseline not preserved")
if s.get("validated_release_commit") != V014 or s.get("state") != "SEALED":
    fail("canonical public status does not preserve sealed v0.14")
r14 = next((r for r in l.get("releases", []) if r.get("version") == "0.14.0-beta.1"), None)
if not r14 or r14.get("validated_release_commit") != V014 or r14.get("retargetable") is not False:
    fail("release ledger does not preserve immutable v0.14")

t = c.get("telemetry_policy", {})
for key in ["privacy_first", "analytics_are_operational_telemetry_only"]:
    if t.get(key) is not True: fail(f"telemetry requirement not true: {key}")
for key in ["invasive_tracking_required", "cross_site_tracking_allowed", "fingerprinting_allowed", "duplicate_beacons_allowed", "analytics_are_evidence"]:
    if t.get(key) is not False: fail(f"telemetry boundary must be false: {key}")

classes = c.get("statistic_classes", {})
for key in ["measured_analytics", "repository_derived", "structural", "verified", "estimate"]:
    if not isinstance(classes.get(key), str) or not classes[key].strip(): fail(f"missing statistic class: {key}")

req = c.get("publication_requirements", {})
for key in ["every_public_stat_has_class", "repository_counts_have_snapshot_provenance", "measured_analytics_have_observation_window", "estimates_are_labelled", "structural_counts_do_not_imply_verification"]:
    if req.get(key) is not True: fail(f"publication requirement not true: {key}")
if req.get("unavailable_or_changed_means_false") is not False:
    fail("source availability must not be treated as truth")

inv = c.get("invariants", {})
for key, value in inv.items():
    if value is not False: fail(f"invariant must remain false: {key}")

print("PASS: v0.15 public observability/statistics contract is privacy-first and fail-closed")
