# Bắt đầu với dự án

Accessibility Solution Analyst là ứng dụng Streamlit dùng Gemini để chuyển ảnh
hoặc PDF doanh nghiệp thành dữ liệu có cấu trúc, mô tả Anh/Việt và audio cho
người khiếm thị.

```text
Ảnh/PDF → Gemini phân tích → Pydantic kiểm tra shape
        → Gemini diễn giải → gTTS tạo MP3 → Streamlit hiển thị
```

## Đọc nhanh

1. Đọc [Đặc tả](./spec.md) để hiểu hệ thống phải giải quyết vấn đề gì.
2. Đọc [Kiến trúc](./architecture.md) để hiểu pipeline, công nghệ và module.
3. Dùng [Hướng dẫn phát triển](./development.md) để cài đặt, chạy và kiểm thử.
4. Xem [Trạng thái](./status.md) để biết phần đã làm, giới hạn và việc còn lại.

Nếu chỉ cần chạy dự án, có thể đi thẳng tới
[Thiết lập](./development.md#thiết-lập). Nếu cần đánh giá tiến độ, đọc
[Trạng thái và backlog](./status.md).

## Vai trò từng file

- **[Đặc tả](./spec.md)** — mục tiêu, capability và contract sản phẩm.
- **[Kiến trúc](./architecture.md)** — công nghệ, data flow, module và thành phần.
- **[Phát triển](./development.md)** — cấu trúc repo, setup, chạy và kiểm thử.
- **[Trạng thái](./status.md)** — phần đã làm, bằng chứng, giới hạn và backlog.

## Nguồn nghiên cứu

- **[Yêu cầu đề tài](./research/project-request.md)** — yêu cầu gốc được bảo tồn.
- **[Bài báo tham khảo](./research/research-paper.pdf)** — nguồn PDF năm 2013.
- **[Mapping bài báo](./research/research-paper-mapping.md)** — citation, capability
  mapping và giới hạn suy rộng.

`status.md` là nguồn duy nhất cho trạng thái và backlog. Tài liệu trong
`research/` là nguồn tham khảo, không mô tả implementation hiện tại.

Mỗi file con của `docs/` phải xuất hiện đúng một lần trong mục lục này; repository
test kiểm tra inventory, target và liên kết tương đối.
