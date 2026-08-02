# Kiến trúc hiện tại

## Pipeline

`app.py` → `InputAdapter` → `VisualAnalyzer/GeminiAnalyzerClient` →
`StructuredDescription` → `GeminiSummarizer` → `SpeechService` →
`AccessibilityResult` → UI.

Danh sách công nghệ và trách nhiệm cụ thể nằm tại
[technology-stack.md](technology-stack.md). Luồng nghiệp vụ chi tiết và các bước
chuẩn hóa output nằm tại [spec.md](spec.md#luồng-hoạt-động-chi-tiết).

## Ranh giới module

- `models.py`: enum/schema Pydantic và validation.
- `input_adapter.py`: ảnh/PDF thành danh sách trang ảnh có thứ tự.
- `analyzer.py`: extraction đa phương thức thành JSON cấu trúc.
- `summarizer.py`: composition chi tiết từ JSON, chuẩn hóa nhãn section và bảo
  đảm coverage dữ kiện mà không nối lặp theo khác biệt dấu câu.
- `language_service.py`: lấy narrative đã composition để render.
- `speech.py`: narrative thành MP3 theo `vi` hoặc `en`.
- `pipeline.py`: điều phối dependency, không chứa Streamlit.
- `ui.py`: Midnight Aurora CSS và presentation helpers.
- `app.py`: state/interaction Streamlit và hiển thị kết quả.

## Invariants

- Source language là `en`, `ja` hoặc `vi` và do AI tự phát hiện.
- Target language do người dùng chọn `vi` hoặc `en`.
- Component type chỉ gồm table/chart/diagram/layout.
- Production code không import `archive/`.
- Key chỉ đọc từ `.env` tại project root.
- Extraction và composition là hai lượt AI riêng.
- Văn bản hiển thị và văn bản đưa vào TTS là cùng narrative sau hậu xử lý.
- Section của narrative dùng nhãn ngữ nghĩa theo target language, không dùng số
  `1–4` đứng riêng.

## Lỗi và phụ thuộc ngoài

Gemini và gTTS cần mạng. Schema sai bị Pydantic từ chối; lỗi hiện được `app.py`
hiển thị chung. Retry, timeout taxonomy, caching và observability chưa triển khai.
