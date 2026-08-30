#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BATCH = ROOT / "references" / "community" / "bq001-scientific-baseline-batch1.json"
TAXONOMY = ROOT / "references" / "community" / "evidence-taxonomy-v0.10.json"
CORE_SCHEMA = ROOT / "data" / "evidence_claim_v01.schema.json"

EXPECTED_SOURCES = {
    "BQ001-SRC-AWARE-2014": ("25301715", "10.1016/j.resuscitation.2014.09.004"),
    "BQ001-SRC-AWARE2-2023": ("37423492", "10.1016/j.resuscitation.2023.109903"),
    "BQ001-SRC-MASCHKE-2024": (None, "10.1038/s42003-024-06613-8"),
    "BQ001-SRC-KOCH-2016": (None, "10.1038/nrn.2016.22"),
}
EXPECTED_LABELS = {
    "Established Evidence",
    "Interpretation",
    "Lived Experience/Testimony",
    "Hypothesis",
    "Speculation",
}
FORBIDDEN_FRAGMENTS = (
    "proves consciousness after death",
    "proves survival after death",
    "proves consciousness independent of brain",
    "proves that continuation beyond irreversible biological death is impossible",
)


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    batch = load(BATCH)
    taxonomy = load(TAXONOMY)
    schema = load(CORE_SCHEMA)

    assert batch["question_id"] == "BQ001"
    assert batch["question_status"] == "UNRESOLVED"
    assert batch["batch"] == "SCIENTIFIC_BASELINE_1"
    assert set(taxonomy["canonical_labels"]) == EXPECTED_LABELS

    sources = {s["source_id"]: s for s in batch["sources"]}
    assert set(sources) == set(EXPECTED_SOURCES)
    for source_id, (pmid, doi) in EXPECTED_SOURCES.items():
        source = sources[source_id]
        assert source["doi"] == doi
        if pmid is not None:
            assert source["pmid"] == pmid
        assert source["url"].startswith("https://")

    core = batch["evidence_core"]
    assert core["evidence_model_version"] == "0.1"
    assert schema["properties"]["evidence_model_version"]["const"] == "0.1"
    claims = {c["claim_id"]: c for c in core["claims"]}
    assert set(claims) == {"BQ001-C1", "BQ001-C2", "BQ001-C3", "BQ001-C4", "BQ001-C5"}

    allowed_claim_classes = set(schema["properties"]["claims"]["items"]["properties"]["claim_class"]["enum"])
    allowed_statuses = set(schema["properties"]["claims"]["items"]["properties"]["status"]["enum"])
    for claim in claims.values():
        assert claim["claim_class"] in allowed_claim_classes
        assert claim["status"] in allowed_statuses
        assert claim["statement"].strip()
        text = claim["statement"].lower()
        for fragment in FORBIDDEN_FRAGMENTS:
            assert fragment not in text
        for source_id in claim["provenance"]["source_ids"]:
            assert source_id in sources

    links = core["evidence_links"]
    assert len(links) == 5
    for link in links:
        assert link["claim_id"] in claims
        assert link["source_id"] in sources
        assert link["evidence_tier"] == "EMPIRICAL_REFERENCE"
        assert link["assessment_state"] == "REVIEWED"
        assert link["notes"].strip()

    annotations = {a["claim_id"]: a["label"] for a in batch["epistemic_annotations"]}
    assert set(annotations) == set(claims)
    assert set(annotations.values()).issubset(EXPECTED_LABELS)
    assert annotations["BQ001-C5"] == "Interpretation"
    for cid in ("BQ001-C1", "BQ001-C2", "BQ001-C3", "BQ001-C4"):
        assert annotations[cid] == "Established Evidence"

    limitations = " ".join(batch["material_limitations"]).lower()
    for required in ("survival", "interview", "exact time", "eeg", "irreversible biological death"):
        assert required in limitations

    implications = batch["model_implications"]
    assert implications["brain_state_dependence_under_tested_conditions"] == "SUPPORTED"
    assert implications["consciousness_after_irreversible_biological_death"] == "UNRESOLVED"
    assert implications["consciousness_independent_of_brain_function"] == "UNRESOLVED"
    assert implications["model_edges_upgrade_epistemic_label"] is False

    for key, value in batch["release_invariants"].items():
        assert value is False, f"fail-closed invariant changed: {key}"

    print("BQ001 SCIENTIFIC BASELINE BATCH 1 PASS: observations separated from interpretation; BQ001 remains UNRESOLVED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
