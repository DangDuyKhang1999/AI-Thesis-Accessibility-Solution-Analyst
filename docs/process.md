# Tiến độ hiện tại của dự án

**Ngày đánh giá:** 2026-08-03  
**Nguồn đánh giá:** mã nguồn, tài liệu và trạng thái Git trong repository  
**Mức trưởng thành:** PoC / MVP happy-case sớm

## Tóm tắt điều hành

Dự án đã chứng minh được luồng cốt lõi trên giao diện web: tải một ảnh, gửi ảnh
cho Gemini để sinh mô tả tiếng Việt, sau đó tạo và phát audio. Đây là bằng chứng
kỹ thuật có giá trị cho ý tưởng luận văn, nhưng chưa phải MVP nghiên cứu hoàn
chỉnh vì chưa có kiến trúc kiểm thử được, bộ dữ liệu đánh giá, đo chất lượng,
schema đầu ra hoặc kiểm chứng accessibility với người dùng/screen reader.

## Phần trăm tiến độ sơ bộ

Con số dùng để nắm nhanh, không phải số đo chính thức:

- **PoC/happy case:** khoảng **75%** — luồng chính đã có, nhưng còn phụ thuộc API
  thật và chưa được kiểm thử end-to-end có kiểm soát.
- **MVP nghiên cứu theo `spec.md`: khoảng 35%**.
- **Phạm vi đầy đủ của đề tài:** khoảng **20%** — chưa có PDF/layout parsing,
  đa ngôn ngữ, schema validation và đánh giá thực nghiệm hoàn chỉnh.

Mức 35% được tính theo trọng số sau:

| Nhóm | Trọng số | Mức hoàn thành | Điểm đóng góp |
| --- | ---: | ---: | ---: |
| Happy path ảnh → text → audio | 25% | 80% | 20.0% |
| Bảo mật và khả năng tái lập | 15% | 50% | 7.5% |
| Kiến trúc và unit test | 20% | 15% | 3.0% |
| Validation và độ tin cậy | 15% | 20% | 3.0% |
| Accessibility thực chứng | 10% | 10% | 1.0% |
| Dataset và đánh giá nghiên cứu | 15% | 5% | 0.75% |
| **Tổng** | **100%** |  | **35.25% ≈ 35%** |

Khi cập nhật tiến độ, chỉ thay cột “Mức hoàn thành” nếu có bằng chứng như test,
commit, biên bản accessibility hoặc kết quả thí nghiệm. Đánh giá theo mốc:

| Mốc | Trạng thái | Nhận định |
| --- | --- | --- |
| Chứng minh ý tưởng kỹ thuật | Đạt phần lớn | Happy case ảnh → text → audio đã có |
| MVP demo ổn định | Đang thực hiện | Thiếu validation, test và xử lý lỗi có cấu trúc |
| MVP nghiên cứu | Giai đoạn đầu | Chưa có dataset, baseline, rubric và kết quả đo |
| Phạm vi đầy đủ trong đề xuất | Chưa bắt đầu đáng kể | Chưa có PDF/layout parser, đa ngôn ngữ, schema validation |

## Cách chạy ứng dụng hiện tại

### Yêu cầu

- Python 3.12 được khuyến nghị.
- Có Gemini API key hợp lệ.
- Có kết nối mạng cho Gemini; Hugging Face và gTTS cũng cần mạng.
- `HF_TOKEN` là tùy chọn vì app có thể thử giọng Việt cục bộ rồi gTTS.

### Cài đặt lần đầu trên PowerShell

Chạy từ thư mục gốc dự án:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Cấu hình và chạy

```powershell
Copy-Item .env.example .env
# Mở .env và điền GEMINI_API_KEY; HF_TOKEN là tùy chọn.
streamlit run streamlit_app.py
```

Streamlit thường mở `http://localhost:8501`. Trên giao diện: chọn một ảnh PNG,
JPG, JPEG hoặc WebP, nhấn **Sinh audio**, sau đó đọc mô tả và nghe audio ở cột
kết quả. Không đưa key thật vào `.env.example` hoặc source code.

### Chạy kiểm tra repository

```powershell
python -m unittest discover -s tests -v
```

### Chạy CLI legacy nếu cần đối chiếu

```powershell
Copy-Item .env.example .env # bỏ qua nếu .env đã tồn tại
python run_happy_case.py --image "assets/samples/bar.png"
```

CLI ghi text/audio vào `output/`; thư mục này đã nằm trong `.gitignore`.

