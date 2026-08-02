import json
from typing import Protocol

from .models import LanguageCode, StructuredDescription


class AnalyzerClient(Protocol):
    def analyze(self, image_bytes: bytes, mime_type: str, source_language: LanguageCode | None,
                target_language: LanguageCode) -> dict: ...


class VisualAnalyzer:
    def __init__(self, client: AnalyzerClient):
        self.client = client

    def analyze_visual(self, image_bytes: bytes, mime_type: str,
                       source_language: LanguageCode | None,
                       target_language: LanguageCode) -> StructuredDescription:
        payload = self.client.analyze(image_bytes, mime_type, source_language, target_language)
        return StructuredDescription.model_validate(payload)


class GeminiAnalyzerClient:
    def __init__(self, api_key: str, model: str = "gemini-2.5-flash-lite"):
        from google import genai

        self.client = genai.Client(api_key=api_key)
        self.model = model

    def analyze(self, image_bytes: bytes, mime_type: str, source_language: LanguageCode | None,
                target_language: LanguageCode) -> dict:
        from google.genai import types

        target = "Vietnamese" if target_language == LanguageCode.VIETNAMESE else "English"
        source_instruction = (
            f"Source language is {source_language.value}."
            if source_language
            else "Detect whether the source language is English, Japanese, or Vietnamese."
        )
        source_code = source_language.value if source_language else "detected en|ja|vi code"
        prompt = f"""You are an accessibility analyst for blind employees.
Analyze this enterprise document or software UI. {source_instruction}
Return ONLY valid JSON in {target} with this exact shape:
{{"source_language":"{source_code}","target_language":"{target_language.value}",
"summary":"clear overview","components":[{{"component_type":"table|chart|diagram|layout",
"label":"name","facts":["exact values and labels"],"relationships":["spatial, trend, hierarchy or comparison"]}}]}}
Identify every meaningful table, chart, diagram and layout region. Preserve numbers and labels.
For numeric data, include relationships for minimum, maximum, direction or trend,
and calculate absolute and percentage differences when the values support them;
never omit intermediate data points and never infer causes not shown by the source.
The summary is the accessible spoken overview: write only 2 to 4 concise sentences,
state the purpose and the most important patterns or conclusions, and do not enumerate
or repeat the component facts. Put detailed values only in components. Within each
component, avoid repeating the same row/group prefix when a grouped relationship can
express it more clearly. Never output ellipses as a substitute for unreadable content;
state that the specific content is unreadable. Do not merely repeat OCR text or invent facts."""
        response = self.client.models.generate_content(
            model=self.model,
            contents=[prompt, types.Part.from_bytes(data=image_bytes, mime_type=mime_type)],
            config=types.GenerateContentConfig(response_mime_type="application/json"),
        )
        text = (response.text or "").strip()
        if not text:
            raise ValueError("LLM không trả về kết quả phân tích.")
        return json.loads(text)
