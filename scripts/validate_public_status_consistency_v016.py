#!/usr/bin/env python3
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HOME = ROOT / "website/app/page.tsx"
PROGRESS = ROOT / "website/app/development-progress/page.tsx"
PUBLIC_APP = ROOT / "website/app"


def fail(message: str) -> None:
    raise SystemExit(f"FAIL: {message}")


for path in (HOME, PROGRESS):
    if not path.is_file():
        fail(f"missing required surface: {path.relative_to(ROOT)}")

home = HOME.read_text()
progress = PROGRESS.read_text()

for token in (
    "v0.15",
    "SEALED BASELINE",
    "v0.16.0-beta.2",
    "GOVERNED CANDIDATE",
    "v0.16.7",
    "SITE CHECKPOINT",
    "BQ001 remains UNRESOLVED",
):
    if token not in progress:
        fail(f"development record missing governed status token: {token}")

for token in (
    "Public Beta",
    "v0.15 sealed",
    "v0.16.0-beta.2 governed candidate",
    "v0.14.0-beta.1",
    "Automation & Reproducibility Beta",
    "READY / SEALED",
    "2 September 2026",
    "Historical sealed release checkpoint",
):
    if token not in home:
        fail(f"homepage missing required current-or-historical token: {token}")

# Inspect text across inline JSX tags, while keeping separate source lines apart.
# This is a bounded status-copy guard, not a general JSX or natural-language parser.
def status_text(source: str) -> str:
    return re.sub(r"<[^>]*>", " ", source)


product_status = re.compile(
    r"\bAkashicNET\b"
    r"(?:[ \t·:–—-]+(?:engine|product|is|release|status|version|current))*"
    r"[ \t·:–—-]*(?:Pre-alpha|Public Beta|v\d+\.\d+(?:\.\d+)?(?:-[\w.]+)?)\b|"
    r"(?:Pre-alpha|Public Beta)[ \t·:–—-]*AkashicNET\b",
    re.IGNORECASE,
)
pre_alpha = re.compile(
    r"\bAkashicNET[^\n<]{0,40}Pre-alpha|"
    r"Pre-alpha[^\n<]{0,40}AkashicNET\b",
    re.IGNORECASE,
)
allowed_product_status_surfaces = {HOME.resolve(), PROGRESS.resolve()}
for surface in PUBLIC_APP.rglob("*.tsx"):
    visible = status_text(surface.read_text())
    if pre_alpha.search(visible):
        fail(f"contradictory current Pre-alpha status: {surface.relative_to(ROOT)}")
    if surface.resolve() not in allowed_product_status_surfaces:
        if product_status.search(visible):
            fail(
                "product status must remain centralised on the homepage checkpoint "
                f"and development record: {surface.relative_to(ROOT)}"
            )

# The homepage has one linked current-product label; the sealed snapshot is historical.
links = re.findall(r'<a\b[^>]*href="/development-progress"[^>]*>(.*?)</a>', home, re.S)
current_label = "Public Beta · v0.15 sealed · v0.16.0-beta.2 governed candidate"
if len(links) != 1 or current_label not in status_text(links[0]):
    fail("homepage must have one linked current-product checkpoint")
if (home.count("Public Beta") != 1 or home.count("v0.16.0-beta.2") != 1
        or "v0.16.7" in home):
    fail("duplicate current-product homepage status")

# Enforce status and limitation together in the governed checkpoint records.
for version, status, limitation in (
    ("v0.16.0-beta.2", "GOVERNED CANDIDATE", "not a sealed release"),
    ("v0.16.7", "SITE CHECKPOINT", "not a release"),
):
    record = re.search(
        r'\["' + re.escape(version) + r'",\s*"' + status + r'",\s*"([^"\n]+)"\]',
        progress,
    )
    if not record or limitation not in record.group(1):
        fail(f"missing candidate/checkpoint limitation: {version}")
if "progress toward v0.17.0" not in status_text(progress):
    fail("site checkpoint must describe progress toward v0.17.0")

# Reject affirmative release claims even when the correct disclaimers also survive.
release_claim = re.compile(
    r"v0\.16\.(?:0-beta\.2|7)\b[ \t]*(?:"
    r"(?:is[ \t]+)?(?:a[ \t]+)?sealed(?:[ \t]+release)?|"
    r"released|READY[ \t]*/[ \t]*SEALED|"
    r"is[ \t]+(?:the[ \t]+)?(?:current[ \t]+)?release"
    r")\b|"
    r"(?:sealed[ \t]+release|released)[ \t·:–—-]*v0\.16\.(?:0-beta\.2|7)\b",
    re.IGNORECASE,
)
if release_claim.search(status_text(home + "\n" + progress)):
    fail("unsealed candidate or site checkpoint presented as a release")

bq001_resolved = re.compile(
    r"\bBQ001\b[ \t·:–—-]*(?:is[ \t]+|status[ \t·:–—-]*)?RESOLVED\b",
    re.IGNORECASE,
)
if bq001_resolved.search(status_text(home + "\n" + progress)):
    fail("public status surface contradicts BQ001 UNRESOLVED")

for forbidden in (
    "truth inference enabled",
    "scientifically confirmed",
    "canonical public integration complete",
):
    if forbidden.lower() in (home + "\n" + progress).lower():
        fail(f"public status surface contains forbidden promotion: {forbidden}")

print(
    "PASS: v0.16 public status is centralised; sealed v0.15 assertions and "
    "BQ001/no-promotion boundaries remain explicit"
)
