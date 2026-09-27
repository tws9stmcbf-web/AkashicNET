#!/usr/bin/env python3
import csv
import hashlib
import io
import json
import re
from collections import defaultdict
from pathlib import Path


# This versioned policy is deliberately independent of the artifact being validated.
DISCOVERY = {'version': '1',
 'normalization': 'ASCII lowercase; extract [a-z0-9_]+ title slug immediately after '
                  '/comments/<post_id>/; split on underscores and discard empty tokens; no '
                  'stemming, decoding or substring matching.',
 'matching': 'Any listed phrase matches consecutive whole tokens. Bare channel is excluded. No '
             'semantic exclusions; false positives remain review candidates. Supplemental metadata '
             'enters only explicitly seeded lanes; vocabulary scans indexed metadata only.',
 'index_rows': 'Only NeuronsToNirvana post rows; URL post_id must equal row post_id. Deduplicate '
               'post IDs, choosing lexicographically smallest normalized slug and canonical URL. '
               'Rows without title slugs count toward indexed IDs but cannot match vocabulary.',
 'vocabulary': {'TEL': ['telepathy', 'telepathic', 'mindreading'],
                'CHN': ['channeling', 'channelling', 'channelers', 'channeled', 'channelled'],
                'MED': ['mediumship', 'channelling_spirits'],
                'PRE': ['precognition', 'presentiment'],
                'RV': ['remote_viewing', 'military_remote'],
                'PK': ['psychokinesis', 'telekinesis', 'loving_intention', 'cooks_intention'],
                'PSI-PERSON': ['psychic', 'psychics', 'channelers', 'mind_readers']},
 'seed_post_ids': {'TEL': [],
                   'CHN': ['1vyr82r'],
                   'MED': [],
                   'PRE': [],
                   'RV': [],
                   'PK': ['15rxs24'],
                   'PSI-PERSON': []},
 'supplemental_metadata': [{'post_id': '1vyr82r',
                            'title_slug': 'three_channelers_describe_the_same_extraterrestrials',
                            'reddit_url': 'https://www.reddit.com/r/NeuronsToNirvana/comments/1vyr82r/three_channelers_describe_the_same_extraterrestrials/'}],
 'supplemental_metadata_origin': 'Carried forward as unverified metadata from census commit '
                                 '81cee7a6c93aa50be27b48f54ba5f1566ebce356, blob '
                                 '62258a6f2d41d8f0f1fb0db0a71ac82e8b644a61. Not governed source '
                                 'provenance.',
 'lineage_rule': 'Group normalized title slugs across lanes; RSL- plus uppercase lexicographically '
                 'smallest post ID, except the explicitly pinned governed source mapping.'}
INDEX_PATH = "references/community/reddit-semantic-index.csv"
INDEX_BLOB = "56be9ed9e89226c808ef1de4287056ee359187be"
PROVENANCE = {'path': 'references/consciousness/interbrain-telepathy-mayim-bialik-source-crawl-v0.1.json',
 'git_blob_sha': '2266fa2073ef75e4757d97dfc5bc670bd187d6c6',
 'pre_existing_commit': 'dfc0854c826cade04d9bbc67fb69f7c712f66944',
 'json_pointer': '/sources/0'}
GOVERNED_ID = "MBB-KY-DICKENS-2025-10-24"
GOVERNED_URL = "https://www.bialikbreakdown.com/episodes/better-than-cia-mind-readers-ky-dickens-has-proof-telepathy-psychic-abilities-are-real"


def checked_blob(path, expected):
    raw = Path(path).read_bytes()
    digest = hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()
    assert digest == expected, (path, "pinned blob mismatch")
    return raw.decode("utf-8")


