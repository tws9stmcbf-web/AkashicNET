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
import zipfile

ROOT = Path(__file__).resolve().parents[1]
LOCK_PATH = 'references/integration/v018/input-lock.json'
MANIFEST_PATH = 'references/integration/v018/omni/method-provenance.json'
COMPONENT_REVIEW_PATH = 'references/integration/v018/omni/component-archive-review.json'


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


def verify_component_review(root, manifest, private_evidence_directory=None):
    """Check an incomplete archive review without confusing receipts with originals.

    Optional private inputs stay outside the checkout. Nothing is copied, fetched,
    retained by this verifier, or accepted as complete component provenance.
    """
    reference = manifest['component_archive_review']
    require(reference['path'] == COMPONENT_REVIEW_PATH, 'unexpected component review path')
    raw = inside(root, reference['path']).read_bytes()
    require(hashlib.sha256(raw).hexdigest() == reference['sha256'], 'component review checksum')
    review = json.loads(raw)
    require(review['schema'] == 'akashicnet.omni-component-archive-review.v1', 'component review schema')
    require(review['reviewer_type'] == 'AI_ASSISTED_NOT_INDEPENDENT'
            and review['evidence_use'] == 'READ_ONLY_TASK_INSPECTION_NOT_REDISTRIBUTION_OR_NEW_RETENTION_APPROVAL'
            and review['status'] == 'PARTIAL_PRESERVED_REPRESENTATION_FULL_BUNDLES_PENDING',
            'component review authority boundary')
    require(review['public_status'] == 'HOLD' and review['content_committed'] is False
            and review['complete_original_references_verified'] == 0,
            'component review promotion boundary')
    require(review['manual_sha256'] == next(a['sha256'] for a in manifest['http_assets']
                                          if a['id'] == 'manual'), 'component review manual mismatch')
    artifacts = review['artifacts']
    by_id = {a['id']: a for a in artifacts}
    require(len(by_id) == len(artifacts) == len({a['filename'] for a in artifacts}) == 5,
            'supporting artifact inventory')
    for a in artifacts:
        require(set(a) <= {'id', 'filename', 'representation', 'sha256', 'size_bytes',
                           'original_reddit_source', 'public_content_redistribution_approved', 'member'},
                'unapproved supporting artifact content')
        require(a['original_reddit_source'] is False
                and a['public_content_redistribution_approved'] is False
                and a['representation'] == 'preserved_first_party_artifact',
                'supporting artifact is not an original source or rights grant')
        require(re.fullmatch(r'[0-9a-f]{64}', a['sha256']) and a['size_bytes'] > 0,
                'invalid supporting artifact pin')
        require(a['filename'] == Path(a['filename']).name, 'invalid supporting artifact filename')
        if 'member' in a:
            m = a['member']
            require(set(m) == {'filename', 'sha256', 'size_bytes', 'representation',
                               'complete_source', 'capture_timestamp_verified', 'target_url_visible'},
                    'unapproved screenshot content')
            require(m['representation'] == 'partial_screenshot' and m['complete_source'] is False
                    and m['capture_timestamp_verified'] is False and m['target_url_visible'] is False,
                    'partial capture cannot establish complete source identity or time')
            require(m['filename'] == Path(m['filename']).name
                    and re.fullmatch(r'[0-9a-f]{64}', m['sha256']) and m['size_bytes'] > 0,
                    'invalid screenshot pin')
    expected = {}
    for c in manifest['component_register']:
        for index, r in enumerate(c['references']):
            parts = r['url'].rstrip('/').split('/')
            post_id = parts[parts.index('comments') + 1]
            comment_id = parts[-1] if 'comment' in parts else None
            ident = 'reddit:' + ('t1_' + comment_id if comment_id else 't3_' + post_id)
            require(r['archive_dependency_id'] == ident, 'component dependency identity')
            row = expected.setdefault(ident, {'url': r['url'], 'post_id': post_id,
                                             'comment_id': comment_id, 'bindings': []})
            require(row['url'] == r['url'], 'shared component locator mismatch')
            row['bindings'].append({'component': c['component'], 'version_label': r['version_label'],
                                    'role': 'original' if index == 0 else 'clarification'})
    dependencies = review['dependencies']
    actual = {d['id']: d for d in dependencies}
    require(len(actual) == len(dependencies) == review['distinct_dependencies'] == 13
            and set(actual) == set(expected) and review['reference_bindings'] == 14,
            'component dependency coverage')
    required = {'FULL_ARCHIVED_REPRESENTATION', 'EXACT_TARGET_BINDING',
                'CAPTURE_TIME_AND_VERSION_EVIDENCE', 'REPRODUCIBLE_BYTE_INTEGRITY',
                'SCOPE_SPECIFIC_USE_PERMISSION', 'RETENTION_DELETION_AND_SUPPRESSION_PLAN'}
    for ident, d in actual.items():
        require(set(d) <= {'id', 'url', 'post_id', 'comment_id', 'bindings', 'status',
                           'original_bytes_sha256', 'historical_capture_timestamp',
                           'current_reddit_equivalence', 'rights_clearance', 'retention_and_deletion',
                           'required_evidence', 'supporting_artifacts', 'partial_capture_scope'},
                'unapproved component source content')
        require(all(d[k] == v for k, v in expected[ident].items()), 'component dependency binding')
        require(d['status'] == 'PENDING_AUTHORIZED_ARCHIVED_BYTES'
                and d['original_bytes_sha256'] is None and d['historical_capture_timestamp'] is None,
                'unverified historical source promoted')
        require(d['current_reddit_equivalence'] == 'NOT_CHECKED_REDDIT_HOLD'
                and d['rights_clearance'] == 'PENDING_SCOPE_SPECIFIC_DECISION'
                and d['retention_and_deletion'] == 'PENDING_CONTROLLED_STORAGE_DECISION',
                'source access or retention boundary')
        require(set(d['required_evidence']) == required and set(d['supporting_artifacts']) <= set(by_id),
                'component missing-evidence contract')
    reconciliation = review['manual_reconciliation']
    require(len(reconciliation) == len(manifest['component_register']), 'reconciliation coverage')
    for r, c in zip(reconciliation, manifest['component_register']):
        require(r['component'] == c['component'] and r['manual_scope'] == c['scope']
                and r['declared_reference_bindings'] == 'MATCH_PINNED_MANUAL'
                and r['complete_component_semantics'] == 'NOT_VERIFIED_MISSING_FULL_SOURCES',
                'unsupported component semantic verification')
    verified = 0
    if private_evidence_directory is not None:
        directory = Path(private_evidence_directory).resolve()
        require(not directory.is_relative_to(Path(root).resolve()), 'private evidence inside checkout')
        for a in artifacts:
            path = inside(directory, a['filename'])
            check_bytes(path.read_bytes(), a)
            if 'member' in a:
                with zipfile.ZipFile(path) as archive:
                    m = a['member']
                    require(archive.getinfo(m['filename']).file_size == m['size_bytes'], 'member byte length')
                    check_bytes(archive.read(m['filename']), m)
            verified += 1
    return {'component_archive_dependencies_pending': len(dependencies),
            'supporting_artifact_bodies_verified': verified,
            'complete_original_component_references_verified': 0}


