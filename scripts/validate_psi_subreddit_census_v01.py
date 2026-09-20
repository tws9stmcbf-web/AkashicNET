#!/usr/bin/env python3
import json
from pathlib import Path

PATH = Path("references/psi/subreddit-psi-metadata-census-v0.1.json")
data = json.loads(PATH.read_text(encoding="utf-8"))
expected = ["TEL", "CHN", "MED", "PRE", "RV", "PK", "PSI-PERSON"]
assert list(data["lanes"]) == expected
assert data["artifact_type"] == "METADATA_ONLY_SUBREDDIT_PSI_CENSUS"
governance = data["governance"]
assert governance["accepted_canonical_edges"] == 0
assert governance["supports_models"] == []
for key in (
    "truth_inference_allowed",
    "scientific_evidence_promotion_allowed",
    "model_support_promotion_allowed",
    "rights_promotion_allowed",
    "public_synthesis_allowed",
    "website_promotion_allowed",
    "source_import_allowed",
    "content_import_allowed",
):
    assert governance[key] is False
assert governance["review_state"] == "REVIEW_REQUIRED"
assert governance["privacy_gate"] == "FAIL_CLOSED"
assert governance["rights_gate"] == "FAIL_CLOSED"
assert governance["bq_statuses"] == {
    "BQ001": "UNRESOLVED",
    "BQ002": "UNRESOLVED",
    "BQ003": "UNRESOLVED",
}
for lane, block in data["lanes"].items():
    selected = block["selected_for_full_provenance_review"]
    assert selected["lane"] == lane
    assert selected["selection_only"] is True
    assert selected["content_import_authorized"] is False
    assert selected["public_synthesis_authorized"] is False
    assert selected["evidence_transfer_allowed"] is False
    assert selected["independent_corroboration"] is False
    assert all(record["evidence_transfer_allowed"] is False for record in block["records"])
    assert all(record["independent_corroboration"] is False for record in block["records"])
for lineage in data["cross_lane_lineages"]:
    assert lineage["evidence_transfer_allowed"] is False
    assert lineage["independent_corroboration"] is False
print("PSI subreddit census governance validation passed")
