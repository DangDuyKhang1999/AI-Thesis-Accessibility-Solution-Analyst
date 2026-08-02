import unittest

from accessibility_analyst.models import (
    ComponentType,
    LanguageCode,
    StructuredDescription,
    VisualComponent,
)
from accessibility_analyst.summarizer import (
    GeminiSummarizer,
    ensure_fact_coverage,
    replace_numbered_sections,
)


class FakeModels:
    def generate_content(self, **kwargs):
        self.prompt = kwargs["contents"]
        return type("Response", (), {"text": "Đây là bản phân tích ngắn gọn, có kết luận rõ ràng."})()


class SummarizerTests(unittest.TestCase):
    def test_replaces_numbered_sections_with_spoken_labels(self):
        narrative = (
            "1. Biểu đồ thể hiện thị phần.\n\n"
            "2. A chiếm 34%, B chiếm 31%.\n\n"
            "3. A cao hơn B 3 điểm phần trăm.\n\n"
            "4. A dẫn đầu và D thấp nhất."
        )

        result = replace_numbered_sections(narrative, LanguageCode.VIETNAMESE)

        self.assertIn("Tổng quan: Biểu đồ", result)
        self.assertIn("Số liệu chi tiết: A chiếm", result)
        self.assertIn("Phân tích số liệu: A cao hơn", result)
        self.assertIn("Nhận định: A dẫn đầu", result)
        self.assertNotRegex(result, r"(?m)^\s*[1-4][.)]\s")

    def test_does_not_append_fact_when_label_and_value_are_already_spoken(self):
        description = StructuredDescription(
            source_language=LanguageCode.VIETNAMESE,
            target_language=LanguageCode.VIETNAMESE,
            summary="raw",
            components=[VisualComponent(
                component_type=ComponentType.CHART,
                label="Thị phần nhà cung cấp",
                facts=["Nhà cung cấp A: 34%", "Nhà cung cấp B: 31%"],
                relationships=[],
            )],
        )
        narrative = "Số liệu chi tiết: Nhà cung cấp A chiếm 34% thị phần. Nhà cung cấp B chiếm 31% thị phần."

        result = ensure_fact_coverage(narrative, description)

        self.assertEqual(narrative, result)

    def test_appends_every_fact_missing_from_generated_narrative(self):
        description = StructuredDescription(
            source_language=LanguageCode.VIETNAMESE,
            target_language=LanguageCode.VIETNAMESE,
            summary="raw",
            components=[VisualComponent(
                component_type=ComponentType.CHART,
                label="Doanh số theo quý",
                facts=["Quý 1: $20.000", "Quý 2: $24.000", "Quý 3: $27.000", "Quý 4: $32.000"],
                relationships=["Tăng dần theo quý"],
            )],
        )
        narrative = "Doanh số tăng đều. Quý 1: $20.000 và Quý 4: $32.000."
        result = ensure_fact_coverage(narrative, description)
        self.assertEqual(result.count("Quý 1: $20.000"), 1)
        self.assertIn("Quý 2: $24.000", result)
        self.assertIn("Quý 3: $27.000", result)
        self.assertEqual(result.count("Quý 4: $32.000"), 1)

    def test_appends_relationships_missing_from_generated_narrative(self):
        description = StructuredDescription(
            source_language=LanguageCode.ENGLISH,
            target_language=LanguageCode.VIETNAMESE,
            summary="raw",
            components=[VisualComponent(
                component_type=ComponentType.CHART,
                label="Chỉ số theo kỳ",
                facts=["Kỳ A: 10", "Kỳ B: 15"],
                relationships=["Tăng 5 đơn vị", "Kỳ B cao hơn Kỳ A 50 phần trăm"],
            )],
        )
        result = ensure_fact_coverage("Biểu đồ thể hiện chỉ số tăng. Kỳ A: 10; Kỳ B: 15.", description)
        self.assertIn("Tăng 5 đơn vị", result)
        self.assertIn("Kỳ B cao hơn Kỳ A 50 phần trăm", result)

    def test_prompt_requires_overview_data_analysis_and_objective_interpretation(self):
        service = GeminiSummarizer.__new__(GeminiSummarizer)
        service.client = type("Client", (), {"models": FakeModels()})()
        service.model = "test-model"
        description = StructuredDescription(
            source_language=LanguageCode.ENGLISH,
            target_language=LanguageCode.VIETNAMESE,
            summary="raw",
            components=[],
        )
        service.summarize(description, LanguageCode.VIETNAMESE)
        prompt = service.client.models.prompt.lower()
        self.assertIn("câu tổng quan", prompt)
        self.assertIn("toàn bộ dữ kiện", prompt)
        self.assertIn("chênh lệch", prompt)
        self.assertIn("nhận định khách quan", prompt)
        self.assertIn("không suy đoán nguyên nhân", prompt)
        self.assertIn("tổng quan:", prompt)
        self.assertNotIn("phần 1", prompt)

    def test_english_output_prompt_uses_english_spoken_labels(self):
        service = GeminiSummarizer.__new__(GeminiSummarizer)
        service.client = type("Client", (), {"models": FakeModels()})()
        service.model = "test-model"
        description = StructuredDescription(
            source_language=LanguageCode.VIETNAMESE,
            target_language=LanguageCode.ENGLISH,
            summary="raw",
            components=[],
        )

        service.summarize(description, LanguageCode.ENGLISH)

        prompt = service.client.models.prompt
        self.assertIn('"Overview:"', prompt)
        self.assertIn('"Detailed data:"', prompt)
        self.assertIn('"Data analysis:"', prompt)
        self.assertIn('"Observation:"', prompt)

    def test_builds_analyst_summary_from_structured_data(self):
        service = GeminiSummarizer.__new__(GeminiSummarizer)
        service.client = type("Client", (), {"models": FakeModels()})()
        service.model = "test-model"
        description = StructuredDescription(
            source_language=LanguageCode.VIETNAMESE,
            target_language=LanguageCode.VIETNAMESE,
            summary="raw",
            components=[VisualComponent(
                component_type=ComponentType.TABLE,
                label="Nhóm dữ liệu",
                facts=["Nhóm A: mục 1", "Nhóm A: mục 2", "Nhóm B: mục 3"],
                relationships=["Các mục có thứ tự và quan hệ nhóm"],
            )],
        )
        result = service.summarize(description, LanguageCode.VIETNAMESE)
        self.assertIn("phân tích", result)
        prompt = service.client.models.prompt
        self.assertIn("một câu", prompt.lower())
        self.assertIn("từng mục", prompt.lower())
        self.assertIn("không bỏ sót", prompt.lower())
        self.assertIn("nhãn, khóa hoặc thuộc tính lặp lại", prompt.lower())
        self.assertIn("Nhóm A: mục 1", prompt)


if __name__ == "__main__":
    unittest.main()
