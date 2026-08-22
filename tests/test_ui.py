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

    def test_desktop_workspace_contains_three_named_regions(self):
        css = midnight_aurora_css()
        self.assertIn('.st-key-control_rail,.st-key-analysis_workspace,.st-key-document_inspector', css)
        self.assertIn('min-height:min(680px,calc(100vh - 190px)) !important', css)

    def test_document_inspector_fits_tall_images_without_inner_scrolling(self):
        css = midnight_aurora_css()
        self.assertIn('.st-key-document_stage {', css)
        self.assertIn('height:min(54vh,540px) !important', css)
        self.assertIn('overflow:hidden !important', css)
        self.assertIn('max-width:100% !important', css)
        self.assertIn('height:auto !important', css)
        self.assertIn('max-height:min(50vh,500px) !important', css)
        self.assertIn('object-fit:contain', css)
        self.assertIn('.st-key-document_inspector [data-testid="stPopover"] button', css)
        self.assertNotIn('.st-key-document_preview', css)


if __name__ == "__main__":
    unittest.main()
