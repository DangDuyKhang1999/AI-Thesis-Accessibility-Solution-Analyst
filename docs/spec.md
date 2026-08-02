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

**Kết quả:** tài liệu đã sẵn sàng để AI phân tích theo từng trang.

### B. Hiểu nội dung trực quan

AI multimodal quan sát toàn bộ trang, tự phát hiện tiếng Anh, Nhật hoặc Việt và
xác định các thành phần có ý nghĩa như bảng, biểu đồ, sơ đồ hoặc vùng giao diện.
Với mỗi thành phần, hệ thống thu thập:

- nhãn, số liệu và đơn vị;
- quan hệ không gian và thứ bậc;
- trình tự, xu hướng và so sánh;
- phần nội dung không thể đọc chắc chắn.

**Kết quả:** nội dung trực quan được chuyển thành dữ liệu có cấu trúc, thay vì
chỉ là chuỗi OCR tuyến tính.

### C. Kiểm tra và chuẩn hóa thông tin

Kết quả AI được kiểm tra theo một schema cố định. Ngôn ngữ, loại thành phần, dữ
kiện và quan hệ phải đúng định dạng trước khi đi tiếp. Bước này tạo một lớp trung
gian có thể kiểm chứng giữa ảnh gốc và phần mô tả cuối.

**Kết quả:** tập thông tin hợp lệ, có tổ chức và có thể dùng để tạo lời mô tả.

### D. Diễn giải thành nội dung dễ nghe

Một lượt AI riêng nhận dữ liệu đã chuẩn hóa và viết lại thành lời tự nhiên. Nội
dung được chia theo ý nghĩa, không đánh số phần:

- **Tổng quan:** tài liệu hoặc hình ảnh nói về điều gì;
- **Số liệu chi tiết:** đọc đầy đủ nhãn, giá trị và đơn vị;
- **Phân tích số liệu:** giải thích xu hướng, cao nhất, thấp nhất và chênh lệch;
- **Nhận định:** nêu kết luận khách quan dựa trên dữ liệu, không đoán nguyên nhân.

**Kết quả:** người nghe biết đoạn hiện tại đang cung cấp loại thông tin gì, thay
vì chỉ nghe “một, hai, ba, bốn” không có ngữ cảnh.

### E. Kiểm tra độ đầy đủ và chống lặp

Hệ thống chuẩn hóa các số thứ tự còn sót thành nhãn có nghĩa, sau đó đối chiếu
phần mô tả với dữ kiện và quan hệ đã trích xuất. Thông tin đã được diễn đạt bằng
cách viết khác vẫn được xem là đã có; chỉ nội dung thực sự thiếu mới được bổ sung.

**Kết quả:** bản mô tả giữ đủ số liệu quan trọng nhưng hạn chế đọc lại cùng một
ý nhiều lần.

### F. Tạo và cung cấp output

Bản mô tả cuối được dùng đồng thời cho phần chữ trên màn hình và công nghệ
text-to-speech. Hệ thống tạo audio tiếng Việt hoặc tiếng Anh, đồng thời giữ phần
dữ liệu cấu trúc để người dùng hoặc người chấm có thể mở ra đối chiếu.

Với PDF nhiều trang, kết quả được tạo theo đúng thứ tự từng trang.

**Output cuối cùng gồm:**

- mô tả tự nhiên có bố cục rõ;
- audio MP3 có cùng nội dung với phần chữ;
- danh sách thành phần, dữ kiện và quan hệ đã nhận diện để kiểm chứng.

### Tóm tắt data flow

```text
Ảnh hoặc PDF
  → chuẩn hóa tài liệu
  → AI hiểu nội dung trực quan
  → chuẩn hóa và kiểm tra thông tin
  → AI diễn giải thành lời tự nhiên
  → kiểm tra độ đầy đủ và chống lặp
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

## Trạng thái triển khai 2026-08-03

- CAP-1: đã nhận PNG/JPEG/WebP và PDF nhiều trang.
- CAP-2/CAP-3: Gemini tạo JSON có schema cho table/chart/diagram/layout.
- CAP-4: pipeline hai lượt tạo bốn đoạn có nhãn ngữ nghĩa: `Tổng quan`, `Số liệu
  chi tiết`, `Phân tích số liệu`, `Nhận định`; bộ hậu xử lý thay marker `1–4` và
  chỉ bổ sung dữ kiện thực sự chưa được diễn đạt.
- CAP-5: AI tự phát hiện input Anh–Nhật–Việt; người dùng chọn output Anh/Việt.
- CAP-6: gTTS tạo audio MP3 theo ngôn ngữ output.
- UI: Midnight Aurora Glassmorphism đã áp dụng quy tắc chữ tối trên bề mặt
  cyan/emerald và chữ sáng trên control nền tối.
- Chưa có evaluation dataset, rubric và kiểm chứng với người dùng khiếm thị.

## Open Questions

- MVP hiện hỗ trợ PDF; DOCX có bắt buộc cho phạm vi nghiệm thu không?
- Ai sẽ đánh giá độ đúng của mô tả và khả năng nghe hiểu, theo thang đo nào?
- Ngưỡng factual accuracy và structural coverage nào được xem là đạt?
