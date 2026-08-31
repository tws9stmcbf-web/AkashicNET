#!/usr/bin/env python3
"""Fail closed if README status blurs current Public Beta and sealed PRE-ALPHA release."""
from pathlib import Path
import sys

README = Path(__file__).resolve().parents[1] / "README.md"
text = README.read_text(encoding="utf-8")

required = {
    "current phase": "PUBLIC BETA",
    "sealed release": "PRE-ALPHA v0.10",
    "sealed tag": "v0.10.0-prealpha",
    "truth gate": "Truth inference: OFF",
    "rights gate": "Rights promotion: OFF",
    "scientific gate": "Scientific-evidence promotion: OFF",
}
missing = [label for label, token in required.items() if token not in text]

for forbidden in (
    "Truth inference: ON",
    "Rights promotion: ON",
    "Scientific-evidence promotion: ON",
):
    if forbidden in text:
        missing.append(f"forbidden status: {forbidden}")

if missing:
    print("Public Beta status validation FAILED:")
    for item in missing:
        print(f"- {item}")
    sys.exit(1)

print("Public Beta status validation passed: current phase and sealed release remain distinct; promotion gates remain OFF.")
