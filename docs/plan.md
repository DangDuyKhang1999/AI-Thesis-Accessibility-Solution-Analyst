# Accessibility Solution Analyst Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Xây dựng pipeline tài liệu/giao diện doanh nghiệp đa ngôn ngữ → phân tích cấu trúc → mô tả Anh/Việt → audio cho nhân viên khiếm thị.

**Architecture:** Streamlit điều phối một pipeline gồm input adapter, LLM analyzer, structured description, translator và TTS. Mỗi bước trao đổi qua kiểu dữ liệu rõ ràng để có thể demo từng năng lực độc lập trước khi ghép end-to-end.

**Tech Stack:** Python 3.12, Streamlit, Google Gen AI SDK, Pydantic, PyMuPDF, gTTS/pyttsx3 và unittest.

## Global Constraints

- Input: tiếng Anh, Nhật hoặc Việt.
- Output mô tả và audio: tiếng Anh hoặc Việt.
- Phải nhận diện bảng dữ liệu, biểu đồ, sơ đồ và layout giao diện.
- Mô tả ngôn ngữ tự nhiên phải truyền đạt cấu trúc, quan hệ và điểm nổi bật; không chỉ chép OCR tuyến tính.
- Các việc bảo mật, tối ưu và triển khai chỉ thực hiện ở mức tối thiểu cần để demo năng lực cốt lõi.

---

## Trạng thái baseline

Luồng ảnh → mô tả tiếng Việt → audio đã chạy trên Streamlit với Gemini và TTS
fallback. Baseline chưa có schema mô tả, PDF, phân loại thành phần hoặc lựa chọn
ngôn ngữ output. Vì vậy bước tiếp theo là mở rộng trực tiếp năng lực đề tài, không
ưu tiên refactor tổng quát.

### Task 1: Mô hình mô tả có cấu trúc

**Files:**
- Create: `src/accessibility_analyst/models.py`
- Create: `tests/test_models.py`

**Produces:** `StructuredDescription`, `VisualComponent`, `ComponentType`, `LanguageCode`.

- [ ] Viết test tạo mô tả gồm summary và danh sách component có loại, nhãn, dữ kiện, quan hệ.
- [ ] Chạy `python -m unittest tests.test_models -v`; xác nhận FAIL vì module chưa tồn tại.
- [ ] Cài `pydantic` và triển khai model tối thiểu cho CAP-3/CAP-4.
- [ ] Chạy lại test; xác nhận PASS.
- [ ] Commit `feat: add structured accessibility description model`.

### Task 2: Phân tích bảng, biểu đồ, sơ đồ và layout

**Files:**
- Create: `src/accessibility_analyst/analyzer.py`
- Create: `tests/test_analyzer.py`
- Modify: `streamlit_app.py`

**Consumes:** `StructuredDescription`; **Produces:** `analyze_visual(bytes, mime_type, source_language) -> StructuredDescription`.

- [ ] Viết fake-client test xác nhận analyzer yêu cầu đủ bốn loại component và parse response thành schema.
- [ ] Chạy `python -m unittest tests.test_analyzer -v`; xác nhận FAIL.
- [ ] Chuyển prompt Gemini hiện tại vào analyzer và yêu cầu output JSON theo schema.
- [ ] Chạy test và demo lần lượt `assets/samples/bar.png`, `bar-2.png`; xác nhận PASS và có component biểu đồ/bảng tương ứng.
- [ ] Commit `feat: analyze enterprise visual structures`.

### Task 3: Tiếp nhận tài liệu và giao diện

PDF được chọn làm định dạng tài liệu đầu tiên cho MVP; DOCX chỉ được bổ sung sau
khi câu hỏi định dạng bắt buộc trong spec được chốt.

**Files:**
- Create: `src/accessibility_analyst/input_adapter.py`
- Create: `tests/test_input_adapter.py`
- Modify: `requirements.txt`
- Modify: `streamlit_app.py`

