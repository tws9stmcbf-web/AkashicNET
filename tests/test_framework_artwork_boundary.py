"""Regression gate: unresolved artwork cannot enter public serving."""
import copy
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPECTED = {
    'human2-hero.webp', 'human2-fig1-evidence-commons.webp',
    'human2-fig2-seven-lenses-domains.webp', 'human2-fig3-7x7-matrix.webp',
    'human2-fig4-flourishing-2100.webp', 'human2-fig5-buddhafly-effect.webp',
    'metad-ak-hero.webp', 'metad-ak-fig1-multi-ai-architecture.webp',
    'metad-ak-fig2-capabilities-boundaries.webp',
}


def validate_hold(review, public_names, page_text):
    assert review['decision'] == 'HOLD'
    assets = review['assets']
    assert len(assets) == len(EXPECTED)
    assert {a['filename'] for a in assets} == EXPECTED
    for a in assets:
        assert re.fullmatch(r'[a-f0-9]{64}', a['sha256'])
        assert re.fullmatch(r'[a-f0-9]{40}', a['source_blob_sha'])
        assert a['source_commit'] == 'a144c74e7d0a9afe009d124be67a02f2da13a53f'
        assert a['source_path'] == 'website/public/images/' + a['filename']
        assert a['creator_provenance'].startswith('UNVERIFIED:')
        assert a['public_visibility'].startswith('UNVERIFIED:')
        assert a['sensitivity_review'].startswith('HOLD:')
        assert a['rights_reuse'].startswith('HOLD:')
        assert a['public_manifest_acceptance'] == 'HOLD'
        assert a['served'] is False
        assert a['filename'] not in public_names
        assert a['filename'] not in page_text


class ArtworkBoundaryTests(unittest.TestCase):
    def setUp(self):
        self.review = json.loads((ROOT / 'website/assets/framework-artwork-review.json').read_text())

    def test_held_artwork_is_not_served_or_embedded(self):
        names = {p.name for p in (ROOT / 'website/public').rglob('*') if p.is_file()}
        pages = '\n'.join(p.read_text() for p in (ROOT / 'website/app').rglob('*.tsx'))
        validate_hold(self.review, names, pages)
        manifest = (ROOT / 'website/assets/MANIFEST.md').read_text()
        for asset in self.review['assets']:
            self.assertIn(f"| `{asset['filename']}` | `{asset['sha256']}` |", manifest)
        self.assertIn('Snapshot date: 12 September 2026', manifest)
        self.assertIn('30 August 2026 (original deployed-asset table below only)', manifest)

    def test_reintroducing_any_held_binary_or_embed_fails(self):
        for filename in EXPECTED:
            with self.subTest(filename=filename):
                with self.assertRaises(AssertionError):
                    validate_hold(self.review, {filename}, '')
                with self.assertRaises(AssertionError):
                    validate_hold(self.review, set(), f'<img src="/images/{filename}"/>')

    def test_missing_dispositions_or_premature_promotion_fail(self):
        for field, value in [('public_manifest_acceptance', 'ACCEPTED'), ('served', True),
                             ('rights_reuse', ''), ('sensitivity_review', ''),
                             ('creator_provenance', ''), ('public_visibility', '')]:
            with self.subTest(field=field):
                changed = copy.deepcopy(self.review)
                changed['assets'][0][field] = value
                with self.assertRaises(AssertionError):
                    validate_hold(changed, set(), '')

    def test_archive_checkpoint_and_inbound_links(self):
        page = (ROOT / 'website/app/human-2/page.tsx').read_text()
        structural = json.loads((ROOT / 'references/community/reddit-corpus-structural-checkpoint-v0.2.json').read_text())
        unified = json.loads((ROOT / 'references/community/unified-index-rebuild-v0.2.json').read_text())
        rows = structural['source_rows']
        drive = unified['sources']['drive']['records']
        total = unified['recount']['current_unified_index_records']
        self.assertEqual(rows + drive, total)
        self.assertIn(f'{rows:,} Reddit source rows + {drive:,} Drive rows = {total:,} unified records', page)
        self.assertIn(f"{structural['unique_canonical_post_urls_all_subreddits']:,} structurally unique Reddit URLs", page)
        self.assertIn('2 September 2026 checkpoint', page)
        self.assertNotIn('12,058', page)
        about = (ROOT / 'website/app/about/page.tsx').read_text()
        for route in ('human-2', 'metad-ak'):
            self.assertIn(f'href="/{route}"', about)
            self.assertTrue((ROOT / f'website/app/{route}/page.tsx').is_file())


if __name__ == '__main__':
    unittest.main()
