"""Verify the bounded OMNI provenance inventory. Default execution is offline.

Hashes establish representation identity, not scientific or reviewer acceptance.
The external source checkout and public captures are optional, read-only inputs.
"""
import argparse
import ast
import hashlib
from html.parser import HTMLParser
import json
import os
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
LOCK_PATH = 'references/integration/v018/input-lock.json'
MANIFEST_PATH = 'references/integration/v018/omni/method-provenance.json'


def require(value, message):
    if not value:
        raise ValueError(message)


def inside(root, relative):
    """A manifest path must never select bytes outside its supplied root."""
    root = Path(root).resolve()
    path = (root / relative).resolve()
    require(not Path(relative).is_absolute() and path.is_relative_to(root),
            'path outside supplied root')
    return path


def check_bytes(data, pin):
    require(len(data) == pin['size_bytes'], 'byte length mismatch')
    require(hashlib.sha256(data).hexdigest() == pin['sha256'], 'SHA-256 mismatch')
    if 'git_blob_sha' in pin:
        blob = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
        require(blob == pin['git_blob_sha'], 'Git blob mismatch')


class ManualTables(HTMLParser):
    """Read only the two relevant tables from the pinned original HTML."""
    def __init__(self):
        super().__init__()
        self.sections = []
        self.tables = {'components': [], 'perspectives': []}
        self.cells = None
        self.cell = None

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'section':
            self.sections.append(attrs.get('id'))
        section = self.sections[-1] if self.sections else None
        if section in self.tables:
            if tag == 'tr':
                self.cells = []
            elif (tag == 'td' or tag == 'th' and attrs.get('scope') == 'row') and self.cells is not None:
                self.cell = {'text': [], 'links': []}
            elif tag == 'a' and self.cell is not None:
                self.cell['links'].append(attrs.get('href'))

    def handle_data(self, data):
        if self.cell is not None:
            self.cell['text'].append(data)

    def handle_endtag(self, tag):
        section = self.sections[-1] if self.sections else None
        if tag in {'td', 'th'} and self.cell is not None:
            self.cell['text'] = ' '.join(''.join(self.cell['text']).split())
            self.cells.append(self.cell)
            self.cell = None
        elif tag == 'tr' and self.cells is not None:
            if self.cells and section in self.tables:
                self.tables[section].append(self.cells)
            self.cells = None
        elif tag == 'section' and self.sections:
            self.sections.pop()


def verify_source_checkout(checkout, manifest):
    """Use the declared immutable commit, never whatever HEAD happens to be."""
    commit = manifest['source_provenance']['commit_sha']
    require(re.fullmatch(r'[0-9a-f]{40}', commit), 'invalid source commit')
    task_env = dict(os.environ, GIT_TERMINAL_PROMPT='0', GIT_NO_LAZY_FETCH='1')
    for pin in manifest['source_pins']:
        require(pin['path'] and not pin['path'].startswith(('/', '-'))
                and '..' not in Path(pin['path']).parts, 'invalid source path')
        raw = subprocess.check_output(['git', 'show', commit + ':' + pin['path']],
                                      cwd=checkout, env=task_env)
        check_bytes(raw, pin)
    return len(manifest['source_pins'])


