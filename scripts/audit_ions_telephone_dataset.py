#!/usr/bin/env python3
"""Read a pinned public workbook locally; emit aggregate counts only.

Exit 0: descriptive endpoints match; 2: mismatch needs reconciliation; 1: invalid input.
No network, participant export, significance test, or evidence promotion.
"""
import argparse
from collections import Counter
from decimal import Decimal, ROUND_HALF_UP
import hashlib
import io
import json
from pathlib import Path
import posixpath
import re
import sys
import xml.etree.ElementTree as ET
import zipfile

SHA256 = '83231d102887e6faae295afca161419cefce606c8463ed07e3246c6feeb03097'
MD5 = '07158e08d430cd17345428cf76728382'
SIZE = 87755
NS = {'m': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
REQUIRED = ('Status', 'Trialtype', 'Hit')
EXPECTED = {'pre_selected': {'trials': 210, 'accuracy_percent': '50.0'},
            'post_selected': {'trials': 630, 'accuracy_percent': '31.9'}}


def percent(hits, trials):
    return str((Decimal(hits) * 100 / Decimal(trials)).quantize(Decimal('0.1'), rounding=ROUND_HALF_UP))


def aggregate(rows):
    counts, hits = Counter(), Counter()
    for row in rows:
        if set(row) != set(REQUIRED):
            raise ValueError('missing or extra analytical fields')
        status, trial, hit = (row[k] for k in REQUIRED)
        if status not in ('Completer', 'Dropout') or trial not in ('0', '1') or hit not in ('0', '1'):
            raise ValueError('unsupported analytical value; no row contents exported')
        key = (status, trial)
        counts[key] += 1
        hits[key] += int(hit)
    if not counts or any(counts[('Completer', t)] == 0 for t in ('0', '1')):
        raise ValueError('both completer conditions are required')
    groups = []
    for (status, trial), n in sorted(counts.items()):
        groups.append({'status': status, 'condition': 'pre_selected' if trial == '1' else 'post_selected',
                       'trials': n, 'hits': hits[(status, trial)], 'accuracy_percent': percent(hits[(status, trial)], n)})
    match = all(g['trials'] == EXPECTED[g['condition']]['trials']
                and g['accuracy_percent'] == EXPECTED[g['condition']]['accuracy_percent']
                for g in groups if g['status'] == 'Completer')
    return {'total_rows': sum(counts.values()), 'groups': groups,
            'published_completer_endpoints': EXPECTED,
            'reproduction_status': 'DESCRIPTIVE_ENDPOINTS_MATCH' if match else 'MISMATCH_REQUIRES_RECONCILIATION',
            'p_values_reproduced': False, 'mechanism_verified': False,
            'independent_human_review': 'PENDING', 'promotion_allowed': False}


def selected_rows(blob):
    """Resolve the named Data sheet and read only the three analytical columns.

    Formulas are never evaluated. External references are never followed.
    Synthetic tests may call this reader; only audit() authenticates a source file.
    """
    with zipfile.ZipFile(io.BytesIO(blob)) as z:
        strings = []
        if 'xl/sharedStrings.xml' in z.namelist():
            for si in ET.fromstring(z.read('xl/sharedStrings.xml')).findall('m:si', NS):
                strings.append(''.join(t.text or '' for t in si.findall('.//m:t', NS)))
        sheets = ET.fromstring(z.read('xl/workbook.xml')).findall('m:sheets/m:sheet', NS)
        matches = [s for s in sheets if s.get('name') == 'Data']
        if len(matches) != 1:
            raise ValueError('one Data sheet required')
        rid = matches[0].get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id')
        rels = ET.fromstring(z.read('xl/_rels/workbook.xml.rels'))
        targets = [r for r in rels if r.get('Id') == rid]
        if len(targets) != 1 or targets[0].get('TargetMode') == 'External':
            raise ValueError('Data sheet relationship must be internal')
        target = targets[0].get('Target', '')
        path = posixpath.normpath(target.lstrip('/') if target.startswith('/') else 'xl/' + target)
        if not path.startswith('xl/'):
            raise ValueError('invalid worksheet path')
        worksheet = ET.fromstring(z.read(path))

        def value(cell):
            if cell.find('m:f', NS) is not None:
                raise ValueError('formula in analytical column')
            if cell.get('t') == 'inlineStr':
                return ''.join(t.text or '' for t in cell.findall('.//m:t', NS))
            v = cell.find('m:v', NS)
            if v is None or v.text is None:
                return None
            if cell.get('t') == 's':
                return strings[int(v.text)]
            if cell.get('t') in ('e', 'b'):
                raise ValueError('error or boolean cell in analytical column')
            return v.text

        rows = worksheet.findall('m:sheetData/m:row', NS)
        if not rows:
            raise ValueError('empty Data sheet')
        header = {}
        for cell in rows[0]:
            label = value(cell)
            if label in REQUIRED:
                if label in header:
                    raise ValueError('duplicate analytical header')
                header[label] = re.sub(r'\d', '', cell.attrib['r'])
        if set(header) != set(REQUIRED):
            raise ValueError('required analytical headers missing')
        columns = {v: k for k, v in header.items()}
        output = []
        for row in rows[1:]:
            selected = {}
            has_content = any(c.find('m:v', NS) is not None or c.find('m:is', NS) is not None or c.find('m:f', NS) is not None for c in row)
            if not has_content:
                continue
            for cell in row:
                col = re.sub(r'\d', '', cell.attrib['r'])
                if col in columns:
                    key = columns[col]
                    if key in selected:
                        raise ValueError('duplicate analytical cell')
                    selected[key] = value(cell)
            output.append(selected)
        return output


def audit(path):
    blob = Path(path).read_bytes()
    if len(blob) != SIZE or hashlib.sha256(blob).hexdigest() != SHA256:
        raise ValueError('input differs from the inspected Figshare version; stop for provenance review')
    report = aggregate(selected_rows(blob))
    report['source'] = {'doi': '10.6084/m9.figshare.21521235.v1', 'figshare_file_id': 38149656,
                        'sha256': SHA256, 'md5': MD5, 'size_bytes': SIZE,
                        'authors': ['Helane Wahbeh', 'Arnaud Delorme', 'Cedric Cannard', 'Dean Radin'],
                        'license': 'CC BY 4.0', 'license_url': 'https://creativecommons.org/licenses/by/4.0/',
                        'retrieved_date': '2026-10-12',
                        'publication_doi': '10.1016/j.explore.2023.08.008'}
    report['method'] = {'columns': list(REQUIRED), 'filter': 'Status exactly equals Completer',
                        'trialtype_mapping': {'0': 'post_selected', '1': 'pre_selected'},
                        'hit_mapping': {'0': 'incorrect', '1': 'correct'},
                        'source_of_mapping': 'Workbook Legend rows 1, 4, 5',
                        'exclusions': 'None beyond the source Status label; no outcome-driven filtering',
                        'scope': 'Descriptive counts only. Publication-specific analysis subset is unresolved.'}
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('workbook', type=Path)
    args = parser.parse_args()
    try:
        report = audit(args.workbook)
    except (OSError, ValueError, KeyError, IndexError, ET.ParseError, zipfile.BadZipFile):
        print('Audit failed: invalid, changed or unsupported input. No source values exported.', file=sys.stderr)
        return 1
    print(json.dumps(report, indent=2))
    return 0 if report['reproduction_status'] == 'DESCRIPTIVE_ENDPOINTS_MATCH' else 2


if __name__ == '__main__':
    raise SystemExit(main())
