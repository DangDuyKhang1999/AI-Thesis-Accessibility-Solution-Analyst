# Accessibility MVP Implementation Plan

**Cập nhật trạng thái:** 2026-08-03  
**Tiến độ MVP nghiên cứu ước lượng:** 35% — xem công thức tại `process.md`.

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Đưa prototype ảnh → mô tả tiếng Việt → audio thành MVP nghiên cứu có thể kiểm thử, đánh giá và trình diễn an toàn.

**Architecture:** Giữ Streamlit làm lớp trình bày nhưng tách phân tích ảnh, chuẩn hóa văn bản và TTS thành các module có interface rõ. API bên ngoài nằm sau adapter để unit test không phụ thuộc mạng và để thay model không ảnh hưởng UI.

**Tech Stack:** Python 3.12, Streamlit, Google Gen AI SDK, requests, pyttsx3, gTTS, unittest.

## Global Constraints

- Key chỉ đến từ biến môi trường/secrets; không lưu credential trong mã nguồn.
- Một lượt MVP chỉ xử lý một ảnh PNG, JPEG hoặc WebP.
- Đầu ra chính là tiếng Việt thuần văn bản, tối ưu cho TTS.
- Ảnh không được lưu lâu dài nếu người dùng chưa chủ động yêu cầu.
- Mọi thay đổi hành vi phải có kiểm thử thất bại trước khi triển khai.

---

## Cấu trúc mục tiêu

```text
src/accessibility_analyst/
  config.py          # đọc và kiểm tra cấu hình
  image_analysis.py  # adapter phân tích ảnh
  text_normalizer.py # chuẩn hóa mô tả cho TTS
  speech.py          # chiến lược và fallback TTS
streamlit_app.py     # UI và điều phối
tests/               # unit/integration tests
assets/samples/      # ảnh mẫu không nhạy cảm
docs/                # spec, plan, tiến độ, tài liệu tham khảo
scripts/legacy/      # prototype CLI được bảo tồn
```

## Giai đoạn 0 — An toàn và vệ sinh repository (P0)

**Ước lượng hoàn thành:** 60%

- [x] Gỡ credential khỏi mã nguồn, lưu local trong `.env` và tự nạp bằng
  `python-dotenv`.
- [x] Thêm `.gitignore`, `.env.example` và kiểm tra tự động cho repository.
- [x] Gom tài liệu, ảnh mẫu và script thử nghiệm vào thư mục có trách nhiệm rõ.
- [ ] Thu hồi Gemini key và Hugging Face token đã từng xuất hiện trong source.
- [ ] Tạo commit nền đầu tiên sau khi kiểm tra không còn secret.

**Kiểm chứng:**

```powershell
python -m unittest discover -s tests -v
git status --short
```

## Giai đoạn 1 — Tách lõi có thể kiểm thử (P0)

**Ước lượng hoàn thành:** 10%

- [ ] Viết test cấu hình: thiếu `GEMINI_API_KEY` phải trả lỗi xác định.
- [ ] Tạo `config.py` với `AppConfig.from_env()` và không đọc biến toàn cục ở UI.
- [ ] Viết test cho `_clean_plain_text`, MIME và chuẩn hóa số tiếng Việt.
- [ ] Chuyển các hàm thuần sang `text_normalizer.py` và `image_analysis.py`.
- [ ] Viết test thứ tự TTS fallback và tách provider vào `speech.py`.
- [ ] Giữ `streamlit_app.py` chỉ phụ trách widget, trạng thái và hiển thị lỗi.

**Hoàn tất khi:** unit test chạy offline, UI không chứa logic provider và happy
case vẫn chạy bằng `streamlit run streamlit_app.py`.

## Giai đoạn 2 — Độ tin cậy của MVP (P1)

**Ước lượng hoàn thành:** 15%

- [ ] Kiểm tra kích thước, MIME thực tế và giới hạn dung lượng ảnh.
- [ ] Định nghĩa kiểu kết quả gồm nội dung, cảnh báo, model và nguồn TTS.
- [ ] Phân loại timeout, quota, xác thực và response rỗng thành thông báo riêng.
- [ ] Thêm integration test dùng fake adapter, không gọi API thật trong CI.
- [ ] Khóa dependency hoặc ghi lại phiên bản môi trường tái lập.

**Hoàn tất khi:** mọi lỗi chính có đường xử lý kiểm thử được và không làm mất
trạng thái ảnh đã tải.

## Giai đoạn 3 — Accessibility thực chứng (P1)

**Ước lượng hoàn thành:** 10%

- [ ] Audit thứ tự tab, accessible name, focus sau khi xử lý và live status.
- [ ] Kiểm thử với NVDA trên Windows và chỉ dùng bàn phím.
- [ ] Cho phép phát/tạm dừng audio bằng control chuẩn, không ép autoplay.
- [ ] Ghi biên bản test gồm tác vụ, kết quả, trở ngại và bản sửa.

**Hoàn tất khi:** người dùng có thể tải ảnh, tạo và nghe kết quả mà không cần
chuột; lỗi và trạng thái đều được screen reader thông báo.

## Giai đoạn 4 — Thiết kế và chạy đánh giá nghiên cứu (P1)

**Ước lượng hoàn thành:** 5%

- [ ] Xây bộ ít nhất 20 ảnh có ground truth cho bảng, biểu đồ và UI.
- [ ] Chốt rubric: đúng dữ kiện, đầy đủ cấu trúc, hallucination, dễ nghe.
- [ ] Lưu phiên bản prompt/model cùng từng lần chạy.
- [ ] So sánh baseline OCR/tuyến tính với pipeline đa phương thức.
- [ ] Tổng hợp số liệu định lượng và nhận xét người dùng thử.

**Hoàn tất khi:** kết quả có thể tái chạy và trả lời được các câu hỏi trong
`spec.md`, không chỉ chứng minh demo hoạt động.

## Giai đoạn 5 — Mở rộng sau MVP (P2)

**Ước lượng hoàn thành:** 0%; không tính vào phần trăm MVP nghiên cứu hiện tại.

- [ ] Đánh giá Docling cho PDF/bảng và schema validation trước khi tích hợp.
- [ ] Thử input Anh/Nhật và đầu ra Anh/Việt trên bộ dữ liệu riêng.
- [ ] Đánh giá TTS Việt local về chất lượng, latency và yêu cầu phần cứng.
- [ ] Chỉ chọn triển khai production sau khi có yêu cầu riêng tư và vận hành.

## Thứ tự thực hiện đề xuất

Giai đoạn 0 → 1 → 2 có tính chặn. Giai đoạn 3 và 4 có thể chuẩn bị song song sau
khi interface lõi ổn định. Giai đoạn 5 không nên bắt đầu trước khi MVP có số liệu
đánh giá, để tránh mở rộng phạm vi luận văn quá sớm.

## Ba việc tiếp theo

1. Thu hồi hai credential đã lộ và tạo commit nền sau khi quét secret.
2. Tách `streamlit_app.py` thành các module bằng TDD, ưu tiên config và text normalizer.
3. Chốt rubric cùng bộ 20 ảnh đánh giá trước khi tối ưu prompt/model.

Không bắt đầu Docling, PDF hay đa ngôn ngữ trước khi ba việc trên hoàn tất.
