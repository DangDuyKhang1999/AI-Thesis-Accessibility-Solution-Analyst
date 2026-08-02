import re

from .models import LanguageCode, StructuredDescription


def _normalized(text: str) -> str:
    return " ".join(text.casefold().split())


def _content_tokens(text: str) -> set[str]:
    return set(re.findall(r"[^\W_]+", text.casefold(), flags=re.UNICODE))


def _is_covered(item: str, narrative: str) -> bool:
    if _normalized(item) in _normalized(narrative):
        return True
    required = _content_tokens(item)
    if not required:
        return True
    passages = re.split(r"[\n.!?;]+", narrative)
    return any(required <= _content_tokens(passage) for passage in passages)


def replace_numbered_sections(narrative: str, language: LanguageCode) -> str:
    labels = (
        ("Tổng quan", "Số liệu chi tiết", "Phân tích số liệu", "Nhận định")
        if language == LanguageCode.VIETNAMESE
        else ("Overview", "Detailed data", "Data analysis", "Observation")
    )

    def replace(match: re.Match[str]) -> str:
        section = int(match.group("section"))
        return f"{labels[section - 1]}: "

    return re.sub(
        r"(?m)^\s*(?:Phần\s+)?(?P<section>[1-4])\s*[.):\-]\s*",
        replace,
        narrative,
        flags=re.IGNORECASE,
    ).strip()


def ensure_fact_coverage(narrative: str, description: StructuredDescription) -> str:
    additions = []
    for component in description.components:
        missing = [fact for fact in component.facts if not _is_covered(fact, narrative)]
        missing_relationships = [
            relationship for relationship in component.relationships
            if not _is_covered(relationship, narrative)
        ]
        if missing:
            prefix = (
                f"Số liệu bổ sung cho {component.label}: "
                if description.target_language == LanguageCode.VIETNAMESE
                else f"Additional data for {component.label}: "
            )
            additions.append(prefix + ". ".join(missing) + ".")
        if missing_relationships:
            prefix = (
                f"Phân tích bổ sung cho {component.label}: "
                if description.target_language == LanguageCode.VIETNAMESE
                else f"Additional analysis for {component.label}: "
            )
            additions.append(prefix + ". ".join(missing_relationships) + ".")
    return "\n\n".join([narrative.strip(), *additions])


class GeminiSummarizer:
    def __init__(self, api_key: str, model: str = "gemini-2.5-flash-lite"):
        from google import genai

        self.client = genai.Client(api_key=api_key)
        self.model = model

    def summarize(self, description: StructuredDescription, target_language: LanguageCode) -> str:
        language = "tiếng Việt" if target_language == LanguageCode.VIETNAMESE else "English"
        section_labels = (
            ("Tổng quan", "Số liệu chi tiết", "Phân tích số liệu", "Nhận định")
            if target_language == LanguageCode.VIETNAMESE
            else ("Overview", "Detailed data", "Data analysis", "Observation")
        )
        overview_label, details_label, analysis_label, observation_label = section_labels
        structured_data = description.model_dump_json(exclude={"summary"}, indent=2)
        prompt = f"""Bạn là chuyên gia mô tả nội dung trực quan cho người khiếm thị.
Dựa duy nhất vào dữ liệu có cấu trúc bên dưới, hãy viết bản mô tả chi tiết bằng {language}.

Yêu cầu:
- Bắt đầu đoạn thứ nhất bằng đúng nhãn "{overview_label}:" và viết đúng một câu tổng quan nêu nội dung, ý nghĩa chính của toàn bộ tài liệu hoặc giao diện.
- Bắt đầu đoạn thứ hai bằng đúng nhãn "{details_label}:" rồi đọc toàn bộ dữ kiện: mô tả lần lượt từng thành phần và từng mục; không bỏ sót nhãn, số liệu hoặc đơn vị đã trích xuất.
- Mỗi chuỗi trong trường facts phải xuất hiện nguyên văn ít nhất một lần trong mô tả; không đổi chữ số thành chữ và không làm tròn số.
- Bắt đầu đoạn thứ ba bằng đúng nhãn "{analysis_label}:" rồi phân tích toàn bộ quan hệ: cấu trúc không gian, thứ bậc, trình tự, so sánh, xu hướng, giá trị cao nhất/thấp nhất và chênh lệch tuyệt đối hoặc phần trăm khi dữ liệu cho phép tính.
- Mỗi chuỗi trong trường relationships phải được diễn đạt ít nhất một lần.
- Bắt đầu đoạn cuối bằng đúng nhãn "{observation_label}:" và đưa ra nhận định khách quan trực tiếp từ số liệu và quan hệ; không suy đoán nguyên nhân, động cơ hoặc bối cảnh mà nguồn không cung cấp.
- Khi nhiều mục có cùng nhãn, khóa hoặc thuộc tính lặp lại, hãy gom chúng thành một nhóm trong câu văn rồi mô tả các giá trị con; không đọc lại tiền tố giống nhau cho từng mục.
- Không giả định tên nhóm hoặc cấu trúc cụ thể từ ví dụ bên ngoài; chỉ suy ra cách nhóm từ dữ liệu đầu vào hiện tại.
- Nếu dữ liệu có phần không đọc được, nói rõ phần cụ thể chưa xác định; không dùng dấu ba chấm thay cho nội dung.
- Dùng các đoạn văn có bố cục rõ, câu tự nhiên, dễ nghe qua TTS; độ dài tương ứng với lượng thông tin thực tế.
- Không dùng số thứ tự như "1.", "2.", "3.", "4.", không dùng bullet hoặc markdown. Bốn nhãn ngữ nghĩa trên là một phần tự nhiên của câu để người nghe hiểu đoạn tiếp theo nói về điều gì.

Dữ liệu có cấu trúc:
{structured_data}"""
        response = self.client.models.generate_content(model=self.model, contents=prompt)
        result = (response.text or "").strip()
        if not result:
            raise ValueError("LLM không trả về bản mô tả chi tiết.")
        result = replace_numbered_sections(result, target_language)
        return ensure_fact_coverage(result, description)
