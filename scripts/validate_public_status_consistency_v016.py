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

allowed_product_status_surfaces = {HOME.resolve(), PROGRESS.resolve()}
product_status = re.compile(
    r"AkashicNET[^\\n<]{0,40}(?:Pre-alpha|Public Beta)|"
    r"(?:Pre-alpha|Public Beta)[^\\n<]{0,40}AkashicNET",
    re.IGNORECASE,
)
for surface in PUBLIC_APP.rglob("*.tsx"):
    if surface.resolve() in allowed_product_status_surfaces:
        continue
    if product_status.search(surface.read_text()):
        fail(
            "product status must remain centralised on the homepage checkpoint "
            f"and development record: {surface.relative_to(ROOT)}"
        )

for forbidden in (
    "BQ001 · RESOLVED",
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
