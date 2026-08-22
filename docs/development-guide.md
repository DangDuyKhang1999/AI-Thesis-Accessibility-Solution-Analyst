# Hướng dẫn phát triển

## Thiết lập

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
if (-not (Test-Path .env)) { Copy-Item .env.example .env }
```

Ứng dụng đọc `GEMINI_API_KEY` từ process environment. `load_dotenv` tại project
root cho phép dùng `.env` cục bộ; không commit file này và không in key/log
provider response có dữ liệu nhạy cảm.

`requirements.txt` hiện được dùng chung với Happy Case archive. `requests` và
`pyttsx3`, cùng biến tùy chọn `HF_TOKEN` trong `.env.example`, chỉ phục vụ
`archive/happy-case-mvp/`; production pipeline hiện dùng Gemini và gTTS.

## Chạy app

```powershell
streamlit run app.py
```

## Validation gate

```powershell
$env:PYTHONPATH="src"
python -B -m unittest discover -s tests -v
python -B -m compileall -q app.py src
python -m pip check
git diff --check
```

Đây là unit/repository contract gate. Nó không gọi Gemini/gTTS thật và không thay
thế browser E2E, factual evaluation hoặc accessibility audit. Kết quả/giới hạn
hiện hành nằm tại [process.md](process.md).

Chạy targeted test khi phát triển:

```powershell
$env:PYTHONPATH="src"
python -B -m unittest tests.test_repository_hygiene -v
python -B -m unittest tests.test_ui -v
```

## Quy ước thay đổi

- Viết test thất bại trước khi thêm hành vi.
- Inject fake provider khi test analyzer/composer/speech; unit test không gọi mạng.
- Không hard-code cấu trúc từ một tài liệu mẫu vào production prompt.
- Khi đổi constructor/service, restart Streamlit để tránh module cũ trong memory.
- UI thay đổi trong `src/accessibility_analyst/ui.py`; logic pipeline không đặt
  trong CSS/markup.
- Thêm dependency runtime vào `requirements.txt`.
- Khi thêm, đổi tên hoặc xóa file trong `docs/`, cập nhật `docs/index.md` đúng một
  target; guard sẽ kiểm tra link và heading anchor.
- Claim chất lượng phải chỉ rõ bằng chứng. Dùng “prompt yêu cầu” hoặc “heuristic”
  khi code không enforce semantics.

## Smoke test thủ công

Đây là checklist cần thực hiện, không phải bằng chứng đã hoàn tất:

1. Upload ảnh rồi PDF nhiều trang; xác nhận ba vùng desktop và flow một cột ở
   viewport hẹp.
2. Xác nhận inspector thu vừa preview trang đầu, popover mở ảnh lớn và không có
   navigation giả cho các trang khác.
3. Chạy phân tích với key test; xác nhận result theo thứ tự trang, audio,
   narrative, badges và component expander.
4. Kiểm tra trạng thái rỗng/loading/error, focus order và thao tác chỉ bàn phím.
5. Đối chiếu narrative với structured data và ảnh. Marker/coverage heuristic có
   thể cần kiểm tra thủ công; không mặc định bốn đoạn luôn đúng.

Live API smoke cần mạng và có thể phát sinh quota/chi phí. Không lưu sample chứa
dữ liệu doanh nghiệp nếu chưa được phép.
