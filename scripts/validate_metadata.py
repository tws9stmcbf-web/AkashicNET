#!/usr/bin/env python3
"""Lightweight metadata/frontmatter validator for experiments.

Checks:
- `experiments/citizen-science-protocol-template.md` contains YAML frontmatter with required keys
- Each file under `experiments/mappings/` contains frontmatter with required mapping keys
- `experiments/visual-provenance-template.md` contains frontmatter with `visual_id`

Exit code 0 on success, 1 on failure.
"""
import sys
import re
from pathlib import Path
import yaml


def read_frontmatter(path: Path):
    text = path.read_text(encoding="utf8")
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        return None
    try:
        return yaml.safe_load(m.group(1))
    except Exception:
        return None


def check_protocol_template(path: Path):
    fm = read_frontmatter(path)
    if not fm:
        print(f"Missing or invalid frontmatter in {path}")
        return False
    required = ["id", "title", "authors", "year", "status", "preregistered", "data_path", "evidence_rationale"]
    missing = [k for k in required if k not in fm]
    if missing:
        print(f"{path}: missing keys: {missing}")
        return False
    return True


def check_mappings(dirpath: Path):
    ok = True
    if not dirpath.exists():
        print(f"Mappings directory {dirpath} does not exist; skipping")
        return ok
    for p in dirpath.glob("*.md"):
        fm = read_frontmatter(p)
        if not fm:
            print(f"Missing frontmatter in mapping {p}")
            ok = False
            continue
        required = ["concept_id", "layer", "proposition"]
        missing = [k for k in required if k not in fm]
        if missing:
            print(f"{p}: missing mapping keys: {missing}")
            ok = False
    return ok


def check_visual_provenance(path: Path):
    fm = read_frontmatter(path)
    if not fm:
        print(f"Missing frontmatter in visual provenance template {path}")
        return False
    if "visual_id" not in fm:
        print(f"visual provenance template {path} missing 'visual_id'")
        return False
    return True


def main():
    repo = Path(__file__).resolve().parents[1]
    ok = True
    tpl = repo / "experiments" / "citizen-science-protocol-template.md"
    if tpl.exists():
        ok = check_protocol_template(tpl) and ok
    else:
        print(f"Template {tpl} not found")
        ok = False

    ok = check_mappings(repo / "experiments" / "mappings") and ok
    ok = check_visual_provenance(repo / "experiments" / "visual-provenance-template.md") and ok

    if not ok:
        print("Metadata validation failed")
        sys.exit(1)
    print("Metadata validation passed")


if __name__ == "__main__":
    main()
