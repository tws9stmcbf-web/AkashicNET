"""Offline guards for this dated, blocked S2 recovery packet.

These checks do not authenticate remote responses or complete S2 extraction.
"""
import copy
import hashlib
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / 'references/psi/moraes-table-s2-provenance-2026-10-06.json'


def validate_blocked_packet(packet):
    assert packet['status'] == 'REVIEW_REQUIRED'
    table = packet['authoritative_table']
    assert table['status'] == 'NOT_RECOVERED'
    assert table['download_url'] is None and table['sha256'] is None
    assert table['observed_row_count'] is None
    assert table['field_schema_verified_against_s2'] is False
    assert packet['included_study_rows'] == []
    reconciliation = packet['reconciliation']
    assert reconciliation['status'] == 'BLOCKED_PENDING_AUTHORITATIVE_S2'
    assert reconciliation['rows_extracted'] == 0
    assert reconciliation['rows_compared_to_existing_records'] == 0
    for key in ('matched_existing_publications', 'unmatched_publications',
                'unresolved_included_study_identifiers'):
        assert reconciliation[key] is None
    assert all(attempt['usable_s2'] is False for attempt in packet['recovery_attempts'])
    for record in packet['existing_source_lookup_seed']['records']:
        assert record['table_s2_membership'] == 'UNVERIFIED'
        for field in ('doi', 'pmid'):
            expected = ('STORED_IDENTIFIER' if record[field]
                        else 'UNRESOLVED_NOT_IN_SELECTED_RECORDS')
            assert record[field + '_status'] == expected
    gates = packet['governance']
    assert gates['BQ001_status'] == 'UNRESOLVED'
    assert gates['supports_models'] == []
    assert gates['privacy_gate'] == 'FAIL_CLOSED'
    for key in ('accepted_edges_added', 'new_source_identities_added',
                'independent_studies_added', 'replications_added'):
        assert type(gates[key]) is int and gates[key] == 0
    for key in ('truth_inference_allowed', 'scientific_evidence_promotion_allowed',
                'canonical_promotion_applied', 'public_synthesis_updated',
                'public_export_allowed', 'rights_promotion_allowed',
                'publication_promotion_allowed', 'original_evidence_batch_modified',
                'psi_pilot_modified', 'bibliographic_pilot_modified',
                'merge_performed', 'deployment_performed'):
        assert gates[key] is False


def validate_existing_aliases(packet):
    records = {r['existing_source_id']: r
               for r in packet['existing_source_lookup_seed']['records']}
    for alias in packet['confirmed_existing_identity_aliases']:
        assert alias['canonical_merge_applied'] is False
        # A DOI-only match may have a PMID on just one source record.
        source_pmids = {records[sid]['pmid'] for sid in alias['source_ids']
                        if records[sid]['pmid'] is not None}
        assert source_pmids == ({alias['pmid']} if alias['pmid'] is not None else set())
        for sid in alias['source_ids']:
            assert records[sid]['doi'] == alias['doi']
            if alias['basis'] == 'EXACT_NORMALIZED_DOI_AND_PMID':
                assert records[sid]['pmid'] == alias['pmid']


class TableS2ProvenanceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.packet = json.loads(LEDGER.read_text(encoding='utf-8'))

    def test_blocked_packet_is_not_extraction(self):
        validate_blocked_packet(self.packet)

    def test_unobserved_counts_cannot_be_presented_as_no_matches(self):
        for key in ('matched_existing_publications', 'unmatched_publications',
                    'unresolved_included_study_identifiers'):
            with self.subTest(key=key):
                changed = copy.deepcopy(self.packet)
                changed['reconciliation'][key] = 0
                with self.assertRaises(AssertionError):
                    validate_blocked_packet(changed)

    def test_lookup_seed_cannot_become_included_rows(self):
        changed = copy.deepcopy(self.packet)
        changed['included_study_rows'] = changed['existing_source_lookup_seed']['records']
        with self.assertRaises(AssertionError):
            validate_blocked_packet(changed)
        changed = copy.deepcopy(self.packet)
        changed['existing_source_lookup_seed']['records'][0]['table_s2_membership'] = 'CONFIRMED'
        with self.assertRaises(AssertionError):
            validate_blocked_packet(changed)

    def test_existing_inputs_and_lookup_loci_are_faithful(self):
        inputs = {}
        for entry in self.packet['existing_source_lookup_seed']['inputs']:
            content = (ROOT / entry['path']).read_bytes()
            self.assertEqual(hashlib.sha256(content).hexdigest(), entry['sha256'])
            git_blob = hashlib.sha1(b'blob ' + str(len(content)).encode() + b'\0' + content).hexdigest()
            self.assertEqual(git_blob, entry['pr_head_git_blob'])
            inputs[entry['path']] = json.loads(content)
        records = self.packet['existing_source_lookup_seed']['records']
        self.assertEqual(len(records), len({r['existing_source_id'] for r in records}))
        for record in records:
            values = {'titles': set(), 'doi': set(), 'pmid': set(), 'pmcid': set()}
            for locus in record['source_loci']:
                item = inputs[locus['path']]
                for token in locus['json_pointer'].split('/')[1:]:
                    token = token.replace('~1', '/').replace('~0', '~')
                    item = item[int(token)] if isinstance(item, list) else item[token]
                self.assertEqual(item.get('source_id', item.get('existing_source_id')),
                                 record['existing_source_id'])
                if 'crossref' in item:
                    values['titles'].add(item['crossref']['metadata']['title'][0])
                    values['pmid'].update(r['uid'] for r in item['pubmed']['records'])
                else:
                    values['titles'].add(item['title'])
                for key in ('doi', 'pmid', 'pmcid'):
                    if item.get(key):
                        values[key].add(item[key])
            self.assertEqual(values['titles'], set(record['titles']))
            for key in ('doi', 'pmid', 'pmcid'):
                self.assertEqual(values[key], {record[key]} if record[key] else set())

    def test_aliases_use_matching_identifiers_without_merges(self):
        validate_existing_aliases(self.packet)

    def test_alias_pmid_cannot_be_invented_or_dropped(self):
        for index, alias in enumerate(self.packet['confirmed_existing_identity_aliases']):
            for pmid in ('99999999', None):
                with self.subTest(basis=alias['basis'], pmid=pmid):
                    changed = copy.deepcopy(self.packet)
                    changed['confirmed_existing_identity_aliases'][index]['pmid'] = pmid
                    with self.assertRaises(AssertionError):
                        validate_existing_aliases(changed)

    def test_promotion_is_rejected(self):
        for key in ('rights_promotion_allowed', 'scientific_evidence_promotion_allowed',
                    'public_export_allowed', 'publication_promotion_allowed'):
            with self.subTest(key=key):
                changed = copy.deepcopy(self.packet)
                changed['governance'][key] = True
                with self.assertRaises(AssertionError):
                    validate_blocked_packet(changed)


if __name__ == '__main__':
    unittest.main()
