# Đặc tả dự án AI Accessibility Solution Analyst

**Cập nhật:** 2026-08-03  
**Trạng thái:** Đặc tả mục tiêu cho MVP nghiên cứu, đã đối chiếu với source hiện tại

## 1. Bối cảnh và vấn đề

Dashboard, bảng thống kê, biểu đồ, sơ đồ và ảnh chụp giao diện doanh nghiệp chứa
quan hệ không gian mà screen reader tuyến tính khó truyền đạt. Dự án hướng tới
chuyển nội dung trực quan đó thành mô tả có cấu trúc, ngắn gọn và có thể nghe
được, ưu tiên nhân viên khiếm thị sử dụng tiếng Việt.

## 2. Mục tiêu sản phẩm

Người dùng tải lên một ảnh tài liệu hoặc giao diện; hệ thống phân tích ảnh bằng
mô hình đa phương thức, tạo mô tả tiếng Việt phù hợp TTS và phát âm thanh ngay
trong trình duyệt.

## 3. Phạm vi MVP

### Baseline đang có

Source hiện tại đã triển khai một ứng dụng Streamlit nguyên khối trong
`streamlit_app.py`: nhận một ảnh, gọi Gemini, làm sạch mô tả tiếng Việt và tạo
audio qua chuỗi fallback Hugging Face → giọng Việt cục bộ → gTTS. Đây là baseline
để phát triển tiếp, không phải kiến trúc đích.

### Chức năng bắt buộc

- Nhận một ảnh PNG, JPEG hoặc WebP trong mỗi lượt xử lý.
- Hiển thị ảnh xem trước và trạng thái xử lý rõ ràng.
- Sinh mô tả tiếng Việt không dùng Markdown hoặc ký hiệu gây khó nghe qua TTS.
- Không bịa nội dung; vùng không nhận diện được phải được nêu rõ.
- Hiển thị văn bản để người dùng kiểm tra và phát audio trên trang.
- Lấy credential từ biến môi trường, không lưu bí mật trong mã nguồn.
- Có thông báo dễ hiểu khi thiếu cấu hình hoặc dịch vụ ngoài thất bại.

### Chưa thuộc MVP hiện tại

- PDF nhiều trang, nhiều ảnh trong một phiên và phân tích luồng nhiều màn hình.
- Input Nhật/Anh, dịch đầu ra Anh/Việt và lựa chọn ngôn ngữ.
- Docling/OCR chuyên dụng, schema Pydantic và cơ chế tự sửa đầu ra.
- Tài khoản, lưu lịch sử, phân quyền và triển khai production.

## 4. Kiến trúc mục tiêu gần

Luồng gồm năm ranh giới độc lập: tiếp nhận input, phân tích thị giác, chuẩn hóa
mô tả, tổng hợp giọng nói và trình bày kết quả. Giao diện Streamlit chỉ điều
phối; logic nghiệp vụ cần được tách thành module để kiểm thử mà không gọi mạng.
Gemini là bộ phân tích hiện tại. TTS ưu tiên dịch vụ Hugging Face, sau đó giọng
Việt cục bộ và gTTS; chiến lược này cần được biểu diễn rõ bằng trạng thái nguồn
audio và lỗi tương ứng.

## 5. Yêu cầu phi chức năng

- Accessibility: thao tác bàn phím, nhãn điều khiển rõ, focus hợp lý, thông báo
  trạng thái có thể đọc bởi screen reader và không phụ thuộc riêng vào màu sắc.
- Bảo mật: key chỉ đến từ môi trường/secrets; log không chứa key hoặc dữ liệu ảnh.
- Kiểm thử: logic thuần có unit test; tích hợp API được cô lập ở adapter; có bộ
  ảnh chuẩn để đánh giá lặp lại.
- Khả năng tái lập: khóa phiên bản môi trường và ghi lại model/prompt khi đánh giá.
- Riêng tư: ảnh chỉ được giữ trong bộ nhớ trong lượt xử lý, trừ khi người dùng
  chủ động yêu cầu lưu.

## 6. Tiêu chí nghiệm thu MVP nghiên cứu

1. Cài mới từ README và chạy được bằng một lệnh Streamlit.
2. Không có credential thật trong Git; secret cũ đã được thu hồi và thay mới.
3. Happy case ảnh mẫu tạo được văn bản tiếng Việt và audio.
4. Thiếu API key, ảnh sai định dạng và lỗi nhà cung cấp đều có thông báo xác định.
5. Unit test bao phủ chuẩn hóa văn bản, MIME, lỗi cấu hình và lựa chọn TTS fallback.
6. Bộ đánh giá có ít nhất 20 ảnh thuộc bảng, biểu đồ và giao diện; kết quả được
   chấm theo độ đúng dữ kiện, độ đầy đủ cấu trúc, mức bịa và khả năng nghe hiểu.
7. Kiểm thử thủ công với keyboard và ít nhất một screen reader được ghi nhận.

## 7. Ma trận yêu cầu và trạng thái

| Nhóm yêu cầu | Trạng thái hiện tại | Bằng chứng/Ghi chú |
| --- | --- | --- |
| Upload một ảnh và preview | Đã có | `streamlit_app.py` |
| Gemini sinh mô tả tiếng Việt | Đã có happy case | Cần `GEMINI_API_KEY` và mạng |
| Văn bản thuần tối ưu TTS | Có một phần | Có làm sạch ký hiệu và chuẩn hóa số lớn |
| Phát audio trên web | Đã có happy case | HF/local/gTTS fallback |
| Secret qua môi trường | Đã đạt ở source hiện tại | Credential nằm trong `.env` bị Git ignore; vẫn nên thu hồi key từng bị lộ |
| Xử lý lỗi có cấu trúc | Một phần | UI hiện gom nhiều lỗi vào exception tổng quát |
| Unit test nghiệp vụ | Chưa có | 4 test hiện tại chỉ kiểm tra vệ sinh repo |
| Keyboard/screen reader audit | Chưa có | Chưa có biên bản NVDA |
| Dataset và đánh giá nghiên cứu | Chưa có | Mới có 2 ảnh mẫu, chưa có ground truth |
| PDF/layout parsing/đa ngôn ngữ | Chưa có | Nằm ngoài MVP gần nhất |

## 8. Câu hỏi nghiên cứu dự kiến

- Mô tả do mô hình đa phương thức sinh ra cải thiện khả năng hiểu cấu trúc trực
  quan bao nhiêu so với OCR/screen reader tuyến tính?
- Prompt có cấu trúc và bước xác minh dữ kiện ảnh hưởng thế nào đến hallucination?
- Độ dài và cấu trúc mô tả nào tối ưu cho việc nghe thay vì đọc?

## 9. Nguồn hiện có

Tài liệu gốc và bài báo tham khảo được bảo tồn tại `docs/references/`. Chúng là
đầu vào định hướng; các tuyên bố về model, giá hoặc quota cần được xác minh lại
tại thời điểm viết luận văn.
