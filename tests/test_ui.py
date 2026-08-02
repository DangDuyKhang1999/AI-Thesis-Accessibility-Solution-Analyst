import unittest

from accessibility_analyst.ui import midnight_aurora_css


class MidnightAuroraUiTests(unittest.TestCase):
    def test_css_has_glass_responsive_focus_and_reduced_motion(self):
        css = midnight_aurora_css()
        self.assertIn("backdrop-filter: blur", css)
        self.assertIn("@media (max-width: 900px)", css)
        self.assertIn(":focus-visible", css)
        self.assertIn("prefers-reduced-motion", css)

    def test_css_uses_midnight_aurora_palette(self):
        css = midnight_aurora_css()
        self.assertIn("#06111f", css)
        self.assertIn("#67e8f9", css)
        self.assertIn("#5eead4", css)

    def test_primary_button_text_cannot_be_overridden_to_white(self):
        css = midnight_aurora_css()
        self.assertIn('[data-testid="stBaseButton-primary"] p', css)
        self.assertIn("color: #02131b !important", css)

    def test_all_bright_aurora_surfaces_use_dark_readable_text(self):
        css = midnight_aurora_css()
        self.assertIn('[data-testid="stProgress"] [data-testid="stMarkdownContainer"] p', css)
        self.assertIn('[data-testid="stProgress"] p { color:#02131b !important;', css)
        self.assertIn('[data-testid="stFileUploaderDropzone"] button', css)
        self.assertIn('color:#02131b !important;', css)

    def test_dark_controls_and_feedback_keep_high_contrast_text(self):
        css = midnight_aurora_css()
        self.assertIn('[data-testid="stAlert"]', css)
        self.assertIn('[data-testid="stExpander"] summary', css)
        self.assertIn('[data-baseweb="select"]', css)
        self.assertIn('color:var(--text) !important;', css)


if __name__ == "__main__":
    unittest.main()
