---
id: SPEC-accessibility-solution-analyst
sources:
  - references/project-request.md
companions:
  - references/research-paper-mapping.md
---

# Đặc tả hệ thống AI Accessibility Solution Analyst

## Why

Nhân viên khiếm thị gặp khó khăn khi sử dụng dashboard, tài liệu kỹ thuật, ERD,
bảng thống kê, biểu đồ và giao diện doanh nghiệp vì screen reader chủ yếu đọc
văn bản theo thứ tự tuyến tính, không truyền đạt được cấu trúc dữ liệu và bố cục.
Hệ thống phải chuyển nội dung trực quan đó thành mô tả có cấu trúc và âm thanh.

Đây là contract mục tiêu, không phải báo cáo nghiệm thu. Trạng thái implementation
và validation hiện tại chỉ được duy trì tại [process.md](process.md).

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
  - **success:** Người nghe có thể biết nội dung chính, số liệu chi tiết, quan hệ,
    phân tích và nhận định mà không cần nhìn đầu vào; audio không đọc các số thứ
    tự mơ hồ như tên của từng phần.

- **CAP-5 — Xử lý đa ngôn ngữ**
  - **intent:** Hệ thống xử lý input Anh–Nhật–Việt và tạo mô tả đầu ra bằng tiếng Anh hoặc tiếng Việt.
  - **success:** Mỗi ngôn ngữ input đều tạo được mô tả Anh hoặc Việt mà vẫn giữ nguyên dữ kiện và cấu trúc quan trọng.

- **CAP-6 — Chuyển mô tả thành âm thanh**
  - **intent:** Người dùng có thể nghe mô tả đã tạo để tiếp cận nội dung mà không cần nhìn màn hình.
  - **success:** Mô tả Anh hoặc Việt được chuyển thành audio có thể phát và nghe trực tiếp.

## Luồng hoạt động chi tiết

### A. Tiếp nhận tài liệu

Người dùng cung cấp ảnh hoặc PDF và chọn ngôn ngữ muốn nghe là tiếng Việt hoặc
tiếng Anh. Ngôn ngữ trong tài liệu không cần chọn thủ công. Hệ thống chuẩn hóa
đầu vào thành từng trang ảnh có thứ tự để cùng một quy trình có thể xử lý cả ảnh
đơn và PDF nhiều trang.

**Kết quả:** `InputDocument` chứa ít nhất một `InputPage` có thứ tự. App xử lý
từng trang tuần tự; chưa có aggregation ở cấp tài liệu.

### B. Hiểu nội dung trực quan

Prompt yêu cầu AI multimodal quan sát một trang, phát hiện tiếng Anh, Nhật hoặc
Việt và xác định bảng, biểu đồ, sơ đồ hoặc vùng giao diện. Với mỗi thành phần,
prompt yêu cầu trả:

- nhãn, số liệu và đơn vị;
- quan hệ không gian và thứ bậc;
- trình tự, xu hướng và so sánh;
- phần không đọc được được diễn đạt trong text thay vì dùng dấu ba chấm.

Schema hiện chỉ có `label`, `facts` và `relationships`; chưa có confidence hoặc
unreadable-region field. Vì vậy yêu cầu về phần không đọc được là prompt-level,
không phải trường dữ liệu bắt buộc.

**Kết quả mục tiêu:** JSON mô tả nội dung trực quan thay vì chuỗi OCR tuyến tính.
Độ đúng của JSON vẫn cần được đánh giá với ground truth.

### C. Kiểm tra và chuẩn hóa thông tin

SDK được cấu hình trả MIME JSON; code đọc `response.text`, gọi `json.loads` rồi
Pydantic hậu kiểm enum, field dư và các constraint đã khai báo. Lists component,
facts và relationships vẫn có thể rỗng.

**Kết quả:** object đúng hình dạng để composition sử dụng. Bước này không đối
chiếu object với ảnh và không bảo đảm factual accuracy hoặc completeness.

### D. Diễn giải thành nội dung dễ nghe

