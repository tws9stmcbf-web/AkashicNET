"""Synthetic safety/aggregation tests. CI does not download participant data."""
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('ions_data_audit', ROOT / 'scripts/audit_ions_telephone_dataset.py')
audit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)


def rows(n=3):
    return [{'Status': 'Completer', 'Trialtype': str(i % 2), 'Hit': str(i % 2)} for i in range(n)]


def workbook(formula=False):
    buf = io.BytesIO()
    uri = 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'
    with zipfile.ZipFile(buf, 'w') as z:
        z.writestr('xl/workbook.xml', f'<workbook xmlns="{uri}" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"><sheets><sheet name="Data" r:id="rId7"/></sheets></workbook>')
        z.writestr('xl/_rels/workbook.xml.rels', '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId7" Target="worksheets/sheet7.xml"/></Relationships>')
        cells = ''.join(f'<c r="{col}1" t="inlineStr"><is><t>{label}</t></is></c>' for col, label in [('A','Status'),('B','SubjectID'),('D','Trialtype'),('E','Hit')])
        formula_xml = '<f>1+0</f>' if formula else ''
        z.writestr('xl/worksheets/sheet7.xml', f'<worksheet xmlns="{uri}"><sheetData><row r="1">{cells}</row><row r="2"><c r="A2" t="inlineStr"><is><t>Completer</t></is></c><c r="B2" t="inlineStr"><is><t>SYNTHETIC-PRIVATE-SENTINEL</t></is></c><c r="D2"><v>1</v></c><c r="E2">{formula_xml}<v>1</v></c></row></sheetData></worksheet>')
    return buf.getvalue()


class TelephoneAuditTests(unittest.TestCase):
    def test_mismatch_is_explicit_and_not_significance(self):
        report = audit.aggregate(rows())
        self.assertEqual(report['reproduction_status'], 'MISMATCH_REQUIRES_RECONCILIATION')
        self.assertFalse(report['p_values_reproduced'])
        self.assertFalse(report['mechanism_verified'])
        self.assertFalse(report['promotion_allowed'])

    def test_match_requires_denominator_and_rounded_accuracy(self):
        r = ([{'Status':'Completer','Trialtype':'1','Hit':str(int(i < 105))} for i in range(210)]
             + [{'Status':'Completer','Trialtype':'0','Hit':str(int(i < 201))} for i in range(630)])
        self.assertEqual(audit.aggregate(r)['reproduction_status'], 'DESCRIPTIVE_ENDPOINTS_MATCH')
        r.append({'Status':'Completer','Trialtype':'1','Hit':'0'})
        self.assertEqual(audit.aggregate(r)['reproduction_status'], 'MISMATCH_REQUIRES_RECONCILIATION')

    def test_invalid_values_and_missing_fields_fail(self):
        for key, value in [('Status','Unknown'),('Trialtype','2'),('Hit','2'),('Hit',None)]:
            r=rows();r[0][key]=value
            with self.subTest(key=key,value=value), self.assertRaises(ValueError): audit.aggregate(r)
        r=rows();del r[0]['Hit']
        with self.assertRaises(ValueError):audit.aggregate(r)

    def test_no_data_or_single_condition_is_not_a_match(self):
        for r in ([],[{'Status':'Completer','Trialtype':'1','Hit':'1'}]):
            with self.assertRaises(ValueError):audit.aggregate(r)

    def test_sheet_resolution_and_column_minimization(self):
        selected=audit.selected_rows(workbook())
        self.assertEqual(selected,[{'Status':'Completer','Trialtype':'1','Hit':'1'}])
        self.assertNotIn('PRIVATE-SENTINEL',json.dumps(selected))

    def test_cached_formula_cannot_masquerade_as_observation(self):
        with self.assertRaises(ValueError):audit.selected_rows(workbook(formula=True))

    def test_different_source_file_rejected_before_counting(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/'source.xlsx';p.write_bytes(workbook())
            with self.assertRaises(ValueError):audit.audit(p)

    def test_frozen_aggregate_receipt_is_internally_consistent(self):
        p=ROOT/'references/akashicomni/ions-telephone-data-check-2026-10-12.json'
        receipt=json.loads(p.read_text())
        self.assertEqual(receipt['source']['sha256'],audit.SHA256)
        self.assertEqual(receipt['total_rows'],sum(g['trials'] for g in receipt['groups']))
        for g in receipt['groups']:
            self.assertEqual(g['accuracy_percent'],audit.percent(g['hits'],g['trials']))
            self.assertLessEqual(g['hits'],g['trials'])
        self.assertEqual(receipt['reproduction_status'],'MISMATCH_REQUIRES_RECONCILIATION')
        self.assertEqual(receipt['independent_human_review'],'PENDING')
        # This checks the saved aggregate, not the original row counts; the workbook is not in CI.


if __name__ == '__main__':
    unittest.main()