def replay_discovery():
    rows = csv.DictReader(io.StringIO(checked_blob(INDEX_PATH, INDEX_BLOB)))
    indexed_ids, candidates = set(), defaultdict(set)
    for row in rows:
        if row["subreddit"] != "NeuronsToNirvana" or row["url_type"] != "post":
            continue
        post_id = row["post_id"]
        assert re.fullmatch(r"[a-z0-9]+", post_id)
        indexed_ids.add(post_id)
        match = re.match(r"https://www\.reddit\.com/r/neuronstonirvana/comments/([a-z0-9]+)(?:/([a-z0-9_]+))?(?=/|$|,)", row["reddit_url"].lower())
        assert match and match[1] == post_id
        if match[2]:
            slug = "_".join(filter(None, match[2].split("_")))
            url = f"https://www.reddit.com/r/NeuronsToNirvana/comments/{post_id}/{slug}/"
            candidates[post_id].add((slug, url))
    metadata = {pid: min(values) for pid, values in candidates.items()}
    for seed in DISCOVERY["supplemental_metadata"]:
        assert seed["post_id"] not in indexed_ids
        metadata[seed["post_id"]] = (seed["title_slug"], seed["reddit_url"])
    lanes = {}
    for lane, terms in DISCOVERY["vocabulary"].items():
        seeds = set(DISCOVERY["seed_post_ids"][lane])
        assert seeds <= metadata.keys()
        lanes[lane] = {pid: values for pid, values in metadata.items()
                       if pid in seeds or (pid in indexed_ids and any("_" + term + "_" in "_" + values[0] + "_" for term in terms))}
    groups = defaultdict(set)
    for records in lanes.values():
        for pid, (slug, _) in records.items():
            groups[slug].add(pid)
    lineages = {slug: "RSL-" + min(ids).upper() for slug, ids in groups.items()}
    return indexed_ids, lanes, lineages

PATH = Path("references/psi/subreddit-psi-metadata-census-v0.1.json")
data = json.loads(PATH.read_text(encoding="utf-8"))
assert data["method"]["discovery"] == DISCOVERY, "discovery policy drift"
assert data["source_surface"]["path"] == INDEX_PATH
assert data["source_surface"]["git_blob_sha"] == INDEX_BLOB
assert data["source_surface"]["supplemental_provisional_records"] == ["1vyr82r"]
assert "supplemental_governed_records" not in data["source_surface"]
indexed_ids, discovered, lineages = replay_discovery()
assert data["source_surface"]["unique_indexed_post_ids"] == len(indexed_ids)
source = json.loads(checked_blob(PROVENANCE["path"], PROVENANCE["git_blob_sha"]))["sources"][0]
assert source["source_id"] == GOVERNED_ID and source["source_url"] == GOVERNED_URL
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
    records = block["records"]
    ids = [record["post_id"] for record in records]
    assert len(ids) == len(set(ids)), (lane, "duplicate post ID")
    assert set(ids) == set(discovered[lane]), (lane, "discovery membership drift")
    assert block["matched_manifestations"] == len(discovered[lane])
    assert block["provisional_unique_source_lineages"] == len({r["source_lineage_id"] for r in records})
    for record in records:
        pid = record["post_id"]
        assert record["lane"] == lane
        assert (record["title_slug"], record["reddit_url"]) == discovered[lane][pid]
        if pid == "1oyi2qp":
            assert record["lineage_basis"] == "GOVERNED_SOURCE_MAPPING"
            assert record["repository_provenance"] == PROVENANCE
            assert record["source_lineage_id"] == GOVERNED_ID
            assert record["underlying_source_urls"] == [GOVERNED_URL]
            assert record["review_state"] == "EXISTING_GOVERNED_SOURCE_REDDIT_MANIFESTATION"
        else:
            assert record["lineage_basis"] == "NORMALIZED_TITLE_SLUG_PROVISIONAL"
            assert record["source_lineage_id"] == lineages[record["title_slug"]]
            assert record["underlying_source_urls"] == []
            assert record["review_state"] == "METADATA_ONLY_REVIEW_REQUIRED"
            assert "repository_provenance" not in record
    selected = block["selected_for_full_provenance_review"]
    matches = [record for record in records if record["post_id"] == selected["post_id"]]
    assert len(matches) == 1, (lane, "selection must identify exactly one lane record")
    assert all(key in selected and selected[key] == value for key, value in matches[0].items()), (lane, "selected record differs")
    assert set(selected) == set(matches[0]) | {"selection_rationale", "selection_only", "content_import_authorized", "public_synthesis_authorized"}

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