## Đã hoàn thành hoặc đã có

- Giao diện Streamlit tải và xem trước ảnh PNG/JPEG/WebP.
- Gọi `gemini-2.5-flash-lite` để tạo mô tả tiếng Việt.
- Làm sạch một phần Markdown/ký hiệu và chuẩn hóa số lớn cho TTS.
- Hiển thị văn bản và phát audio trực tiếp trong trình duyệt.
- TTS có ba đường: Hugging Face Bark, giọng Việt local qua pyttsx3, rồi gTTS.
- Có CLI prototype và hai ảnh mẫu phục vụ happy case.
- Có tài liệu đề tài, đề xuất MVP cũ và một bài báo tham khảo.
- Trong đợt rà soát này: tài liệu/công cụ cũ đã được phân loại và kiểm tra vệ
  sinh repo được bổ sung. Ngày 2026-08-03, credential được chuyển từ source sang
  `.env`; `.env` và thư mục backup chứa key đều bị Git ignore.
- BMAD Method 6.10.0 đã được cài cho Codex; đây là công cụ quy trình, không làm
  tăng phần trăm chức năng của MVP.

## Đang thiếu so với đặc tả

- Không có unit test cho logic xử lý; test hiện tại mới bảo vệ cấu trúc và secret.
- Logic UI, Gemini, chuẩn hóa và TTS còn tập trung trong một file khoảng 376 dòng.
- Chưa xác thực dung lượng/nội dung thật của file, chưa có timeout và taxonomy lỗi ở UI.
- Chưa có output schema, bước xác minh dữ kiện hoặc cơ chế chống hallucination đo được.
- Chưa triển khai Docling/OCR, PDF, nhiều ảnh hoặc đa ngôn ngữ.
- Chưa có CI, packaging, dependency lock, deployment hoặc observability.
- Chưa có accessibility audit với keyboard/NVDA và chưa có nghiên cứu người dùng.
- Chưa có bộ dữ liệu chuẩn, baseline, rubric, thí nghiệm hay số liệu luận văn.

## Rủi ro và mức ưu tiên

| Mức | Rủi ro | Hành động tiếp theo |
| --- | --- | --- |
| P0 | Credential thật từng được hard-code | Thu hồi và cấp lại cả Gemini key lẫn HF token |
| P0 | Repository chưa có commit nền | Quét secret, kiểm thử rồi tạo commit đầu tiên |
| P0 | Code ghép chặt, khó kiểm thử | Tách config, analysis, normalizer và speech bằng TDD |
| P1 | Kết quả AI chưa được đo độ đúng | Tạo ground truth, rubric và baseline |
| P1 | Sản phẩm hỗ trợ người khiếm thị nhưng chưa audit accessibility | Kiểm thử keyboard và NVDA, ghi bằng chứng |
| P1 | TTS fallback nuốt lỗi provider | Trả metadata và lỗi có cấu trúc cho UI |
| P2 | Phạm vi đề xuất quá rộng | Hoàn tất MVP một ảnh tiếng Việt trước khi mở rộng |

## Bằng chứng trong repository

- `streamlit_app.py`: web happy case và toàn bộ pipeline hiện tại.
- `scripts/legacy/`: CLI ảnh → text/audio và thử nghiệm TTS cũ.
- `assets/samples/`: hai ảnh dashboard mẫu.
- `docs/references/`: yêu cầu ban đầu, đề xuất MVP, trạng thái cũ và bài báo.
- `tests/test_repository_hygiene.py`: kiểm tra tài liệu chuẩn, ignore và secret.
- `_bmad/` và `.agents/skills/`: BMAD Core/BMM và skill tích hợp Codex.
- Git: nhánh `main` chưa có commit tại thời điểm khảo sát; toàn bộ file đang untracked.

## Mốc tiếp theo được khuyến nghị

Mốc gần nhất là “baseline an toàn, tái lập”: thu hồi key đã lộ, tạo commit đầu
tiên, tách logic lõi bằng TDD và chạy được test offline. Sau đó mới audit
accessibility và xây bộ đánh giá nghiên cứu. Chi tiết thứ tự nằm trong `plan.md`.

## Cách cập nhật file này

Sau mỗi mốc, cập nhật ngày, chuyển hạng mục giữa “đã có” và “đang thiếu”, thêm
bằng chứng test/commit và ghi rủi ro mới. Chỉ đánh dấu hoàn thành khi có lệnh kiểm
chứng, kết quả đánh giá hoặc biên bản test tương ứng.
