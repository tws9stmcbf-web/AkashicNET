"""Temporary no-new-artwork gate; reopening requires a separately reviewed change.

No candidate fingerprint is stored here. Freeze existing asset locations/content
against the pre-feature base and reject new binary content anywhere in Git,
including intermediate commits. This deliberately fails closed for other new
artwork too while the publication incident remains unresolved.
"""
from pathlib import Path
import re
import subprocess
import unittest

ROOT = Path(__file__).resolve().parents[1]
BASE = '08dab15f0f0f9582bb73cb2d482efa9ad54cafa6'
MEDIA = {'.webp', '.png', '.jpg', '.jpeg', '.gif', '.svg', '.avif', '.ico', '.pdf', '.mp4', '.woff', '.woff2'}


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT)


def tree(ref):
    entries = {}
    for record in git('ls-tree', '-rz', ref).split(b'\0'):
        if record:
            meta, path = record.split(b'\t', 1)
            mode, kind, oid = meta.split()
            entries[path.decode()] = (mode, kind, oid.decode())
    return entries


def check_file(path, mode, data, baseline):
    """An unchanged baseline file is allowed; no relocated asset inherits approval."""
    if baseline == (mode, data):
        return
    if mode != b'100644' and mode != b'100755':
        raise ValueError('New symlink/submodule is not permitted')
    if path.startswith('website/public/') or Path(path).suffix.lower() in MEDIA:
        raise ValueError('New or changed served/media asset is withheld')
    try:
        text = data.decode('utf-8')
    except UnicodeDecodeError:
        raise ValueError('New binary content is withheld') from None
    if '\0' in text:
        raise ValueError('New binary content is withheld')
    if path.startswith('website/') and re.search(r'data\s*:|base64|atob\s*\(|Buffer\.from', text, re.I):
        raise ValueError('Encoded inline payload requires separate review')


class SpiritPublicationBoundaryTests(unittest.TestCase):
    def test_all_intermediate_commits_and_current_tree(self):
        base = tree(BASE)
        cache = {}
        def blob(oid):
            if oid not in cache:
                cache[oid] = git('cat-file', 'blob', oid)
            return cache[oid]
        git('merge-base', '--is-ancestor', BASE, 'HEAD')
        for ref in git('rev-list', BASE + '..HEAD').decode().splitlines() + ['HEAD']:
            for path, (mode, kind, oid) in tree(ref).items():
                if base.get(path) == (mode, kind, oid):
                    continue
                self.assertEqual(kind, b'blob', 'New submodule is withheld')
                prior = base.get(path)
                check_file(path, mode, blob(oid), (prior[0], blob(prior[2])) if prior else None)
        # Include uncommitted tracked changes when used locally.
        for path in git('ls-files', '-z').decode().split('\0'):
            if path and (ROOT / path).exists():
                prior = base.get(path)
                p = ROOT / path
                mode = b'120000' if p.is_symlink() else b'100755' if p.stat().st_mode & 0o111 else b'100644'
                check_file(path, mode, p.read_bytes(), (prior[0], blob(prior[2])) if prior else None)

    def test_public_withholding_note_has_no_audit_identifier(self):
        manifest = (ROOT / 'website/assets/MANIFEST.md').read_text()
        note = next(line for line in manifest.splitlines() if 'withheld candidate' in line)
        self.assertNotRegex(note, r'[a-fA-F0-9]{64}|\.(webp|png|jpg)')
        for gate in ('PUBLIC_VERIFIED', 'sensitivity/PII review', 'reuse rights', 'ELIGIBLE', 'lineage'):
            self.assertIn(gate, note)

    def test_renamed_relocated_and_disguised_assets_fail(self):
        for path in ('website/public/renamed.webp', 'website/public/download', 'website/app/other/picture.webp', 'elsewhere/payload.txt'):
            with self.subTest(path=path), self.assertRaises(ValueError):
                check_file(path, b'100644', b'RIFF\x00synthetic\xffWEBP', None)

    def test_changed_existing_asset_and_symlink_fail(self):
        with self.assertRaises(ValueError):
            check_file('website/public/logo.svg', b'100644', b'<svg/>', (b'100644', b'old'))
        with self.assertRaises(ValueError):
            check_file('website/app/asset', b'120000', b'../../private', None)

    def test_inline_route_payload_fails(self):
        with self.assertRaises(ValueError):
            check_file('website/app/elsewhere/route.ts', b'100644', b'const image = "data:image/webp;base64,synthetic"', None)

    def test_unchanged_baseline_asset_passes(self):
        check_file('website/public/logo.webp', b'100644', b'\xff', (b'100644', b'\xff'))

    def test_workflow_has_no_path_filter_and_checks_exact_head(self):
        workflow = (ROOT / '.github/workflows/validate-spirit-publication-boundary.yml').read_text()
        self.assertNotRegex(workflow, r'paths(?:-ignore)?:')
        self.assertIn('fetch-depth: 0', workflow)
        self.assertIn('github.event.pull_request.head.sha || github.sha', workflow)
        self.assertIn('git rev-parse HEAD', workflow)

    def test_spirit_card_clears_absolute_mobile_header(self):
        page = (ROOT / 'website/app/spirit/page.tsx').read_text()
        self.assertIn('padding: "clamp(7rem,8vw,8rem) 0 70px"', page)


if __name__ == '__main__':
    unittest.main()
