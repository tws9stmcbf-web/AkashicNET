"""Preserve the narrow IONS email conditions; not a live-page compliance audit."""
import json
from pathlib import Path
import unittest

RECORD = Path(__file__).resolve().parents[1] / "references/community/ions-vision-for-humanity-rights.json"

class IonsPresentationRightsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.record = json.loads(RECORD.read_text(encoding="utf-8"))

    def test_presentation_and_permission_provenance(self):
        self.assertEqual(self.record["presentation"]["review_url"],
                         "https://akashicnet.org/noetic-sciences/vision-for-humanity")
        self.assertEqual(self.record["presentation"]["presenter"], "Dr. Helané Wahbeh")
        self.assertEqual(self.record["provenance"]["authority"], "IONS Programs Team")
        self.assertEqual(self.record["provenance"]["permission_email_date"], "2026-10-05")

    def test_link_and_commentary_without_slide_reproduction(self):
        conditions = self.record["conditions"]
        self.assertEqual(conditions["treatment"], "link-and-commentary-only")
        self.assertEqual(conditions["individual_slide_images"], {
            "reproduce": False, "display": False,
            "platforms": ["AkashicNET", "r/NeuronsToNirvana"]})

    def test_required_notice_and_specific_presentation_link(self):
        conditions = self.record["conditions"]
        self.assertEqual(conditions["non_endorsement"], {
            "required": True, "placement": "top-of-page",
            "statement": "The Institute of Noetic Sciences (IONS) does not endorse this review or commentary."})
        self.assertEqual(conditions["presentation_link"], {
            "required": True, "placement": "bottom-of-page",
            "target": "specific official ConnectIONS Live presentation recording/page",
            "general_page_sufficient": False})

    def test_no_permission_expansion(self):
        scope = self.record["scope"]
        self.assertEqual(scope["applies_only_to"],
                         "This presentation and the reviewed AkashicNET treatment")
        for key in ("broader_reuse_granted", "third_party_image_rights_granted", "ions_endorsement"):
            self.assertIs(scope[key], False)

if __name__ == "__main__":
    unittest.main()