def verify_repository(root=ROOT, capture_directory=None, sites_checkout=None,
                      private_component_evidence_directory=None):
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
    component_review = verify_component_review(root, manifest, private_component_evidence_directory)
    return {**component_review, 'bundled_http_bodies_verified': bundled, 'http_descriptors': len(assets),
            'external_http_bodies_verified': external, 'sites_source_blobs_verified': source_count,
            'component_bundles_complete': False, 'method_pin_gate_complete': False,
            'question_status': 'UNRESOLVED', 'real_pilot_status': 'HOLD'}


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--capture-directory', type=Path, help='Optional original HTTP bodies, read only')
    p.add_argument('--sites-checkout', type=Path, help='Optional authorized source Git repository, read only')
    p.add_argument('--private-component-evidence-directory', type=Path,
                   help='Optional preserved supporting artifacts outside checkout, read only; no original-source promotion')
    args = p.parse_args()
    try:
        print(json.dumps(verify_repository(capture_directory=args.capture_directory,
                                           sites_checkout=args.sites_checkout,
                                           private_component_evidence_directory=args.private_component_evidence_directory), sort_keys=True))
    except (ValueError, KeyError, StopIteration, OSError, zipfile.BadZipFile, subprocess.CalledProcessError) as exc:
        p.exit(1, str(exc) + '\n')

