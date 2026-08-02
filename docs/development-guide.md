# Hướng dẫn phát triển

## Thiết lập

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
```

Điền `GEMINI_API_KEY` trong `.env`; không commit file này.

## Chạy app

```powershell
streamlit run app.py
```

## Chạy test

```powershell
$env:PYTHONPATH="src"
python -B -m unittest discover -s tests -v
python -B -m compileall -q app.py src
git diff --check
```

## Quy ước thay đổi

- Viết test thất bại trước khi thêm hành vi.
- Inject fake provider khi test analyzer/composer/speech; unit test không gọi mạng.
- Không hard-code cấu trúc từ một tài liệu mẫu vào production prompt.
- Khi đổi constructor/service, restart Streamlit để tránh module cũ trong memory.
- UI thay đổi trong `ui.py`; logic pipeline không đặt trong CSS/markup.
- Thêm dependency runtime vào `requirements.txt`.

## Smoke test thủ công

Upload một ảnh/PDF, xác nhận preview, output language, mô tả chi tiết, audio và
accordion component. Xác nhận narrative/voice dùng `Tổng quan`, `Số liệu chi
tiết`, `Phân tích số liệu`, `Nhận định`, không còn marker `1–4` hoặc đoạn coverage
lặp. Kiểm tra tương phản progress/uploader/select/alert/expander/CTA,
desktop/mobile và keyboard focus. API smoke test
dùng `.env` cục bộ, không in key hoặc response chứa thông tin nhạy cảm.
