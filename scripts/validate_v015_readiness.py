#!/usr/bin/env python3
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECKS = [
    ("v0.14 sealed readiness", ["python", "scripts/validate_automation_reproducibility_beta_v014.py"]),
    ("release ledger through v0.15", ["python", "scripts/validate_release_ledger_v014.py"]),
    ("v0.14 release reconstruction", ["python", "scripts/validate_release_readiness_reconstruction_v014.py"]),
    ("v0.15 observability contract", ["python", "scripts/validate_public_observability_contract_v015.py"]),
    ("v0.15 infrastructure contract", ["python", "scripts/validate_public_infrastructure_observability_v015.py"]),
    ("v0.15 public status consistency", ["python", "scripts/validate_public_status_consistency_v015.py"]),
    ("public data boundary", ["python", "scripts/check_public_data_boundary.py"]),
    ("v0.14 source coverage", ["python", "scripts/validate_source_coverage_v014.py"]),
    ("v0.13 link integrity", ["python", "scripts/validate_public_knowledge_link_integrity_v013.py"]),
    ("immutable GitHub Actions refs", ["python", "scripts/validate_actions_immutable_refs.py"]),
]

failed = []
for name, command in CHECKS:
    print(f"\n=== {name} ===", flush=True)
    result = subprocess.run(command, cwd=ROOT)
    if result.returncode != 0:
        failed.append(name)

if failed:
    print("\nFAIL: v0.15 readiness failed closed:")
    for name in failed:
        print(f" - {name}")
    sys.exit(1)

print("\nPASS: repository-side v0.15 readiness gates are green")
print("NOTE: this does not prove live AkashicNET.org deployment alignment; live-site verification remains a separate seal prerequisite.")
