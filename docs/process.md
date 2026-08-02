# Tiến độ hiện tại

**Ngày cập nhật:** 2026-08-03

**Mức trưởng thành:** MVP chức năng đang hoàn thiện chất lượng

## Ước lượng sơ bộ

| Phạm vi | Tiến độ | Bằng chứng |
| --- | ---: | --- |
| Pipeline chức năng theo yêu cầu đề tài | 84% | Ảnh/PDF → JSON cấu trúc → mô tả có nhãn ngữ nghĩa → audio |
| UI demo | 88% | Midnight Aurora, tương phản đồng bộ, desktop/mobile smoke test |
| Độ tin cậy và đánh giá nghiên cứu | 25% | Có unit test; chưa có dataset/rubric/user study |
| Toàn bộ đề tài | 60% | Chức năng chính có, phần đánh giá khoa học còn thiếu |

Các tỷ lệ chỉ để nắm nhanh, không phải số đo nghiệm thu.

## Luồng đang chạy

1. `InputAdapter` nhận ảnh hoặc render từng trang PDF thành PNG.
2. `GeminiAnalyzerClient` tự phát hiện ngôn ngữ Anh/Nhật/Việt và trả JSON theo
   `StructuredDescription` gồm table/chart/diagram/layout.
3. `GeminiSummarizer` nhận JSON và viết bốn đoạn: `Tổng quan`, `Số liệu chi
   tiết`, `Phân tích số liệu`, `Nhận định`; tự gom nhãn lặp theo dữ liệu hiện tại.
4. Hậu xử lý thay các marker `1–4` nếu model vẫn sinh ra, kiểm tra dữ kiện theo
   nhãn + giá trị và chỉ bổ sung phần thật sự còn thiếu.
5. `SpeechService` nhận chính văn bản đã chuẩn hóa và tạo MP3 Việt/Anh.
6. `app.py` hiển thị preview, mô tả, audio và cấu trúc nhận diện.

## Cách chạy

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
streamlit run app.py
```

Biến bắt buộc: `GEMINI_API_KEY`. Input source được AI tự phát hiện; người dùng
chỉ chọn output tiếng Việt hoặc tiếng Anh.

## Kiểm thử hiện tại

```powershell
$env:PYTHONPATH="src"
python -B -m unittest discover -s tests -v
python -B -m compileall -q app.py src
```

Suite hiện có 32 test, bao phủ model validation, input adapter, analyzer giả,
pipeline, composer prompt, section normalization, chống lặp dữ kiện, UI contrast
contract và repository hygiene.

## Đã hoàn thành

- Tách MVP cũ vào `archive/happy-case-mvp/`.
- Dựng package production trong `src/accessibility_analyst/`.
- Ảnh và PDF nhiều trang; auto-detect Anh/Nhật/Việt.
- Output mô tả và audio Việt/Anh.
- Schema cho bảng, biểu đồ, sơ đồ và layout.
- Pipeline AI hai lượt: extraction rồi composition.
- Narrative và voice dùng nhãn ngữ nghĩa thay vì đọc số phần `1–4` mơ hồ.
- Coverage fallback nhận diện dữ kiện đã được diễn đạt khác dấu câu/cách nối từ.
- UI Glassmorphism responsive, focus/reduced-motion và tương phản thống nhất cho
  progress, uploader, select, alert, expander và CTA.
- `.env` bị ignore; test quét credential trong active source.

## Còn thiếu

- Dataset chuẩn cho từng loại table/chart/diagram/layout và ba ngôn ngữ input.
- Rubric đo độ đúng dữ kiện, độ đầy đủ cấu trúc và khả năng nghe hiểu.
- Accessibility audit thực tế bằng keyboard, NVDA và người dùng khiếm thị.
- Retry/timeout có cấu trúc cho Gemini và gTTS; hiện lỗi được hiển thị chung.
- Cache kết quả, giới hạn kích thước/số trang PDF và quan sát chi phí API.
- CI, dependency lock và cấu hình deployment.
- DOCX chưa hỗ trợ; yêu cầu gốc không chỉ định định dạng bắt buộc.

## Bước tiếp theo

Ưu tiên xây bộ demo/evaluation bao phủ bốn loại component và ba ngôn ngữ input,
sau đó đo độ đúng và audit screen reader. Không mở rộng chức năng ngoài
`project-request.md` trước khi có bằng chứng chất lượng cho pipeline hiện tại.
