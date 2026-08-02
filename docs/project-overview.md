# Tổng quan dự án

Accessibility Solution Analyst là ứng dụng web Python/Streamlit giúp nhân viên
khiếm thị tiếp cận tài liệu và giao diện doanh nghiệp. Hệ thống không chỉ đọc OCR
tuyến tính mà trích xuất bảng, biểu đồ, sơ đồ và layout thành dữ liệu có cấu trúc,
sau đó diễn giải thành văn xuôi có nhãn ngữ nghĩa và audio. Cùng một narrative
đã chuẩn hóa được dùng cho màn hình và TTS để người nghe hiểu mỗi đoạn đang nói
về tổng quan, số liệu, phân tích hay nhận định.

## Công nghệ

| Nhóm | Công nghệ |
| --- | --- |
| Runtime/UI | Python 3.12, Streamlit |
| AI | Google Gen AI SDK, `gemini-2.5-flash-lite` |
| Validation | Pydantic 2 |
| Document | PyMuPDF |
| Speech | gTTS |
| Test | unittest, Playwright smoke test cục bộ |

Kiến trúc là monolith dạng pipeline/service, một entry point `app.py`, không có
database hoặc HTTP API riêng. Xem [architecture.md](architecture.md) và
[development-guide.md](development-guide.md).
