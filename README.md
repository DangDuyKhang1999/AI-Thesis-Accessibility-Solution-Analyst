# AI Thesis Accessibility Solution Analyst

Ứng dụng Streamlit chuyển ảnh và PDF doanh nghiệp thành mô tả chi tiết có cấu
trúc và audio dành cho người khiếm thị.

## Chức năng hiện tại

- Nhận PNG, JPEG, WebP và PDF nhiều trang.
- AI tự nhận diện input tiếng Anh, Nhật hoặc Việt.
- Người dùng chọn output tiếng Việt hoặc tiếng Anh.
- Gemini nhận diện bảng, biểu đồ, sơ đồ và layout thành JSON có schema.
- Lượt AI thứ hai tạo mô tả nghe hiểu được theo bốn đoạn ngữ nghĩa: `Tổng quan`,
  `Số liệu chi tiết`, `Phân tích số liệu` và `Nhận định` (hoặc nhãn tiếng Anh).
- Chuẩn hóa đầu ra đánh số `1–4` thành nhãn có nghĩa trước khi tạo audio và
  tránh nối lại dữ kiện đã được diễn đạt bằng cách viết khác.
- gTTS tạo audio theo ngôn ngữ output.
- UI Midnight Aurora Glassmorphism responsive và tương phản cao.

## Cài đặt và chạy

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
# Điền GEMINI_API_KEY trong .env
streamlit run app.py
```

Mặc định app mở tại `http://localhost:8501`.

## Kiểm thử

```powershell
$env:PYTHONPATH="src"
python -B -m unittest discover -s tests -v
python -B -m compileall -q app.py src
```

Hiện có 32 unit/repository tests. Playwright được dùng cục bộ cho smoke test UI
desktop/mobile nhưng chưa nằm trong `requirements.txt`.

## Cấu trúc chính

- `app.py`: entry point production.
- `src/accessibility_analyst/`: input, model, analyzer, composer, TTS, pipeline và UI.
- `archive/happy-case-mvp/`: MVP cũ được lưu để đối chiếu, không được production import.
- `tests/`: unit test và repository hygiene.
- `docs/`: đặc tả, kiến trúc, tiến độ và hướng dẫn phát triển.

Key chỉ nằm trong `.env`; file này bị Git ignore. Xem [docs/index.md](docs/index.md)
để truy cập toàn bộ tài liệu.