def verify_repository(root=ROOT, capture_directory=None, sites_checkout=None):
    root = Path(root)
    lock = json.loads(inside(root, LOCK_PATH).read_bytes())
    method = lock['manual_method']
    reference = method['provenance_manifest']
    require(reference['path'] == MANIFEST_PATH, 'unexpected provenance manifest')
    raw_manifest = inside(root, reference['path']).read_bytes()
    require(hashlib.sha256(raw_manifest).hexdigest() == reference['sha256'],
            'manifest checksum mismatch')
    manifest = json.loads(raw_manifest)
    require(manifest['schema'] == 'akashicnet.omni-method-provenance.v1', 'manifest schema')
    require(method['version'] == manifest['method_version'] == '0.5.0 Public Review Specification',
            'method version mismatch')
    require(method['implementation'] == 'REFERENCE_ONLY_NOT_FULL_METHOD', 'method implementation boundary')
    require(method['original_html_pin'] == 'VERIFIED_HTTP_200_SNAPSHOT', 'original HTML status')
    require(method['components_individually_pinned'] is False, 'incomplete component gate changed')
    require(method['retrieved_text_sha256'] == manifest['historical_text']['sha256'],
            'historical representation changed')
    gates = manifest['gates']
    require(gates['original_html_pin_complete'] is True, 'original HTML pin missing')
    require(gates['components_individually_pinned'] is False
            and gates['method_pin_gate_complete'] is False, 'incomplete method gate changed')
    require(gates['real_pilot_status'] == 'HOLD' and gates['question_status'] == 'UNRESOLVED'
            and gates['v018_release_status'] == 'PLANNED_NOT_RELEASE_READY', 'review/release boundary')
    require(not any(gates['promotion_guards'].values()), 'promotion guard changed')
    assets = manifest['http_assets']
    require(len({a['id'] for a in assets}) == len(assets), 'duplicate HTTP identity')
    require(len({a['url'] for a in assets}) == len(assets), 'duplicate HTTP locator')
    bundled = 0
    external = 0
    for pin in assets:
        require(pin['status'] == 200 and pin['url'].startswith('https://akashicnet.org/')
                and pin['final_url'] == pin['url'], 'unverified HTTP asset')
        require(pin['representation'] == 'http_response_body_identity', 'HTTP representation')
        require(re.fullmatch(r'[0-9a-f]{64}', pin['sha256'])
                and pin['size_bytes'] > 0, 'invalid HTTP pin')
        if pin.get('bundled_path'):
            check_bytes(inside(root, pin['bundled_path']).read_bytes(), pin)
            bundled += 1
        if capture_directory is not None:
            check_bytes(inside(capture_directory, pin['capture_filename']).read_bytes(), pin)
            external += 1
    manual = next(a for a in assets if a['id'] == 'manual')
    require(method['original_html_sha256'] == manual['sha256'], 'manual lock mismatch')
    parser = ManualTables()
    parser.feed(inside(root, manual['bundled_path']).read_text(encoding='utf-8'))
    register = manifest['component_register']
    require(len(register) == len(parser.tables['components']) == 7, 'component register coverage')
    for entry, cells in zip(register, parser.tables['components']):
        require(len(cells) == 4 and entry['component'] == cells[0]['text']
                and entry['scope'] == cells[3]['text'], 'component register mismatch')
        require(len(entry['references']) == 2, 'original/addendum pair missing')
        for pin, cell in zip(entry['references'], cells[1:3]):
            require(cell['links'] == [pin['url']] and cell['text'] == pin['version_label'],
                    'component version/locator mismatch')
            require(pin['original_bytes_sha256'] is None
                    and pin['status'] == 'PENDING_AUTHORIZED_ARCHIVED_BYTES'
                    and pin['live_retrieval'] == 'NOT_ATTEMPTED_REDDIT_HOLD',
                    'unverified component promoted')
    source = ast.parse(inside(root, 'scripts/research_integration_v018.py').read_text())
    names = next(ast.literal_eval(n.value) for n in source.body if isinstance(n, ast.Assign)
                 and any(isinstance(t, ast.Name) and t.id == 'PERSPECTIVES' for t in n.targets))
    current = [cells[0]['text'].replace(' · ', ' ') for cells in parser.tables['perspectives']]
    require(names == current and len(names) == 12, 'pilot perspective mapping drift')
    source_count = verify_source_checkout(sites_checkout, manifest) if sites_checkout is not None else 0
    return {'bundled_http_bodies_verified': bundled, 'http_descriptors': len(assets),
            'external_http_bodies_verified': external, 'sites_source_blobs_verified': source_count,
            'component_bundles_complete': False, 'method_pin_gate_complete': False,
            'question_status': 'UNRESOLVED', 'real_pilot_status': 'HOLD'}


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--capture-directory', type=Path, help='Optional original HTTP bodies, read only')
    p.add_argument('--sites-checkout', type=Path, help='Optional authorized source Git repository, read only')
    args = p.parse_args()
    try:
        print(json.dumps(verify_repository(capture_directory=args.capture_directory,
                                           sites_checkout=args.sites_checkout), sort_keys=True))
    except (ValueError, KeyError, StopIteration, OSError, subprocess.CalledProcessError) as exc:
        p.exit(1, str(exc) + '\n')
