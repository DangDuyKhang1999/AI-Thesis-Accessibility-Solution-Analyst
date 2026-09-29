# Trạng thái và backlog

- **Ngày đối chiếu:** 2026-09-29
- **Baseline implementation:** `4e145d03dcc581bddeacf2fab0c7ed5c0fb5feac`
- **Mức trưởng thành:** MVP chức năng; validation nghiên cứu và accessibility thực tế chưa hoàn tất
- **Vai trò file:** nguồn trạng thái duy nhất của repository

## Implemented

1. `InputAdapter` nhận PNG/JPEG/WebP hoặc render PDF thành `InputPage` PNG theo
   thứ tự.
2. `app.py` lặp tuần tự từng trang. Mỗi trang chạy extraction → Pydantic shape
   validation → composition → heuristic hậu xử lý → gTTS.
3. UI chỉ cho chọn output Việt/Anh. Prompt analyzer yêu cầu tự nhận diện nguồn
   Anh/Nhật/Việt khi caller truyền `None`.
4. Desktop workspace có ba vùng: control rail, analysis workspace và document
   inspector. Kết quả có audio, narrative và component details theo trang;
   inspector chỉ preview trang đầu và có popover mở lớn.
5. Happy Case cũ nằm trong `archive/happy-case-mvp/`; source production không
   import archive.

## Bằng chứng có thể tái chạy

| Phạm vi | Bằng chứng hiện có | Không chứng minh |
| --- | --- | --- |
| Schema/model | Pydantic từ chối field dư và chuỗi bắt buộc rỗng trong các case đã test | Dữ kiện đúng với ảnh, components/facts/relationships đầy đủ hoặc không rỗng |
| Input | Unit test cho bytes không rỗng với image MIME và MIME không hỗ trợ; code path PDF dùng PyMuPDF | Decode/xác thực nội dung ảnh, bộ PDF lỗi/đa trang đại diện, giới hạn kích thước hoặc số trang |
| Analyzer/pipeline | Fake provider kiểm tra prompt auto-detect, model mặc định, orchestration, text/audio output | Gemini live, độ chính xác nhận diện hoặc dịch thuật |
| Composition | Test prompt, marker replacement và token/substr coverage heuristic | Tương đương ngữ nghĩa, factual completeness hoặc chất lượng nghe hiểu |
| UI | Test chuỗi CSS cho tương phản, focus, responsive và inspector ảnh dọc | Browser layout thực, WCAG conformance, keyboard flow hoặc screen reader |
| Repository/docs | Guard archive boundary; assignment `API_KEY`/`HF_TOKEN` và `load_dotenv` ở hai archive entrypoint; ignore rule, index, link/anchor và banner nguồn nghiên cứu | Scan secret tổng quát trong production, CI trên môi trường khác hoặc deployment |

Tại baseline, suite discovery có 42 unit/repository contract tests. Con số này
là ảnh chụp tại ngày đối chiếu;
lệnh discovery bên dưới mới là nguồn xác nhận khi suite thay đổi.

```powershell
$env:PYTHONPATH="src"
python -B -m unittest discover -s tests -v
python -B -m compileall -q app.py src
python -m pip check
git diff --check
```

Repo chưa chứa browser E2E, live API test, dataset/ground truth, NVDA audit hoặc
user study có thể tái chạy.

## Giới hạn đang mở

- JSON được `json.loads` rồi Pydantic kiểm tra hình dạng; SDK không dùng response
  schema và không có bước đối chiếu lại ảnh.
- Coverage fallback dựa trên substring/tập token, có thể bỏ sót hoặc đánh dấu
  nhầm nội dung đã được diễn đạt.
- Prompt yêu cầu bốn đoạn và dữ liệu không đọc được, nhưng code không validate
  đủ bốn đoạn và schema không có confidence/unreadable-region field.
- `GEMINI_API_KEY` được đọc từ process environment; `.env` ở root chỉ là cách
  nạp biến thuận tiện qua `load_dotenv`.
- Gemini và gTTS cần mạng; chưa có retry, timeout, cache, quota/cost telemetry hay
  phân loại lỗi theo stage.
- Chưa hỗ trợ DOCX; yêu cầu gốc không chỉ định định dạng file bắt buộc.

## Backlog validation nghiên cứu

- [ ] Chuẩn bị bộ mẫu table/chart/diagram/layout bằng nguồn Anh, Nhật và Việt.
- [ ] Ghi ground truth cho label, giá trị, đơn vị, quan hệ, thứ bậc và vùng không
  xác định được.
- [ ] Định nghĩa rubric và ngưỡng đạt cho factual accuracy, structural coverage,
  translation fidelity và listening clarity.
- [ ] Tách đánh giá extraction khỏi narrative/TTS và lưu kết quả định lượng với
  model/version cố định.

## Backlog reliability

- [ ] Giới hạn dung lượng upload và số trang PDF.
- [ ] Thêm timeout/retry cho extraction, composition và gTTS.
- [ ] Phân loại lỗi input, JSON, schema, composition và speech ở UI.
- [ ] Cache theo file hash, target language và model version.
- [ ] Theo dõi latency, request count và chi phí/quota mà không log dữ liệu nhạy cảm.
- [ ] Kiểm tra nhất quán source/target language tại model boundary.

## Backlog accessibility

- [ ] Kiểm thử keyboard flow và audit NVDA trên Windows.
- [ ] Kiểm tra flow input → status → audio/narrative → component details → inspector.
- [ ] Đánh giá với người dùng mục tiêu theo phương pháp và consent rõ ràng.
- [ ] Xác định active exploration theo trường dữ liệu có cần thiết cho nghiệm thu,
  hay narrative thụ động đã đủ.

## Backlog delivery

- [ ] Thêm dependency lock, CI và browser E2E có thể tái chạy.
- [ ] Chỉ tạo cấu hình deployment sau khi evaluation đạt ngưỡng.

## Điều kiện hoàn thành

MVP nghiên cứu chỉ được xem là đạt khi chạy trên dataset đại diện, có số đo
factual/structural rõ ràng, narrative và audio Việt/Anh được đánh giá, đồng thời
lưu kết quả keyboard, screen-reader và user validation bằng phương pháp có thể
kiểm tra. Unit test hiện tại là điều kiện cần, không phải bằng chứng nghiệm thu.

Contract ổn định nằm tại [spec.md](spec.md).
