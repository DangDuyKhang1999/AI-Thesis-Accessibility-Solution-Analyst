import unittest

from accessibility_analyst.analyzer import GeminiAnalyzerClient, VisualAnalyzer
from accessibility_analyst.language_service import render_description
from accessibility_analyst.models import ComponentType, LanguageCode
from accessibility_analyst.pipeline import AccessibilityPipeline


class FakeAnalyzerClient:
    def analyze(self, image_bytes, mime_type, source_language, target_language):
        return {
            "source_language": (source_language or LanguageCode.ENGLISH).value,
            "target_language": target_language.value,
            "summary": "Quarterly revenue chart.",
            "components": [{
                "component_type": "chart",
                "label": "Revenue",
                "facts": ["Q1: 10", "Q2: 15"],
                "relationships": ["Q2 is higher than Q1"],
            }],
        }


class FakeSpeech:
    def synthesize(self, text, language):
        return b"audio", "audio/mpeg"


class FakeSummarizer:
    def summarize(self, description, target_language):
        return "Revenue increased overall. The chart shows Q1 at 10 and Q2 at 15, with Q2 higher than Q1."


class FakeGeminiModels:
    def generate_content(self, **kwargs):
        self.prompt = kwargs["contents"][0]
        return type("Response", (), {"text": '{"source_language":"ja","target_language":"vi","summary":"Sơ đồ","components":[]}'})()


class FakeGeminiSdkClient:
    def __init__(self):
        self.models = FakeGeminiModels()


class ProductionPipelineTests(unittest.TestCase):
    def test_analyzer_allows_automatic_source_language_detection(self):
        client = GeminiAnalyzerClient.__new__(GeminiAnalyzerClient)
        client.client = FakeGeminiSdkClient()
        client.model = "test-model"
        payload = client.analyze(b"image", "image/png", None, LanguageCode.VIETNAMESE)
        self.assertEqual(payload["source_language"], "ja")
        self.assertIn("detect", client.client.models.prompt.lower())
        self.assertIn("absolute and percentage", client.client.models.prompt.lower())

    def test_gemini_client_uses_supported_default_model(self):
        client = GeminiAnalyzerClient("test-key")
        self.assertEqual(client.model, "gemini-2.5-flash-lite")

    def test_analyzer_returns_structured_description(self):
        result = VisualAnalyzer(FakeAnalyzerClient()).analyze_visual(
            b"image", "image/png", LanguageCode.ENGLISH, LanguageCode.VIETNAMESE
        )
        self.assertEqual(result.components[0].component_type, ComponentType.CHART)
        self.assertEqual(result.components[0].facts, ["Q1: 10", "Q2: 15"])

    def test_render_description_uses_composed_narrative_without_rebuilding_components(self):
        description = VisualAnalyzer(FakeAnalyzerClient()).analyze_visual(
            b"image", "image/png", LanguageCode.ENGLISH, LanguageCode.ENGLISH
        )
        text = render_description(description)
        self.assertEqual(text, "Quarterly revenue chart.")
        self.assertNotIn("Q1: 10", text)
        self.assertNotIn("Q2 is higher than Q1", text)

    def test_pipeline_returns_text_components_and_audio(self):
        pipeline = AccessibilityPipeline(
            analyzer=VisualAnalyzer(FakeAnalyzerClient()),
            summarizer=FakeSummarizer(),
            speech=FakeSpeech(),
        )
        result = pipeline.run(
            b"image", "image/png", LanguageCode.ENGLISH, LanguageCode.VIETNAMESE
        )
        self.assertEqual(result.audio_bytes, b"audio")
        self.assertEqual(result.description.components[0].label, "Revenue")
        self.assertEqual(
            result.rendered_text,
            "Revenue increased overall. The chart shows Q1 at 10 and Q2 at 15, with Q2 higher than Q1.",
        )
        self.assertIn("Q1 at 10", result.rendered_text)
        self.assertIn("Q2 higher than Q1", result.rendered_text)


if __name__ == "__main__":
    unittest.main()
