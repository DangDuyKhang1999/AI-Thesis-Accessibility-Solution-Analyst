# Đề xuất triển khai MVP ban đầu

> **Trạng thái tài liệu:** Artifact lịch sử/chưa kiểm chứng. Tài liệu này ghi lại
> phương án miễn phí được đề xuất trong giai đoạn đầu, không phải stack hoặc claim
> chất lượng hiện tại. Các con số hiệu năng, quota, độ chính xác và chi phí bên
> dưới là claim của proposal gốc, chưa có citation/evaluation trong repo. Xem
> [stack hiện hành](../technology-stack.md) và
> [trạng thái hiện tại](../process.md).

Nội dung bên dưới đã được biên tập lại thành Markdown để dễ đọc, không phải bản
chép nguyên văn. Bản gốc trước khi định dạng vẫn truy xuất chính xác từ lịch sử
Git bằng `git show 4e145d0:docs/references/original-mvp-proposal.md`.

## Mục tiêu của proposal

Phương án ban đầu hướng tới hệ thống diễn giải dữ liệu doanh nghiệp cho người
khiếm thị bằng công nghệ mã nguồn mở chạy local hoặc free-tier API trong giai
đoạn 2025–2026. Proposal giả định máy cá nhân có GPU hoặc CPU với tối thiểu 16 GB
RAM và ưu tiên chi phí tiền mặt bằng không.

## Pipeline kỹ thuật được đề xuất lúc đầu

| Bước | Công nghệ đề xuất | Lý do được nêu trong proposal |
| --- | --- | --- |
| Layout parsing | IBM Docling local | Mã nguồn mở MIT, trích xuất bảng/cấu trúc và xuất Markdown |
| Multimodal reasoning | Gemini 1.5 Flash free tier | Proposal nêu 1.500 request/ngày và context một triệu token |
| Local fallback | Qwen2.5-VL-7B qua Ollama | Chạy offline và được mô tả là mạnh với biểu đồ Á Đông |
| Validation/schema | Pydantic AI | Framework mã nguồn mở để ép kiểu JSON và đề xuất self-correction |
| Audio | VieNeu-TTS local | Model mã nguồn mở, TTS Việt/Anh chạy local và xuất WAV |

Các lựa chọn trên thuộc proposal lịch sử. Khi cần đối chiếu với hệ thống đang
được duy trì, xem [stack hiện hành](../technology-stack.md).

## Hướng dẫn triển khai được đề xuất

### 1. Trích xuất cấu trúc bằng IBM Docling

Proposal đề nghị dùng `DoclingLoader` thay Azure Document Intelligence để chuyển
ảnh dashboard/PDF thành Markdown, giữ ranh giới bảng bằng ký tự `|---|`. Tài liệu
gốc tuyên bố Docling xử lý table structure nhanh hơn OCR thông thường 30 lần và
hoàn toàn miễn phí cho nghiên cứu, nhưng repo không chứa benchmark hoặc nguồn
kiểm chứng claim đó.

### 2. Suy luận đa phương thức với Gemini 1.5 Flash

Ảnh cùng Markdown từ bước Docling sẽ được gửi lên Gemini. Proposal gọi kỹ thuật
prompt là “Charts-of-Thought”: trích xuất → xác minh → diễn giải, đồng thời nêu
free-tier 1.500 request/ngày và context một triệu token để nạp hàng chục screenshot
trong một phiên. Bản gốc gọi Gemini 1.5 Flash là lựa chọn số một cho sinh viên và
tuyên bố kỹ thuật này có thể đạt độ chính xác ngang con người; các claim đó không
được dùng làm bằng chứng cho hệ thống hiện tại.

### 2a. Local fallback bằng Qwen2.5-VL-7B

Proposal đặt Qwen2.5-VL-7B chạy qua Ollama làm đường dự phòng offline trên phần
cứng cá nhân.

### 3. Kiểm soát output bằng Pydantic AI

Proposal dự kiến dùng Pydantic AI, khai báo model dữ liệu và tự động yêu cầu AI
sửa lại khi thiếu thông tin quan trọng, ví dụ tên nút bấm.
Ví dụ gốc:

```python
class UI_Report(BaseModel):
    target_name: str  # Tên màn hình
    primary_action: str  # Hành động chính (Ví dụ: Nhấn Đăng nhập)
    table_summary: Optional[str]  # Tóm tắt bảng nếu có
```

### 4. Tạo audio bằng VieNeu-TTS

Proposal dự kiến chạy VieNeu-TTS như local Docker API, sinh WAV Việt/Anh và lập
trình để AI thêm khoảng nghỉ thủ công nhằm mô phỏng SSML, giúp người khiếm thị
nghe bảng dễ hơn. Bản gốc mô tả model dựa trên Qwen 0.5B, tối ưu tiếng Việt và
hỗ trợ English–Vietnamese cho tài liệu CNTT.

## Demo được hình dung trong proposal

1. Input là ảnh bảng “Mã lỗi hệ thống”.
2. Docling báo đây là bảng bốn cột, mười dòng.
3. Gemini nhận diện lỗi 500 xuất hiện nhiều nhất và dịch thành “Lỗi máy chủ nội
   bộ”.
4. VieNeu-TTS đọc “Báo cáo mã lỗi”, nghỉ 0,5 giây rồi nêu lỗi máy chủ chiếm tỷ lệ
   cao nhất.

Đây là scenario minh họa, không phải fixture, test case hay kết quả evaluation
được lưu trong repository.

## So sánh chi phí trong proposal gốc

| Thành phần | Giải pháp trả phí được nêu | Phương án nghiên cứu được nêu | Tiết kiệm claim gốc |
| --- | --- | --- | ---: |
| Parsing | Azure Document Intelligence, 10 USD/1.000 trang | IBM Docling local | 10 USD |
| Reasoning | GPT-4o, 15 USD/1M token | Gemini 1.5 Flash free tier | 15 USD |
| TTS | ElevenLabs, 22 USD/tháng | VieNeu-TTS local | 22 USD |

Proposal kết luận chi phí tiền mặt có thể bằng 0, chỉ còn điện/phần cứng. Con số
“100% tiết kiệm” và đơn giá gốc không được duy trì như dữ liệu giá hiện hành.

## Kết luận lịch sử

Đề xuất ban đầu đặt trọng tâm vào Docling + Gemini + local TTS, gọi tổ hợp này là
một demo MVP “SOTA” không cần ngân sách và cho rằng giá trị nghiên cứu nằm ở cách
cấu trúc prompt để AI mô tả khả năng “hình dung”/Generative UI cho người khiếm
thị. Dự án sau đó chọn pipeline khác; tài liệu này chỉ còn vai trò ghi lại hướng
khởi đầu, không xác nhận các claim trên.
