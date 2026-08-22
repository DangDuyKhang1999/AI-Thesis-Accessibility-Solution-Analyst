# Kế hoạch chất lượng và backlog

File này không phải báo cáo tiến độ. Trạng thái và bằng chứng hiện tại nằm duy
nhất tại [process.md](process.md).

## Contract đã có trong code

- Model cho language, component, document/page và accessibility result.
- Adapter PNG/JPEG/WebP/PDF; xử lý kết quả tuần tự theo trang.
- Hai lượt Gemini: extraction JSON rồi composition từ structured data.
- UI chọn output Việt/Anh và yêu cầu AI phát hiện nguồn Anh/Nhật/Việt.
- Hậu xử lý marker cùng coverage fallback dựa trên chuỗi/token.
- MP3 bằng gTTS; narrative màn hình và input TTS là cùng một chuỗi.
- Desktop workspace ba vùng và inspector preview trang đầu.
- Archive Happy Case tách khỏi import production.

Các mục trên là implementation contract, không đồng nghĩa đã đạt factual
accuracy, accessibility conformance hoặc listening clarity.

## Backlog validation nghiên cứu

- [ ] Chuẩn bị bộ mẫu đại diện cho table/chart/diagram/layout bằng nguồn Anh,
  Nhật và Việt; ghi version, license và điều kiện sử dụng.
- [ ] Ghi ground truth cho label, giá trị, đơn vị, quan hệ, thứ bậc và phần không
  xác định được.
- [ ] Định nghĩa rubric factual accuracy, structural coverage, translation
  fidelity và listening clarity cùng ngưỡng đạt.
- [ ] Tách đánh giá extraction khỏi đánh giá narrative/TTS.
- [ ] Chạy đánh giá lặp lại với model/version cố định và lưu kết quả định lượng.

## Backlog reliability

- [ ] Giới hạn dung lượng upload và số trang PDF trước khi gọi API.
- [ ] Thêm timeout/retry có giới hạn cho extraction, composition và gTTS.
- [ ] Phân loại lỗi input, JSON, schema, composition và speech ở UI.
- [ ] Cache theo file hash, target language và model version.
- [ ] Theo dõi latency, request count và chi phí/quota mà không log dữ liệu nhạy cảm.
- [ ] Thêm kiểm tra nhất quán source/target language và policy cho target Japanese
  ở model boundary.

## Backlog accessibility

- [ ] Kiểm thử đầy đủ chỉ bằng bàn phím trên browser mục tiêu.
- [ ] Audit NVDA trên Windows, gồm thứ tự đọc, thông báo tiến trình và lỗi.
- [ ] Kiểm tra flow input → status → audio/narrative → component details → inspector.
- [ ] Đánh giá với người dùng mục tiêu và ghi consent/phương pháp nghiên cứu.
- [ ] Xác định có cần active exploration theo trường dữ liệu hay narrative thụ động
  là đủ cho phạm vi nghiệm thu.

## Backlog delivery

- [ ] Thêm dependency lock và CI chạy validation gate.
- [ ] Bổ sung browser E2E có thể tái chạy nếu chọn công cụ phù hợp.
- [ ] Tạo cấu hình deployment chỉ sau khi evaluation đạt ngưỡng đã định nghĩa.

## Điều kiện hoàn thành MVP nghiên cứu

Một bản build chỉ được xem là đạt khi chạy trên dataset đại diện, có số đo
factual/structural rõ ràng, narrative và audio Việt/Anh được đánh giá, cùng kết
quả keyboard/screen-reader/user validation được lưu bằng phương pháp có thể kiểm
tra. Unit tests hiện tại là điều kiện cần, không phải bằng chứng nghiệm thu đó.
