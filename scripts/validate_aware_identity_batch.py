#!/usr/bin/env python3
"""Validate the bounded, review-only AWARE crosswalk against pinned inputs."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
BATCH = ROOT / 'references/psi/aware-underlying-publication-identity-2026-10-03.json'
SOURCE_HEAD = 'c54a946f7f4abef3ad2a7f2a70102c801b697d09'
CATALOGUE_HEAD = 'c2262f8df8e800478e3f7abfd5407cbc9069173a'
CATALOGUE_PATH = 'website/public/research/source-catalogue/records.json'
EXPECTED = {
    'CM-LEAD-001': ('10.1016/j.resuscitation.2014.09.004', '25301715', 'SRC-BQ001-AWARE-2014'),
    'CM-LEAD-002': ('10.1016/j.resuscitation.2023.109903', '37423492', 'SRC-BQ001-AWARE2-2023'),
}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def normalize_doi(value):
    value = (value or '').strip().lower()
    for prefix in ('https://doi.org/', 'http://doi.org/', 'doi:'):
        if value.startswith(prefix):
            value = value[len(prefix):]
    return value.strip()


def validate(packet, catalogue):
    require(packet['source_boundary']['commit'] == SOURCE_HEAD, 'source head changed')
    require(packet['source_boundary']['source_id'] == 'SRC-SPR-PE-0001', 'discovery source changed')
    require(packet['source_boundary']['original_pilot_modified'] is False, 'pilot changed')
    require(packet['catalogue_snapshot']['commit'] == CATALOGUE_HEAD, 'catalogue head changed')
    require(packet['catalogue_snapshot']['path'] == CATALOGUE_PATH, 'catalogue path changed')
    require(packet['catalogue_snapshot']['modified'] is False, 'catalogue modified')
    scope = packet['scope']
    require(scope['candidate_publications'] == 2, 'scope expanded')
    for key in ('site_wide_crawl_performed', 'methodological_appraisal_performed', 'new_source_ids_minted'):
        require(scope[key] is False, 'scope expanded: ' + key)
    require(len(catalogue) == packet['catalogue_snapshot']['record_count'] == 70, 'catalogue count changed')
    g = packet['governance']
    for key in ('evidence', 'canonical', 'rights', 'publication', 'promotion', 'privacy'):
        require(g[key + '_gate'] == 'CLOSED', key + ' gate open')
    for key in ('independent_studies_added', 'accepted_edges_added', 'new_publication_records_added'):
        require(type(g[key]) is int and g[key] == 0, key + ' nonzero')
    for key in ('big_question_status_changes', 'article_text_retained', 'extended_quotations_retained'):
        require(g[key] is False, key + ' enabled')
    require(g['review_state'] == 'REVIEW_REQUIRED' and g['rights_status'] == 'LINK_AND_METADATA_ONLY', 'review/rights opened')
    require(g['supports_models'] == [], 'model support added')
    records = packet['records']
    require(len(records) == 2, 'batch must contain exactly two links')
    require({r['catalogue_record_id'] for r in records} == set(EXPECTED), 'duplicate or unexpected identity')
    require(len({normalize_doi(r['doi']) for r in records}) == 2, 'duplicate DOI')
    sources = json.loads((ROOT / 'references/big-questions/BQ001/evidence-batch1-v0.1.json').read_text())['sources']
    community = json.loads((ROOT / 'references/community/bq001-scientific-baseline-batch1.json').read_text())['sources']
    for r in records:
        cid = r['catalogue_record_id']
        doi, pmid, sid = EXPECTED[cid]
        require((normalize_doi(r['doi']), r['pmid'], r['existing_source_id']) == (doi, pmid, sid), 'DOI/PMID/source mismatch')
        matches = [c for c in catalogue if normalize_doi(c.get('doi')) == doi]
        require(len(matches) == 1 and matches[0]['id'] == cid, 'catalogue duplicate or wrong identity')
        c = matches[0]
        require(c['catalogue_review']['status'] == 'REVIEW_REQUIRED', 'catalogue review changed')
        require(catalogue[int(r['deduplication']['catalogue_pointer'][1:])]['id'] == cid, 'catalogue pointer mismatch')
        require(c.get('catalogue_review', {}).get('identifiers', {}).get('pmid') in (None, pmid), 'catalogue PMID conflict')
        s = next(s for s in sources if s['source_id'] == sid)
        require((s['doi'], s['pmid'], s['title'], s['year']) == (doi, pmid, r['title'], r['year']), 'existing source mismatch')
        require(sources[int(r['deduplication']['existing_source_pointer'].split('/')[-1])]['source_id'] == sid, 'existing source pointer mismatch')
        cs = next(s for s in community if s['source_id'] == r['community_source_id'])
        require((cs['doi'], cs['pmid']) == (doi, pmid), 'community identity mismatch')
        require(r['pubmed_url'] == f'https://pubmed.ncbi.nlm.nih.gov/{pmid}/', 'unrelated PubMed endpoint')
        require(r['doi_url'] == 'https://doi.org/' + doi, 'unrelated DOI endpoint')
        require(r['deduplication']['action'] == 'LINK_EXISTING_ONLY', 'duplicate insertion requested')
        require(r['identity_status'] == 'MATCHED_EXISTING_PUBLICATION_REVIEW_REQUIRED', 'identity promoted')
        require(r['review_state'] == 'REVIEW_REQUIRED' and r['rights_status'] == 'LINK_AND_METADATA_ONLY', 'record gate opened')
        require(r['supports_models'] == [] and type(r['independent_studies_added']) is int and r['independent_studies_added'] == 0, 'evidence promoted')
        require(r['article_text_retained'] is False, 'article text retained')
        require(r['discovered_from'] == 'SRC-SPR-PE-0001', 'discovery lineage changed')
        require(r['provenance']['bibliographic_verification_url'] == f'https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=EXT_ID:{pmid}%20AND%20SRC:MED&format=json', 'metadata endpoint mismatch')
    def no_bodies(obj):
        if isinstance(obj, dict):
            require(not {'abstract', 'article_body', 'full_text', 'quotation', 'extended_quotation'} & obj.keys(), 'body/quotation field forbidden')
            for value in obj.values():
                no_bodies(value)
        elif isinstance(obj, list):
            for value in obj:
                no_bodies(value)
    no_bodies(packet)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--catalogue-file', type=Path, help='Exact bytes of the pinned catalogue; SHA-256 checked')
    args = parser.parse_args()
    packet = json.loads(BATCH.read_text())
    raw = args.catalogue_file.read_bytes() if args.catalogue_file else subprocess.check_output(
        ['git', 'show', f'{CATALOGUE_HEAD}:{CATALOGUE_PATH}'], cwd=ROOT)
    require(hashlib.sha256(raw).hexdigest() == packet['catalogue_snapshot']['sha256'], 'catalogue snapshot hash mismatch')
    validate(packet, json.loads(raw))
    pilot_path = packet['source_boundary']['path']
    require((ROOT / pilot_path).read_bytes() == subprocess.check_output(
        ['git', 'show', f'{SOURCE_HEAD}:{pilot_path}'], cwd=ROOT), 'historical pilot modified')
    pilot = json.loads((ROOT / pilot_path).read_text())
    entry = next(r for r in pilot['records'] if r['source_id'] == 'SRC-SPR-PE-0001')
    require(entry['cited_study_identifiers'] == [] and entry['cited_study_identifiers_status'] == 'NOT_EXTRACTED_IN_THIS_PILOT', 'pilot boundary mismatch')
    print('PASS: two existing identities; zero additions; all batch gates closed')


if __name__ == '__main__':
    main()
