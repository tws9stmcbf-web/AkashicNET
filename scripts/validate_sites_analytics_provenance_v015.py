#!/usr/bin/env python3
"""Validate governed, opt-in analytics provenance without claiming deployment."""

import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROVENANCE = ROOT / "references/community/sites-analytics-provenance-v0.15.json"
TOKEN_NAME = "NEXT_PUBLIC_CLOUDFLARE_ANALYTICS_TOKEN"
SITES_SOURCE_COMMIT = "afa354735f42145e123a4e2469be6f70fd65b6a3"
VALUE = r"""(?P<value>\$\{\{.*?\}\}|\$\{[^}\r\n]+\}|"[^"\r\n]*"|'[^'\r\n]*'|[^\s#,};]+)"""
DIRECT_ASSIGNMENT = re.compile(
    rf"""(?ix)["']?{re.escape(TOKEN_NAME)}["']?\s*(?:=|:)\s*{VALUE}"""
)
DOCKER_ASSIGNMENT = re.compile(
    rf"""(?ix)^\s*(?:ENV|ARG)\s+{re.escape(TOKEN_NAME)}\s+{VALUE}"""
)
NAMED_TOKEN = re.compile(
    rf"""(?ix)["']?name["']?\s*(?:=|:)\s*["']?{re.escape(TOKEN_NAME)}["']?"""
)
VALUE_FIELD = re.compile(rf"""(?ix)["']?value["']?\s*(?:=|:)\s*{VALUE}""")
SAFE_INDIRECTION = re.compile(
    r"""(?x)^(?:
        null
        |none
        |<[^>\r\n]+>
        |\$\{\{\s*(?:secrets|vars|env)\.[A-Za-z_][A-Za-z0-9_.-]*\s*\}\}
        |\$\{[A-Za-z_][A-Za-z0-9_]*\}
        |\$[A-Za-z_][A-Za-z0-9_]*
        |\$env:[A-Za-z_][A-Za-z0-9_]*
        |(?:secret|secrets|var|vars|local|env)\.[A-Za-z_][A-Za-z0-9_.-]*
        |process\.env\.[A-Za-z_][A-Za-z0-9_]*
        |os\.environ\[[^\]\r\n]+\]
        |os\.getenv\([^\)\r\n]+\)
        |vault:[^\s]+
    )$"""
)


def fail(message: str) -> None:
    raise SystemExit(f"FAIL: {message}")


def is_safe_indirection(raw_value: str) -> bool:
    value = raw_value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        value = value[1:-1].strip()
    return not value or SAFE_INDIRECTION.fullmatch(value) is not None


if not PROVENANCE.is_file():
    fail(f"missing analytics provenance: {PROVENANCE.relative_to(ROOT)}")

record = json.loads(PROVENANCE.read_text(encoding="utf-8"))
site = record.get("canonical_site", {})
integration = record.get("integration", {})
deployment = record.get("deployment", {})
governance = record.get("governance", {})

if site.get("project_id") != "appgprj_6a93c8c170388191b89b2d90a544c0b1":
    fail("analytics provenance must identify the canonical ChatGPT Sites project")
if site.get("live_url") != "https://akashicnet.org":
    fail("analytics provenance must identify the canonical live URL")
if site.get("source_commit_sha") != SITES_SOURCE_COMMIT:
    fail("analytics provenance must pin the reviewed canonical Sites source commit")
if integration.get("activation_variable") != TOKEN_NAME:
    fail("analytics activation variable drifted")
if integration.get("runtime_configuration_state") != "ABSENT":
    fail("analytics must remain disabled until separately configured")
if integration.get("single_beacon_guard") is not True:
    fail("single-beacon ownership guard is required")
if integration.get("fail_closed") is not True:
    fail("analytics integration must fail closed")
if deployment.get("source_commit_deployed") is not False:
    fail("provenance must not claim an unperformed deployment")
if deployment.get("live_beacon_state") != "UNVERIFIED":
    fail("unverified live-beacon state must not be promoted to a claim")
if governance.get("classification") != "aggregate operational telemetry only":
    fail("analytics must remain operational telemetry")
for field in (
    "scientific_evidence",
    "truth_inference",
    "visitor_level_public_logs",
    "private_drive_promotion",
    "sealed_v0_14_baseline_modified",
):
    if governance.get(field) is not False:
        fail(f"governance invariant must remain false: {field}")

tracked = subprocess.check_output(
    ["git", "-C", str(ROOT), "ls-files", "-z"],
).split(b"\0")
violations = set()
for raw_path in tracked:
    if not raw_path:
        continue
    relative = raw_path.decode("utf-8", errors="surrogateescape")
    path = ROOT / relative
    try:
        data = path.read_bytes()
    except OSError as exc:
        fail(f"cannot inspect tracked file {relative}: {exc}")
    if b"\0" in data:
        continue

    text = data.decode("utf-8", errors="ignore")
    lines = text.splitlines()

    for match in DIRECT_ASSIGNMENT.finditer(text):
        if not is_safe_indirection(match.group("value")):
            line_number = text.count("\n", 0, match.start()) + 1
            violations.add(f"{relative}:{line_number}")

    for index, line in enumerate(lines):
        for match in DOCKER_ASSIGNMENT.finditer(line):
            if not is_safe_indirection(match.group("value")):
                violations.add(f"{relative}:{index + 1}")

        if NAMED_TOKEN.search(line):
            for offset, candidate in enumerate(lines[index:index + 5]):
                if "valueFrom" in candidate:
                    break
                for match in VALUE_FIELD.finditer(candidate):
                    if not is_safe_indirection(match.group("value")):
                        violations.add(f"{relative}:{index + offset + 1}")

if violations:
    fail(
        "possible committed analytics token value in tracked configuration: "
        + ", ".join(sorted(violations))
    )

print(
    "PASS: canonical Sites analytics provenance is fail-closed, "
    "unpromoted and free of tracked token values"
)
