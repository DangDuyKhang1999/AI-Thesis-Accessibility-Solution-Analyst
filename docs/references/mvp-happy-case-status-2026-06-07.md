MVP Happy Case — Trạng thái dự án
Ngày: 2026-06-07

1) Mục tiêu
- Một luồng web duy nhất: tải ảnh lên -> sinh mô tả tiếng Việt thuần văn bản -> phát audio ngay trên web để hỗ trợ người khiếm thị.

2) Trạng thái hiện tại
- Đã tạo giao diện Streamlit tối giản ở `streamlit_app.py`.
- UI có upload ảnh, preview ảnh, nút sinh audio và player nghe trực tiếp.
- Luồng xử lý không còn yêu cầu xuất file text ra ngoài; text chỉ dùng nội bộ.
- Prompt đã được dọn để output là văn bản thuần, không bullet, không markdown, không ký tự trang trí.
- Nếu HF Inference không truy cập được, app ưu tiên voice Việt cục bộ nếu có; nếu không có voice Việt thì tự động chuyển sang `gTTS` tiếng Việt.

3) Kết quả đã xác nhận
- Text tiếng Việt đã sinh thành công.
- Luồng xử lý một bước từ ảnh sang audio đã có thể chạy trong app web mới.
- Vấn đề TTS tiếng Anh đã được xử lý bằng cách chặn voice không phải tiếng Việt và thêm fallback `gTTS`.

4) Lưu ý kỹ thuật
- Model text mặc định đang dùng: `gemini-2.5-flash-lite`.
- HF Inference TTS vẫn là đường ưu tiên khi mạng hoạt động.
- Output âm thanh được trả trực tiếp về UI, không cần file text trung gian.

5) File liên quan
- Ứng dụng web: `streamlit_app.py`
- Script chính CLI cũ: `happy_case_vn/run_happy_case.py`
- File trạng thái này: `DOC/mvp_happy_case_status.txt`
- Phụ thuộc: `happy_case_vn/requirements.txt`

6) Hướng tiếp theo
- Nếu cần, bước tiếp theo chỉ là tinh chỉnh bố cục UI, ví dụ chia 2 cột upload / kết quả và thêm nhãn trạng thái ngắn gọn.
