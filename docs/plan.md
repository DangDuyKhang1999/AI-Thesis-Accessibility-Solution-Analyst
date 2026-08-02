# Kế hoạch triển khai và trạng thái

**Mục tiêu:** Ảnh/PDF doanh nghiệp đa ngôn ngữ → phân tích cấu trúc → mô tả chi
tiết Anh/Việt → audio cho người khiếm thị.

## Hoàn thành

- [x] Model `LanguageCode`, `ComponentType`, `VisualComponent`,
  `StructuredDescription`, `InputDocument`, `AccessibilityResult`.
- [x] Adapter PNG/JPEG/WebP/PDF nhiều trang bằng PyMuPDF.
- [x] Gemini extraction JSON cho table/chart/diagram/layout.
- [x] AI tự nhận diện input Anh–Nhật–Việt.
- [x] Output tiếng Việt hoặc tiếng Anh.
- [x] Lượt composition riêng tạo mô tả chi tiết có cấu trúc.
- [x] Thay section marker `1–4` bằng nhãn nghe hiểu được trước khi tạo voice.
- [x] Kiểm tra coverage theo nhãn và giá trị để tránh nối lặp dữ kiện đã nói.
- [x] Audio MP3 theo ngôn ngữ output.
- [x] Pipeline test được bằng fake providers.
- [x] UI Midnight Aurora responsive và tương phản cao.
- [x] Chuẩn hóa tương phản cho progress, uploader, select, alert, expander và CTA.
- [x] Archive Happy Case MVP, production không import archive.

## Tiếp theo: chất lượng MVP

### 1. Bộ dữ liệu đánh giá

- [ ] Chuẩn bị ít nhất một mẫu cho mỗi table/chart/diagram/layout bằng từng ngôn
  ngữ Anh, Nhật, Việt.
- [ ] Ghi ground truth: nhãn, số liệu, quan hệ, cấu trúc và phần không đọc được.
- [ ] Định nghĩa rubric factual accuracy, structural coverage và listening clarity.

### 2. Reliability

- [ ] Thêm timeout/retry có giới hạn cho hai lượt Gemini và gTTS.
- [ ] Phân loại lỗi input, extraction, schema, composition và speech ở UI.
- [ ] Giới hạn dung lượng file và số trang PDF trước khi gọi API.
- [ ] Cache theo file hash, target language và model version.

### 3. Accessibility validation

- [ ] Kiểm thử đầy đủ bằng bàn phím.
- [ ] Audit với NVDA trên Windows.
- [ ] Kiểm tra thứ tự đọc: input → trạng thái → mô tả → audio → chi tiết.
- [ ] Ghi nhận đánh giá nghe hiểu từ người dùng mục tiêu.

### 4. Delivery

- [ ] Thêm dependency lock và CI chạy test/compile.
- [ ] Tạo cấu hình deployment sau khi evaluation đạt ngưỡng.

## Điều kiện hoàn thành MVP nghiên cứu

Pipeline phải chạy được trên bộ mẫu đại diện, giữ đúng dữ kiện quan trọng, diễn
đạt cấu trúc tốt hơn OCR tuyến tính, phát audio Việt/Anh và có kết quả đánh giá
định lượng cùng accessibility audit.
