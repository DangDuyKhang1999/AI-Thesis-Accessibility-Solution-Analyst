# Kiến trúc hiện tại

## Tổng quan công nghệ

Hệ thống là một Streamlit monolith có các service boundary rõ ràng trong package
Python. Pipeline dùng Gemini hai lần: lượt đầu phân tích hình ảnh thành dữ liệu có
cấu trúc, lượt sau diễn giải dữ liệu đó thành narrative dễ nghe. Pydantic kiểm tra
hình dạng dữ liệu giữa hai lượt; gTTS chuyển narrative cuối thành MP3.

| Tầng | Công nghệ | Vai trò |
| --- | --- | --- |
| Giao diện | Streamlit | Upload, lựa chọn ngôn ngữ và trình bày kết quả |
| Tài liệu | PyMuPDF | Render PDF thành các trang PNG |
| Phân tích | Google Gen AI SDK, Gemini | Nhận diện ngôn ngữ, component, dữ kiện và quan hệ |
| Kiểm tra shape | `json.loads`, Pydantic 2 | Parse JSON và kiểm tra schema; không xác minh factual accuracy |
| Diễn giải | Gemini và hậu xử lý heuristic | Tạo narrative có nhãn và giảm bỏ sót chuỗi dữ kiện |
| Âm thanh | gTTS | Tạo MP3 tiếng Việt hoặc tiếng Anh |
| Kiểm thử | `unittest` | Unit test và repository contract test |

Việc tách extraction và composition tạo ranh giới để đánh giá hai giai đoạn độc
lập. Repository hiện chưa có dataset hoặc rubric thực hiện phép đánh giá đó.

## Data flow theo trang

```text
upload
  → InputAdapter → InputDocument[InputPage...]
  → app.py lặp tuần tự từng InputPage
      → GeminiAnalyzerClient → dict từ JSON
      → VisualAnalyzer/Pydantic → StructuredDescription
      → GeminiSummarizer → narrative hậu xử lý
      → render_description → cùng narrative
      → SpeechService → MP3
      → AccessibilityResult
  → UI hiển thị kết quả theo thứ tự trang
```

Không có bước tổng hợp ở cấp toàn tài liệu. Với PDF nhiều trang, mỗi trang là một
request extraction, composition và speech độc lập. App chỉ bắt đầu render danh
sách result sau khi toàn bộ vòng lặp trang thành công; lỗi ở trang sau gọi
`st.stop()` nên các result đã tạo trước đó trong lần chạy đó cũng chưa được hiển
thị. Inspector chỉ hiển thị ảnh tham chiếu của trang đầu.

Luồng nghiệp vụ chi tiết nằm tại
[spec.md](spec.md#luồng-hoạt-động-chi-tiết).

## Ranh giới module

- `models.py`: enum và Pydantic models; `extra="forbid"`, một số chuỗi có
  `min_length`, nhưng lists có thể rỗng.
- `input_adapter.py`: kiểm tra loại input, giữ ảnh thành một trang hoặc render PDF
  sang PNG với PyMuPDF.
- `analyzer.py`: prompt Gemini trả JSON, `json.loads`, rồi `VisualAnalyzer` gọi
  `StructuredDescription.model_validate`.
- `summarizer.py`: yêu cầu Gemini composition từ components; thay marker section
  và nối facts/relationships chưa khớp bằng heuristic.
- `language_service.py`: `render_description` chỉ strip và trả
  `StructuredDescription.summary` hiện đã được pipeline thay bằng narrative.
- `speech.py`: gTTS ghi MP3 vào temporary file rồi trả bytes/MIME.
- `pipeline.py`: điều phối một trang, không chứa Streamlit.
- `ui.py`: CSS/presentation helpers Midnight Aurora.
- `app.py`: process environment, widgets, vòng lặp trang, lỗi và presentation.

## Thành phần chính

- `InputAdapter`: nhận PNG/JPEG/WebP hoặc render PDF thành các `InputPage` PNG.
- `GeminiAnalyzerClient`: gọi Gemini multimodal và parse JSON response.
- `VisualAnalyzer`: kiểm tra response qua `StructuredDescription`.
- `GeminiSummarizer`: tạo narrative từ structured components.
- `replace_numbered_sections` và `ensure_fact_coverage`: hậu xử lý best-effort.
- `SpeechService`: tạo MP3 bằng gTTS.
- `AccessibilityPipeline`: điều phối analyzer, summarizer, renderer và speech.
- `midnight_aurora_css` cùng các UI helper: presentation cho Streamlit.

Các model trung tâm gồm `InputDocument`, `InputPage`, `VisualComponent`,
`StructuredDescription` và `AccessibilityResult`. Schema cấm field dư và một số
chuỗi rỗng, nhưng component/fact list vẫn có thể rỗng và chưa có confidence hoặc
unreadable-region field.

## Contract thực tế

- UI chỉ cho target `vi` hoặc `en`. `LanguageCode` nội bộ cũng chứa `ja` và chưa
  có validator riêng cấm dùng Japanese làm target khi gọi pipeline trực tiếp.
- Khi source là `None`, prompt yêu cầu Gemini chọn `en`, `ja` hoặc `vi`; Pydantic
  từ chối mã ngoài enum nhưng không kiểm chứng model phát hiện đúng.
- Component type bị giới hạn ở `table`, `chart`, `diagram`, `layout`.
- Production source không import `archive/`; invariant này có repository test.
- `GEMINI_API_KEY` được lấy bằng `os.getenv`. `load_dotenv(ROOT / ".env")` chỉ hỗ
  trợ nạp file local vào process environment.
- Extraction và composition là hai lượt Gemini riêng. Analyzer overview không đi
  vào payload composition; narrative mới thay lại trường `summary`.
- `rendered_text` và text đưa vào gTTS là cùng narrative.

## Heuristic, không phải invariant ngữ nghĩa

- Prompt yêu cầu bốn nhãn ngữ nghĩa, nhưng code không parse/validate đủ bốn đoạn
  hoặc đúng thứ tự. Hậu xử lý còn có thể nối đoạn bổ sung ở cuối.
- `replace_numbered_sections` chỉ thay marker khớp regex ở đầu dòng.
- `ensure_fact_coverage` dùng substring hoặc tập token trong từng passage. Nó
  không chứng minh facts đúng, tương đương ngữ nghĩa hay không bị diễn đạt lặp.
- Prompt yêu cầu mô tả phần không đọc được dưới dạng text, nhưng schema không có
  confidence hoặc unreadable-region field.

## Lỗi và phụ thuộc ngoài

`UnsupportedInputError` cung cấp lỗi input cụ thể. Các lỗi Gemini, JSON, Pydantic,
composition và gTTS được `app.py` bắt chung và hiển thị nội dung exception.
Gemini/gTTS cần mạng; chưa có timeout, retry, cache, stage taxonomy hoặc telemetry.
