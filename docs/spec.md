---
id: SPEC-accessibility-solution-analyst
sources:
  - references/project-request.md
companions: []
---

# Đặc tả hệ thống AI Accessibility Solution Analyst

## Why

Nhân viên khiếm thị gặp khó khăn khi sử dụng dashboard, tài liệu kỹ thuật, ERD,
bảng thống kê, biểu đồ và giao diện doanh nghiệp vì screen reader chủ yếu đọc
văn bản theo thứ tự tuyến tính, không truyền đạt được cấu trúc dữ liệu và bố cục.
Hệ thống phải chuyển nội dung trực quan đó thành mô tả có cấu trúc và âm thanh.

## Capabilities

- **CAP-1 — Tiếp nhận nội dung doanh nghiệp**
  - **intent:** Người dùng có thể cung cấp tài liệu hoặc ảnh giao diện doanh nghiệp bằng tiếng Anh, Nhật hoặc Việt.
  - **success:** Hệ thống tiếp nhận được mẫu dashboard, tài liệu kỹ thuật, ERD, bảng thống kê, biểu đồ hoặc giao diện và chuyển sang bước phân tích.

- **CAP-2 — Phân tích nội dung và bố cục**
  - **intent:** Hệ thống dùng LLM để phân tích nội dung, quan hệ không gian và cấu trúc của tài liệu hoặc giao diện.
  - **success:** Kết quả phân tích nêu được chủ đề chính, các vùng thông tin và quan hệ cần thiết để hiểu đầu vào.

- **CAP-3 — Nhận diện thành phần trực quan**
  - **intent:** Hệ thống nhận diện bảng dữ liệu, biểu đồ, sơ đồ và layout giao diện.
  - **success:** Với đầu vào có thành phần thuộc bốn nhóm, kết quả xác định đúng loại và thông tin chính của từng thành phần.

- **CAP-4 — Sinh mô tả tự nhiên có cấu trúc**
  - **intent:** Hệ thống chuyển kết quả phân tích thành mô tả ngôn ngữ tự nhiên thể hiện được cấu trúc thay vì chỉ đọc văn bản tuyến tính.
  - **success:** Người nghe có thể biết nội dung chính, thứ tự, nhóm, nhãn, quan hệ và điểm nổi bật mà không cần nhìn đầu vào.

- **CAP-5 — Xử lý đa ngôn ngữ**
  - **intent:** Hệ thống xử lý input Anh–Nhật–Việt và tạo mô tả đầu ra bằng tiếng Anh hoặc tiếng Việt.
  - **success:** Mỗi ngôn ngữ input đều tạo được mô tả Anh hoặc Việt mà vẫn giữ nguyên dữ kiện và cấu trúc quan trọng.

- **CAP-6 — Chuyển mô tả thành âm thanh**
  - **intent:** Người dùng có thể nghe mô tả đã tạo để tiếp cận nội dung mà không cần nhìn màn hình.
  - **success:** Mô tả Anh hoặc Việt được chuyển thành audio có thể phát và nghe trực tiếp.

## Constraints

- Đối tượng phục vụ chính là nhân viên khiếm thị trong bối cảnh doanh nghiệp.
- Input phải bao phủ tiếng Anh, Nhật và Việt; output phải hỗ trợ tiếng Anh và Việt.
- Mô tả phải truyền đạt cấu trúc của dữ liệu hoặc bố cục, không chỉ chép lại OCR.
- LLM là thành phần phân tích và diễn giải trung tâm của pipeline.

## Non-goals

- Bảo mật production, tối ưu hiệu năng, tài khoản, phân quyền, CI/CD và triển khai thương mại không phải mục tiêu chính của đặc tả này.
- Không khóa cứng nhà cung cấp LLM, OCR hoặc TTS khi yêu cầu gốc chưa chỉ định.
- Không mở rộng sang các ngôn ngữ input/output ngoài Anh–Nhật–Việt và Anh–Việt.

## Success signal

Trong một demo hoàn chỉnh, người dùng đưa vào các mẫu doanh nghiệp đại diện cho
bảng, biểu đồ, sơ đồ và layout bằng ba ngôn ngữ nguồn; hệ thống tạo mô tả có cấu
trúc bằng Anh hoặc Việt và phát được audio giúp người nghe hiểu nội dung chính
cùng quan hệ trực quan mà không xem bản gốc.

## Open Questions

- Ngoài ảnh chụp, định dạng tài liệu bắt buộc cho MVP là PDF, DOCX hay cả hai?
- Ai sẽ đánh giá độ đúng của mô tả và khả năng nghe hiểu, theo thang đo nào?
- Người dùng chọn ngôn ngữ output hay hệ thống tự quyết định theo ngữ cảnh?
