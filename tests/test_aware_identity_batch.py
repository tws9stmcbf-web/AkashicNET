"""Focused negative regressions for identity, duplicate counting and closed gates."""
import copy
import importlib.util
import json
from pathlib import Path
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('aware', ROOT / 'scripts/validate_aware_identity_batch.py')
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


class AwareIdentityTests(unittest.TestCase):
    def setUp(self):
        self.packet = json.loads(mod.BATCH.read_text())
        # Minimal synthetic catalogue: never substitutes for pinned-snapshot validation.
        self.catalogue = [{'id': f'SYNTHETIC-{i}', 'doi': None} for i in range(70)]
        for i, r in enumerate(self.packet['records'], 54):
            self.catalogue[i] = {'id': r['catalogue_record_id'], 'doi': r['doi'],
                                 'catalogue_review': {'status': 'REVIEW_REQUIRED'}}

    def test_valid_crosswalk(self):
        mod.validate(self.packet, self.catalogue)

    def test_invalid_source_locators_rejected(self):
        for index, key, value in [
            (0, 'existing_source_path', 'missing.json'),
            (0, 'community_source_path', 'missing.json'),
            (0, 'existing_source_pointer', '/wrong/0'),
            (0, 'existing_source_pointer', '/sources/00'),
            (0, 'catalogue_pointer', 'x54'),
            (0, 'catalogue_pointer', '/-16'),
            (0, 'related_ledger_work_id', 'WORK-343-AWARE2-2023'),
            (1, 'related_ledger_path', 'missing.json'),
            (1, 'related_ledger_work_id', 'BOGUS'),
        ]:
            with self.subTest(index=index, key=key, value=value):
                p = copy.deepcopy(self.packet)
                p['records'][index]['deduplication'][key] = value
                with self.assertRaises(ValueError):
                    mod.validate(p, self.catalogue)

    def test_missing_or_mismatched_ledger_rejected(self):
        ledger_path = ROOT / mod.LEDGER_PATH
        original_read = Path.read_text
        ledger = json.loads(ledger_path.read_text())
        wrong = copy.deepcopy(ledger)
        next(w for w in wrong['works'] if w['work_id'] == 'WORK-343-AWARE2-2023')['pmid'] = '25301715'
        for replacement in ({'works': []}, wrong, None):
            def read(path, *args, **kwargs):
                if path == ledger_path:
                    if replacement is None:
                        raise FileNotFoundError(path)
                    return json.dumps(replacement)
                return original_read(path, *args, **kwargs)
            with self.subTest(replacement=replacement is None), patch.object(Path, 'read_text', read):
                with self.assertRaises((ValueError, FileNotFoundError)):
                    mod.validate(self.packet, self.catalogue)

    def test_swapped_pmid_and_unrelated_endpoint_rejected(self):
        for key, value in [('pmid', '37423492'), ('pubmed_url', 'https://pubmed.ncbi.nlm.nih.gov/37423492/')]:
            with self.subTest(key=key):
                p = copy.deepcopy(self.packet)
                p['records'][0][key] = value
                with self.assertRaises(ValueError):
                    mod.validate(p, self.catalogue)

    def test_normalized_catalogue_duplicate_rejected(self):
        self.catalogue[0]['doi'] = ' HTTPS://DOI.ORG/10.1016/J.RESUSCITATION.2014.09.004 '
        with self.assertRaises(ValueError):
            mod.validate(self.packet, self.catalogue)

    def test_duplicate_batch_rejected(self):
        self.packet['records'][1] = copy.deepcopy(self.packet['records'][0])
        with self.assertRaises(ValueError):
            mod.validate(self.packet, self.catalogue)

    def test_gate_opening_rejected(self):
        for gate in ('evidence', 'canonical', 'rights', 'publication', 'promotion', 'privacy'):
            with self.subTest(gate=gate):
                p = copy.deepcopy(self.packet)
                p['governance'][gate + '_gate'] = 'OPEN'
                with self.assertRaises(ValueError):
                    mod.validate(p, self.catalogue)

    def test_promotion_and_body_retention_rejected(self):
        for key, value in [('independent_studies_added', 1), ('supports_models', ['M1']),
                           ('review_state', 'APPROVED'), ('article_body', 'disallowed')]:
            with self.subTest(key=key):
                p = copy.deepcopy(self.packet)
                p['records'][0][key] = value
                with self.assertRaises(ValueError):
                    mod.validate(p, self.catalogue)


if __name__ == '__main__':
    unittest.main()