**Produces:** `InputDocument(pages, detected_language, source_name)` từ ảnh hoặc PDF.

- [ ] Viết test cho PNG/JPEG/WebP và PDF hai trang; file khác phải bị từ chối rõ ràng.
- [ ] Chạy `python -m unittest tests.test_input_adapter -v`; xác nhận FAIL.
- [ ] Dùng PyMuPDF render PDF thành từng trang ảnh và giữ thứ tự trang.
- [ ] Mở rộng uploader, preview và pipeline để xử lý `InputDocument`.
- [ ] Chạy test và demo một PDF doanh nghiệp; xác nhận mỗi trang đi vào analyzer đúng thứ tự.
- [ ] Commit `feat: accept enterprise images and pdf documents`.

### Task 4: Input Anh–Nhật–Việt và output Anh–Việt

**Files:**
- Create: `src/accessibility_analyst/language_service.py`
- Create: `tests/test_language_service.py`
- Modify: `streamlit_app.py`

**Produces:** `detect_source_language(text_or_metadata) -> LanguageCode` và `render_description(description, target_language) -> str`.

- [ ] Viết test fixtures cùng một dữ kiện bằng Anh, Nhật, Việt; bản dịch phải giữ nhãn và số liệu.
- [ ] Chạy `python -m unittest tests.test_language_service -v`; xác nhận FAIL.
- [ ] Thêm lựa chọn output `vi`/`en`; yêu cầu LLM phân tích input trong ba ngôn ngữ và render theo ngôn ngữ đích.
- [ ] Chạy test và ba demo input; xác nhận cả hai ngôn ngữ output giữ nguyên dữ kiện.
- [ ] Commit `feat: add multilingual analysis and translation`.

### Task 5: Audio theo ngôn ngữ output

**Files:**
- Create: `src/accessibility_analyst/speech.py`
- Create: `tests/test_speech.py`
- Modify: `streamlit_app.py`

**Produces:** `synthesize(text, language) -> AudioResult(bytes, mime_type, provider)`.

- [ ] Viết provider-fake test xác nhận tiếng Việt dùng voice Việt và tiếng Anh dùng voice Anh.
- [ ] Chạy `python -m unittest tests.test_speech -v`; xác nhận FAIL.
- [ ] Di chuyển TTS hiện tại vào service và chọn voice theo `LanguageCode`.
- [ ] Chạy test; phát thử hai audio Anh/Việt trên web.
- [ ] Commit `feat: synthesize bilingual accessibility audio`.

### Task 6: Demo end-to-end theo yêu cầu đề tài

**Files:**
- Create: `src/accessibility_analyst/pipeline.py`
- Create: `tests/test_pipeline.py`
- Create: `docs/demo-scenarios.md`
- Modify: `streamlit_app.py`

**Produces:** `run_pipeline(document, target_language) -> AccessibilityResult`.

- [ ] Viết integration test bằng fake provider cho chuỗi input → component → structured description → translation → audio.
- [ ] Chạy `python -m unittest tests.test_pipeline -v`; xác nhận FAIL.
- [ ] Ghép các service vào pipeline và cho UI hiển thị component, mô tả cùng audio.
- [ ] Chuẩn bị kịch bản demo bao phủ bảng, biểu đồ, sơ đồ, layout và ba ngôn ngữ input.
- [ ] Chạy `python -m unittest discover -s tests -v` và thực hiện toàn bộ kịch bản demo.
- [ ] Commit `feat: complete multilingual accessibility demo pipeline`.

## Thứ tự và mốc

Task 1 → 2 tạo lõi giá trị khác biệt so với screen reader tuyến tính. Task 3 mở
rộng từ ảnh sang tài liệu. Task 4 → 5 hoàn thiện pipeline ngôn ngữ và audio. Task
6 là mốc MVP đề tài: demo được toàn bộ chuỗi yêu cầu trong `project-request.md`.