Một lượt AI riêng nhận source/target metadata cùng components; overview ban đầu
của analyzer không được đưa vào payload. Prompt yêu cầu lời tự nhiên theo bốn
nhãn, không đánh số phần:

- **Tổng quan:** tài liệu hoặc hình ảnh nói về điều gì;
- **Số liệu chi tiết:** đọc đầy đủ nhãn, giá trị và đơn vị;
- **Phân tích số liệu:** giải thích xu hướng, cao nhất, thấp nhất và chênh lệch;
- **Nhận định:** nêu kết luận khách quan dựa trên dữ liệu, không đoán nguyên nhân.

Code không parse để enforce đủ bốn đoạn hoặc đúng thứ tự. Model có thể không tuân
thủ, và coverage fallback có thể nối thêm đoạn sau nhãn cuối.

**Kết quả mục tiêu:** người nghe biết loại thông tin của từng đoạn thay vì chỉ
nghe “một, hai, ba, bốn” không có ngữ cảnh.

### E. Kiểm tra độ đầy đủ và chống lặp

`replace_numbered_sections` thay marker `1–4` chỉ khi regex khớp ở đầu dòng.
`ensure_fact_coverage` coi item đã có nếu nguyên chuỗi xuất hiện hoặc tập token
của item nằm trong một passage; item chưa khớp được nối vào narrative.

Đây là heuristic best-effort. Nó không xác định được tương đương ngữ nghĩa, không
kiểm chứng dữ kiện và có thể nối lặp hoặc bỏ sót nội dung diễn đạt khác từ vựng.

**Kết quả mục tiêu:** giảm bỏ sót chuỗi structured data mà không lặp máy móc.

### F. Tạo và cung cấp output

Bản narrative cuối được lưu lại vào `StructuredDescription.summary`,
`render_description` trả cùng chuỗi cho màn hình và gTTS. Production pipeline chỉ
tạo `AccessibilityResult` sau khi speech thành công, dù model cho phép audio
fields là `None` cho các adapter/test khác.

Với PDF nhiều trang, kết quả được tạo theo đúng thứ tự từng trang; inspector hiện
chỉ preview trang đầu và chưa có navigation cho các trang sau.

**Output cuối cùng gồm:**

- mô tả tự nhiên có bố cục rõ;
- audio MP3 có cùng nội dung với phần chữ;
- danh sách thành phần, dữ kiện và quan hệ đã nhận diện để kiểm chứng.

### Tóm tắt data flow

```text
Ảnh hoặc PDF
  → chuẩn hóa tài liệu
  → AI được yêu cầu trích xuất nội dung trực quan
  → JSON parse + Pydantic shape validation
  → AI diễn giải thành lời tự nhiên
  → marker/coverage heuristic
  → mô tả cuối
  ├─→ văn bản dễ tiếp cận
  ├─→ âm thanh MP3
  └─→ dữ liệu cấu trúc để đối chiếu
```

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

## Ranh giới kiểm chứng

- Các CAP mô tả kết quả mong muốn. Việc có code path tương ứng không đồng nghĩa
  `success` đã được chứng minh.
- Pydantic chỉ kiểm tra shape; factual accuracy và structural coverage cần
  dataset/ground truth.
- Prompt và heuristic không phải semantic guarantee.
- CSS source tests không thay thế browser, keyboard, WCAG, NVDA hoặc user study.
- Mapping bài báo tham khảo và giới hạn suy rộng nằm tại
  [research-paper-mapping.md](references/research-paper-mapping.md).
- Bằng chứng hiện có và backlog nằm tại [process.md](process.md) và
  [plan.md](plan.md).

## Open Questions

- MVP hiện hỗ trợ PDF; DOCX có bắt buộc cho phạm vi nghiệm thu không?
- Ai sẽ đánh giá độ đúng của mô tả và khả năng nghe hiểu, theo thang đo nào?
- Ngưỡng factual accuracy và structural coverage nào được xem là đạt?
