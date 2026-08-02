# Danh mục thành phần

## Application

- `app.py`: Streamlit entry point và workflow UI.
- `InputAdapter`: validation ảnh/PDF và phân trang.
- `VisualAnalyzer`: schema boundary cho extraction.
- `GeminiAnalyzerClient`: adapter Google multimodal API.
- `GeminiSummarizer`: composition mô tả chi tiết từ structured JSON.
- `replace_numbered_sections`: đổi marker phần `1–4` thành nhãn Việt/Anh có nghĩa.
- `ensure_fact_coverage`: bổ sung facts/relationships còn thiếu và nhận diện dữ
  kiện đã xuất hiện dù cách nối từ hoặc dấu câu khác nhau.
- `SpeechService`: gTTS adapter.
- `AccessibilityPipeline`: orchestration và kết quả cuối.

## Data models

- `LanguageCode`: `en`, `ja`, `vi`.
- `ComponentType`: table, chart, diagram, layout.
- `VisualComponent`: label, facts, relationships.
- `StructuredDescription`: ngôn ngữ, overview và components.
- `InputPage`/`InputDocument`: input nhiều trang.
- `AccessibilityResult`: description, narrative và audio.

## Presentation

- `midnight_aurora_css`: theme Glassmorphism responsive; quy ước chữ midnight
  trên bề mặt sáng và chữ gần trắng trên bề mặt tối.
- `apply_midnight_aurora`: inject theme.
- `render_header`: hero và trạng thái AI.
- `render_status`: copy trạng thái có style thống nhất.
