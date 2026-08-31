#!/usr/bin/env python3
"""Fail-closed static contract check for legacy metadata provenance scoring v0.5.

The private Drive-derived graph/ledger are intentionally not required. This validator
checks the public scoring specification and generator source for the boundaries that
must hold whenever the private scoring pipeline is run.
"""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = ROOT / "references/community/evidence-provenance-scoring-v0.1.md"
OVERLAY = ROOT / "scripts/overlay_evidence_provenance_v05.py"

SPEC_MARKERS = (
    "does **not** measure whether a work's claims are true, scientifically valid",
    "Rights remain independent.",
    "No score in this layer may promote a claim or source to scientific-evidence status.",
    "`UNRESOLVED_PROVENANCE`: score cannot exceed 45",
    "`REVIEW_REQUIRED`: score cannot exceed 55",
    "Even E3 is still metadata-level evidence",
    "Hash identity is never inferred from equal filename/title/size alone.",
    "Scientific-evidence status is never promoted from provenance or canonical-confidence scoring alone.",
)

OVERLAY_MARKERS = (
    "if r['reconciled_status']=='UNRESOLVED_PROVENANCE': cap=45",
    "if r['reconciled_status']=='REVIEW_REQUIRED': cap=55",
    "'not_truth_score':True",
    "'not_rights_score':True",
    "'not_scientific_evidence_score':True",
    "'truth_inference_allowed':False",
    "'rights_promotion_allowed':False",
    "'scientific_evidence_promotion_allowed':False",
    "graph['policy']['evidence_score_is_not_truth_score']=True",
    "graph['policy']['evidence_score_does_not_change_rights']=True",
    "graph['policy']['evidence_score_is_not_scientific_evidence_score']=True",
    "n.get('rights_status')=='UNKNOWN_UNVERIFIED'",
)


def validate(spec_text: str, overlay_text: str) -> list[str]:
    failures: list[str] = []
    for marker in SPEC_MARKERS:
        if marker not in spec_text:
            failures.append(f"spec marker missing: {marker}")
    for marker in OVERLAY_MARKERS:
        if marker not in overlay_text:
            failures.append(f"overlay guard missing: {marker}")
    return failures


def main() -> int:
    failures = validate(
        SPEC.read_text(encoding="utf-8"),
        OVERLAY.read_text(encoding="utf-8"),
    )
    if failures:
        print("EVIDENCE/PROVENANCE v0.5 CONTRACT: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("EVIDENCE/PROVENANCE v0.5 CONTRACT: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
