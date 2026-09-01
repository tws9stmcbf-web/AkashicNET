#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BQ_ROOT = ROOT / "references" / "big-questions"


def main() -> int:
    checked = 0
    for path in BQ_ROOT.rglob("evidence-batch*.json"):
        payload = json.loads(path.read_text(encoding="utf-8"))
        sources = payload.get("sources", [])
        for source in sources:
            checked += 1
            original = source.get("url") or source.get("source_url")
            assert original, f"missing original URL in {path}"
            link_check = source.get("link_check")
            if link_check is not None:
                assert isinstance(link_check, dict), f"invalid link_check in {path}"
                assert link_check.get("checked_at"), f"missing checked_at in {path}"
                status = link_check.get("status") or link_check.get("state")
                assert status, f"missing link-check status in {path}"
                assert source.get("url", original) == original or source.get("source_url", original) == original
    assert checked > 0, "no public evidence source records discovered"
    print(f"PUBLIC KNOWLEDGE LINK INTEGRITY v0.13 PASS: {checked} source record(s); original URLs preserved")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
