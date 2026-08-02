# Chỉ mục tài liệu dự án

**Cập nhật:** 2026-08-03  
**Loại dự án:** Monolith Python/Streamlit  
**Entry point:** `archive/happy-case-mvp/streamlit_app.py`

## Tài liệu chính

- [Đặc tả sản phẩm](./spec.md) — phạm vi, yêu cầu và tiêu chí nghiệm thu.
- [Kế hoạch triển khai](./plan.md) — các giai đoạn và ưu tiên thực hiện.
- [Tiến độ hiện tại](./process.md) — phần trăm sơ bộ, bằng chứng, rủi ro và cách chạy.
- [README](../README.md) — hướng dẫn khởi động nhanh.

## Tài liệu tham khảo

- [Yêu cầu đề tài ban đầu](./references/project-request.md)
- [Đề xuất MVP ban đầu](./references/original-mvp-proposal.md)
- [Snapshot MVP ngày 2026-06-07](./references/mvp-happy-case-status-2026-06-07.md)
- [Bài báo nghiên cứu](./references/research-paper.pdf)

## Bắt đầu nhanh

```powershell
pip install -r requirements.txt
Copy-Item .env.example .env
# Điền GEMINI_API_KEY trong .env
streamlit run archive/happy-case-mvp/streamlit_app.py
```

Xem `process.md` để biết quy trình cài virtual environment, cấu hình TTS tùy chọn,
chạy test và sử dụng CLI legacy.
