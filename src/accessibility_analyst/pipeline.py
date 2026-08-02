from .analyzer import VisualAnalyzer
from .language_service import render_description
from .models import AccessibilityResult, LanguageCode


class AccessibilityPipeline:
    def __init__(self, analyzer: VisualAnalyzer, summarizer, speech):
        self.analyzer = analyzer
        self.summarizer = summarizer
        self.speech = speech

    def run(self, image_bytes: bytes, mime_type: str, source_language: LanguageCode | None,
            target_language: LanguageCode) -> AccessibilityResult:
        description = self.analyzer.analyze_visual(
            image_bytes, mime_type, source_language, target_language
        )
        summary = self.summarizer.summarize(description, target_language)
        description = description.model_copy(update={"summary": summary})
        text = render_description(description)
        audio_bytes, audio_mime = self.speech.synthesize(text, target_language)
        return AccessibilityResult(
            description=description,
            rendered_text=text,
            audio_bytes=audio_bytes,
            audio_mime_type=audio_mime,
        )
