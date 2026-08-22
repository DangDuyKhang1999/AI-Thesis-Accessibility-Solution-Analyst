# Danh mục thành phần

## Entry point và orchestration

- `app.py`: Streamlit entry point, load environment, tạo ba vùng desktop, adapt
  upload, lặp trang và render kết quả/preview trang đầu.
- `AccessibilityPipeline`: chạy analyzer → summarizer → renderer → speech cho một
  trang và trả `AccessibilityResult`.

## Input và extraction

- `InputAdapter`: nhận bytes, tên, MIME; giữ ảnh thành một `InputPage` hoặc render
  PDF sang PNG. Không có size/page limit.
- `UnsupportedInputError`: lỗi input rỗng, loại không hỗ trợ, PDF lỗi/rỗng.
- `AnalyzerClient`: protocol cho adapter extraction.
- `GeminiAnalyzerClient`: Google Gen AI adapter; prompt JSON, đọc `response.text`
  và gọi `json.loads`.
- `VisualAnalyzer`: Pydantic boundary bằng
  `StructuredDescription.model_validate`.

## Composition và output

- `GeminiSummarizer`: gửi components cùng metadata ngôn ngữ sang lượt Gemini thứ
  hai; analyzer summary bị loại khỏi payload composition.
- `replace_numbered_sections`: đổi marker `1–4` khớp regex thành nhãn Việt/Anh.
- `ensure_fact_coverage`: so khớp substring/tập token rồi nối facts hoặc
  relationships chưa khớp; không kiểm tra tương đương ngữ nghĩa.
- `render_description`: strip và trả narrative đang nằm trong trường `summary`.
- `SpeechService`: gTTS adapter, tạo temporary MP3 và trả bytes `audio/mpeg`.

## Data models

- `LanguageCode`: `en`, `ja`, `vi`; cùng enum được dùng cho source và target.
- `ComponentType`: `table`, `chart`, `diagram`, `layout`.
- `VisualComponent`: `component_type`, `label`, `facts`, `relationships`.
- `StructuredDescription`: `source_language`, `target_language`, `summary`,
  `components`. Analyzer đặt overview ban đầu vào `summary`; pipeline thay nó bằng
  narrative hoàn chỉnh.
- `InputPage`: `index`, `data`, `mime_type`.
- `InputDocument`: `source_name`, danh sách `pages` không rỗng.
- `AccessibilityResult`: `description`, `rendered_text`, `audio_bytes`,
  `audio_mime_type`. Audio fields cho phép `None` ở model, nhưng production
  pipeline chỉ tạo result sau khi speech thành công.

Pydantic cấm field dư và một số chuỗi rỗng; schema không có confidence,
unreadable-region hoặc ground-truth fields, và không yêu cầu component/fact lists
phải có phần tử.

## Presentation

- `midnight_aurora_css`: theme, widget overrides, ba named regions, inspector ảnh
  contain, breakpoint dưới 900px, focus styling và reduced-motion CSS.
- `apply_midnight_aurora`: inject CSS bằng `st.markdown`.
- `render_header`: hero và copy trạng thái.
- `render_status`: render status copy; caller chịu trách nhiệm nội dung.
