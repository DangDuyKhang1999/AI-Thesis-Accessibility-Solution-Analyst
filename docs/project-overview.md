# Tổng quan dự án

Accessibility Solution Analyst là MVP nghiên cứu Python/Streamlit nhằm giúp nhân
viên khiếm thị tiếp cận ảnh tài liệu và giao diện doanh nghiệp. Hệ thống yêu cầu
Gemini trích xuất bảng, biểu đồ, sơ đồ và layout thành dữ liệu có cấu trúc, sau đó
dùng một lượt Gemini riêng để diễn giải dữ liệu đó thành narrative Anh/Việt và
gTTS MP3.

Đây là pipeline AI thử nghiệm, không phải công cụ OCR/đánh giá accessibility đã
được chứng nhận. Schema validation kiểm tra hình dạng response chứ không chứng
minh factual accuracy. Xem trạng thái và bằng chứng tại [process.md](process.md).

## Trải nghiệm hiện tại

- Control rail: upload ảnh/PDF, thông báo auto-detect và chọn output Việt/Anh.
- Analysis workspace: trạng thái, progress, audio, narrative và component details
  cho từng trang được xử lý tuần tự.
- Document inspector: preview thu vừa trang đầu và popover mở ảnh lớn. Chưa có
  navigation preview cho các trang PDF còn lại.
- Dưới 900px, CSS chuyển các cột thành flow một cột.

## Stack

| Nhóm | Công nghệ/vai trò |
| --- | --- |
| Runtime/UI | Python 3.12, Streamlit |
| AI | Google Gen AI SDK, `gemini-2.5-flash-lite` cho extraction và composition |
| Shape validation | `json.loads`, Pydantic 2 |
| Document | PyMuPDF render PDF sang PNG |
| Speech | gTTS, cần mạng |
| Test | `unittest`: model/input/pipeline/summarizer, CSS source contract và repository/docs hygiene |

Repo không có browser automation, live provider tests, database, account system
hoặc HTTP API riêng. Kiến trúc deploy là một Streamlit monolith với service
boundaries trong package. Xem [architecture.md](architecture.md) và
[development-guide.md](development-guide.md).
