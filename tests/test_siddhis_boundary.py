"""Mutation regressions for the question-only hold, not evidence approval."""
import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('siddhis_boundary', ROOT / 'scripts/validate_siddhis_boundary.py')
boundary = importlib.util.module_from_spec(spec)
spec.loader.exec_module(boundary)


class SiddhisBoundaryTests(unittest.TestCase):
    def setUp(self):
        self.page = boundary.PAGE.read_text(encoding='utf-8')

    def test_question_only_page_passes(self):
        boundary.validate(self.page)

    def test_mutable_reddit_searches_fail(self):
        for url in (
            'https://www.reddit.com/r/NeuronsToNirvana/search/?q=meditation&restrict_sr=1',
            'https://old.reddit.com/search?q=siddhis',
        ):
            with self.subTest(url=url), self.assertRaises(ValueError):
                boundary.validate(self.page.replace('</main>', f'<a href="{url}">Candidate connection</a></main>'))

    def test_unassessed_semantic_connections_fail(self):
        for post in ('1hcvvjs', '17zzx4k'):
            with self.subTest(post=post), self.assertRaises(ValueError):
                boundary.validate(self.page.replace('</main>', f'<a href="https://www.reddit.com/r/NeuronsToNirvana/comments/{post}/">Siddhis candidate</a></main>'))
        with self.assertRaises(ValueError):
            boundary.validate(self.page.replace('No community records are approved', 'The frozen UNASSESSED local record is approved'))

    def test_unsupported_evidence_assertions_fail(self):
        for claim in (
            'Established historical fact',
            'Meditation can affect attention and measurable brain activity.',
            'Traditional significance is established.',
            '<a href="https://doi.org/10.1016/j.neubiorev.2016.03.021">Scientific support</a>',
            'This evidence is supported by unregistered reference SRC-NEW.',
        ):
            with self.subTest(claim=claim), self.assertRaises(ValueError):
                boundary.validate(self.page.replace('</main>', f'<p>{claim}</p></main>'))

    def test_status_and_gate_relaxations_fail(self):
        for before, after in (
            ('UNRESOLVED', 'RESOLVED'), ('remains HOLD', 'is OPEN'),
            ('remain CLOSED', 'are OPEN'), ('edges remain 0', 'edges remain 1'),
            ('supports_models remains empty', 'supports_models includes model A'),
            ('Private material is prohibited.', 'Private material is permitted.'),
        ):
            with self.subTest(before=before), self.assertRaises(ValueError):
                boundary.validate(self.page.replace(before, after))


if __name__ == '__main__':
    unittest.main()
