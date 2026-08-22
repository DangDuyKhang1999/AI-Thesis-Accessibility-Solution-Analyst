# Thiết kế tách MVP và codebase chính thức

> **Trạng thái tài liệu:** Artifact lịch sử — foundation này đã hoàn tất ngày
> 2026-08-03. Danh sách module và data flow bên dưới là thiết kế ban đầu, đã được
> [kiến trúc hiện hành](../../architecture.md) thay thế. Xem
> [trạng thái hiện tại](../../process.md); nội dung còn lại được giữ để truy vết.

## Mục tiêu

Đóng gói Happy Case MVP đã hoàn thành thành tài liệu tham chiếu có thể chạy lại,
sau đó phát triển hệ thống chính thức theo `docs/spec.md` mà không tiếp tục mở
rộng file Streamlit thử nghiệm hiện tại.

## Cấu trúc

```text
archive/happy-case-mvp/       # Bản demo cũ, chỉ bảo trì để chạy lại
  streamlit_app.py
  run_happy_case.py
  assets/samples/
src/accessibility_analyst/    # Package chính thức
  models.py
  input_adapter.py
  analyzer.py
  language_service.py
  speech.py
  pipeline.py
app.py                        # Entry point Streamlit chính thức
tests/                        # Unit và integration tests
```

`.env`, `.gitignore`, `requirements.txt` và `docs/` tiếp tục nằm tại root. Các
script thử nghiệm trùng lặp đã bị xóa; toàn bộ Happy Case chỉ còn một bản trong
`archive/happy-case-mvp/`.

## Ranh giới thành phần

- `models`: kiểu dữ liệu và enum dùng chung; không gọi mạng hoặc UI.
- `input_adapter`: kiểm tra ảnh/PDF và chuyển tài liệu thành các trang có thứ tự.
- `analyzer`: gọi LLM và trả về mô tả có schema cho bảng, biểu đồ, sơ đồ, layout.
- `language_service`: nhận diện ngôn ngữ nguồn và render mô tả Anh/Việt.
- `speech`: chuyển văn bản sang audio bằng provider phù hợp với ngôn ngữ đích.
- `pipeline`: điều phối các service, không chứa logic Streamlit.
- `app.py`: thu thập input và hiển thị kết quả; không chứa logic nghiệp vụ lõi.

## Luồng dữ liệu

Ảnh hoặc PDF đi qua `input_adapter`, từng trang được đưa vào `analyzer`, kết quả
schema được `language_service` chuyển thành mô tả ngôn ngữ tự nhiên Anh/Việt,
sau đó `speech` tạo audio. `pipeline` trả về đồng thời component, mô tả và audio
cho `app.py`.

## Di chuyển MVP

MVP được chuyển, không nhân bản, vào `archive/happy-case-mvp/`. Đường dẫn đọc
`.env` và sample được điều chỉnh theo project root để MVP vẫn chạy bằng lệnh
được ghi trong README của archive. Code chính thức không import module từ
archive; chỉ được tham khảo hành vi đã chứng minh hoạt động.

## Xử lý lỗi

Các module lõi phát sinh exception có kiểu và thông báo rõ ràng cho input không
hợp lệ, response LLM sai schema, ngôn ngữ không hỗ trợ và lỗi TTS. `app.py` chịu
trách nhiệm chuyển lỗi thành thông báo dễ hiểu; không nuốt lỗi dữ liệu quan trọng.

## Kiểm thử và thứ tự triển khai

Mỗi module được phát triển test-first. Bắt đầu bằng model có cấu trúc, sau đó
analyzer, input adapter, đa ngôn ngữ, speech và pipeline. Test dùng fake provider
để không phụ thuộc API; smoke test thủ công dùng key cục bộ trong `.env`. Sau khi
di chuyển, cả lệnh chạy MVP archive lẫn test hygiene hiện tại phải còn hoạt động.

## Ngoài phạm vi vòng đầu

Không xây tài khoản, phân quyền, database, deployment production hoặc tối ưu tải
lớn. Chỉ duy trì quản lý key qua `.env` và validation cần thiết để phát triển an
toàn; giá trị chính vẫn là mô tả cấu trúc trực quan và audio đa ngôn ngữ.
