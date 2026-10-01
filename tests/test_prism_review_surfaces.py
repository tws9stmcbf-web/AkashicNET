"""Draft inquiry schema and repository release consistency regressions."""
import copy
import json
from pathlib import Path
import unittest

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]


class ReviewSurfaceTests(unittest.TestCase):
    def test_inquiry_schema_fixture_and_required_contracts(self):
        schema = json.loads((ROOT / 'schemas/akashic-prism-inquiry-module-v0.1.schema.json').read_text())
        Draft202012Validator.check_schema(schema)
        validator = Draft202012Validator(schema)
        fixture = json.loads((ROOT / 'tests/fixtures/prism/inquiry-module-hold.json').read_text())
        self.assertEqual(list(validator.iter_errors(fixture)), [])
        for field in schema['required']:
            with self.subTest(field=field):
                record = copy.deepcopy(fixture)
                del record[field]
                self.assertFalse(validator.is_valid(record))
        for field, value in [('automatic_subject_status_inference_allowed', True),
                             ('rights_review_required', False),
                             ('publication_status', 'published')]:
            record = copy.deepcopy(fixture)
            record['ethical_governance'][field] = value
            self.assertFalse(validator.is_valid(record))

    def test_absent_release_surface_requires_unverified_register(self):
        # Repository approval cannot be inferred from a historical external report.
        artifact = ROOT / 'website/public/releases/akashicprism-v0.2.json'
        self.assertFalse(artifact.exists())
        page = (ROOT / 'website/app/insights/akashicprism-big-questions/page.tsx').read_text()
        self.assertIn('DRAFT v0.1', page)
        self.assertNotIn('id="release"', page)
        register = (ROOT / 'references/knowledge-governance/AKASHIC_ECOSYSTEM_VERSION_REGISTER.md').read_text()
        self.assertIn('Repository release status is UNVERIFIED and publication remains HOLD', register)
        self.assertNotIn('AKN-FW-003 now has public pre-alpha release profile v0.2', register)


if __name__ == '__main__':
    unittest.main()
