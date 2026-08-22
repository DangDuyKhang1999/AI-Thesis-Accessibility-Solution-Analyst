# AI Thesis Accessibility Solution Analyst

Ứng dụng Streamlit thử nghiệm chuyển ảnh và PDF doanh nghiệp thành dữ liệu trực
quan có cấu trúc, bản mô tả Anh/Việt và audio hỗ trợ người khiếm thị.

## Luồng đã triển khai

- Nhận PNG, JPEG, WebP hoặc PDF; PDF được render thành các trang PNG theo thứ tự.
- Với từng trang, Gemini được yêu cầu phát hiện nguồn Anh/Nhật/Việt và trả JSON
  cho `table`, `chart`, `diagram` hoặc `layout`.
- Pydantic kiểm tra hình dạng dữ liệu. Lớp này không xác minh dữ kiện trong JSON
  có đúng với ảnh hay đã đầy đủ hay chưa.
- Một lượt Gemini riêng được yêu cầu tạo narrative có nhãn ngữ nghĩa. Hậu xử lý
  thay marker `1–4` và nối facts/relationships chưa khớp bằng heuristic chuỗi;
  đây không phải bảo đảm tương đương ngữ nghĩa.
- gTTS tạo MP3 từ đúng narrative được hiển thị.
- UI desktop có ba vùng: điều khiển, kết quả phân tích và ảnh tham chiếu. Mọi
  trang được xử lý tuần tự, nhưng inspector hiện chỉ preview trang đầu.

Trạng thái kiểm chứng và giới hạn hiện hành chỉ được duy trì tại
[docs/process.md](docs/process.md); backlog nằm tại [docs/plan.md](docs/plan.md).
Mục lục đầy đủ nằm ở [docs/index.md](docs/index.md).

## Cài đặt và chạy

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
if (-not (Test-Path .env)) { Copy-Item .env.example .env }
# Điền GEMINI_API_KEY nếu dùng .env cục bộ
streamlit run app.py
```

Ứng dụng đọc `GEMINI_API_KEY` từ process environment; `load_dotenv` tại project
root giúp nạp biến này từ `.env` khi phát triển cục bộ. Không commit `.env`.

## Validation gate

```powershell
$env:PYTHONPATH="src"
python -B -m unittest discover -s tests -v
python -B -m compileall -q app.py src
python -m pip check
git diff --check
```

Suite dùng `unittest` cho model, input, pipeline, summarizer, CSS contract và
repository/documentation hygiene. Repo chưa có browser E2E, live API test,
NVDA audit, user study hoặc dataset đánh giá factual accuracy có thể tái chạy.

## Cấu trúc chính

- `app.py`: entry point và workflow Streamlit.
- `src/accessibility_analyst/`: adapter, schema, AI services, TTS, pipeline và UI.
- `tests/`: unit/repository contract tests.
- `docs/`: tài liệu canonical, nguồn gốc và artifact lịch sử có nhãn.
- `archive/happy-case-mvp/`: MVP cũ để đối chiếu; production không import.
- `_bmad-output/`: artifact làm việc local, bị Git ignore và không phải nguồn
  trạng thái dự án.
