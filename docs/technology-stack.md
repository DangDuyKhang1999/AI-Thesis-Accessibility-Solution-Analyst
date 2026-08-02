# Tổng quan giải pháp công nghệ

## Bài toán cần giải quyết

Screen reader truyền thống đọc văn bản theo thứ tự tuyến tính nhưng không giải
thích tốt biểu đồ, bảng, sơ đồ và bố cục giao diện. Vì vậy, người khiếm thị có thể
nghe được chữ nhưng vẫn không hiểu dữ liệu đang thể hiện điều gì, các phần liên
quan với nhau ra sao hoặc đâu là kết luận quan trọng.

Giải pháp của dự án là tạo một lớp phân tích trung gian bằng AI: biến nội dung
trực quan thành dữ liệu có cấu trúc, diễn giải cấu trúc đó thành lời tự nhiên, sau
đó chuyển chính lời diễn giải thành âm thanh.

## Kiến trúc giải pháp

Hệ thống được chia thành năm tầng công nghệ:

| Tầng | Công nghệ | Vai trò giải quyết vấn đề |
| --- | --- | --- |
| Tiếp nhận tài liệu | Streamlit, PyMuPDF | Nhận ảnh/PDF và đưa mọi trang về dạng hình ảnh thống nhất để AI có thể xử lý |
| Hiểu nội dung trực quan | Gemini multimodal | Nhận diện ngôn ngữ, bảng, biểu đồ, sơ đồ, bố cục, nhãn, số liệu và quan hệ |
| Chuẩn hóa thông tin | JSON có schema, Pydantic | Biến kết quả AI thành cấu trúc kiểm tra được, hạn chế đầu ra tùy ý hoặc thiếu định dạng |
| Diễn giải dễ nghe | Gemini text generation và hậu xử lý ngôn ngữ | Chuyển dữ liệu có cấu trúc thành tổng quan, số liệu, phân tích và nhận định; hạn chế lặp và số thứ tự khó hiểu |
| Cung cấp khả năng tiếp cận | gTTS, giao diện Streamlit | Chuyển nội dung cuối thành MP3 và cho phép đọc/nghe/đối chiếu trên cùng giao diện |

## Vì sao cần hai lượt AI

Hệ thống không yêu cầu AI nhìn ảnh rồi lập tức tạo voice. Cách đó khó kiểm soát
việc bỏ sót số liệu, lặp nội dung hoặc suy diễn sai. Thay vào đó:

- Lượt thứ nhất tập trung vào **hiểu và trích xuất**: ảnh có những thành phần nào,
  chứa dữ kiện gì và các dữ kiện quan hệ ra sao.
- Kết quả được đưa về **dữ liệu có cấu trúc** để kiểm tra tính hợp lệ.
- Lượt thứ hai tập trung vào **diễn đạt**: biến dữ liệu đã chuẩn hóa thành lời tự
  nhiên phù hợp với người nghe.

Cách tách này giúp đánh giá độc lập hai vấn đề: AI có đọc đúng dữ liệu hay không,
và phần mô tả có dễ nghe, dễ hiểu hay không.

## Vai trò của từng công nghệ chính

### Gemini multimodal

Gemini đảm nhiệm phần khó nhất mà OCR thông thường không giải quyết được: hiểu
ý nghĩa trực quan. Ngoài chữ, mô hình cần xác định đâu là bảng, biểu đồ, sơ đồ,
vùng giao diện; đồng thời giữ lại số liệu, đơn vị, xu hướng, thứ bậc và so sánh.
Gemini cũng tự phát hiện đầu vào tiếng Anh, Nhật hoặc Việt.

### JSON schema và Pydantic

LLM có thể trả lời linh hoạt nhưng hệ thống cần đầu ra ổn định. Lớp schema buộc
kết quả phân tích phải có ngôn ngữ, loại thành phần, dữ kiện và quan hệ rõ ràng.
Nếu kết quả sai cấu trúc, hệ thống từ chối thay vì tiếp tục tạo một bản audio khó
kiểm chứng.

### Gemini text generation

Lượt AI thứ hai không phân tích lại ảnh mà diễn giải dữ liệu đã được chuẩn hóa.
Đầu ra được tổ chức theo bốn ý có nghĩa khi nghe: **Tổng quan**, **Số liệu chi
tiết**, **Phân tích số liệu** và **Nhận định**. Với tiếng Anh, hệ thống dùng các
nhãn tương ứng bằng tiếng Anh.

### Hậu xử lý ngôn ngữ

AI vẫn có thể tạo số thứ tự hoặc diễn đạt khác với dữ kiện gốc. Lớp hậu xử lý
thay các marker `1–4` bằng nhãn có nghĩa, kiểm tra các nhãn/số liệu/quan hệ đã
được nhắc đến và chỉ bổ sung thông tin thực sự thiếu. Mục tiêu là giữ độ đầy đủ
mà không làm voice lặp lại máy móc.

### gTTS

gTTS chuyển bản mô tả cuối cùng sang MP3 tiếng Việt hoặc tiếng Anh. Văn bản trên
màn hình và văn bản dùng để tạo voice là cùng một nội dung, giúp người dùng và
người đánh giá có thể đối chiếu.

### Streamlit và thiết kế giao diện

Streamlit cung cấp luồng sử dụng đơn giản: tải tài liệu, chọn ngôn ngữ đầu ra,
xem trạng thái, đọc mô tả và phát audio. Giao diện Midnight Aurora sử dụng độ
tương phản cao, hỗ trợ focus bàn phím và giảm chuyển động để phù hợp hơn với yêu
cầu accessibility.

## Luồng công nghệ tổng quát

```text
Ảnh hoặc PDF
  → chuẩn hóa từng trang
  → AI hiểu nội dung trực quan
  → dữ liệu có cấu trúc và được kiểm tra
  → AI diễn giải thành lời tự nhiên
  → chuẩn hóa và kiểm tra độ đầy đủ
  → văn bản dễ nghe
  → âm thanh MP3
```

## Giá trị của cách tiếp cận

- Không dừng ở OCR mà truyền đạt cả cấu trúc và quan hệ của dữ liệu.
- Tách “đọc đúng” và “nói dễ hiểu” thành hai giai đoạn có thể đánh giá riêng.
- Hỗ trợ đầu vào Anh–Nhật–Việt và đầu ra Anh–Việt.
- Giữ văn bản và voice nhất quán để thuận tiện kiểm chứng.
- Có thể mở rộng hoặc thay thế mô hình AI/TTS mà không thay đổi mục tiêu nghiệp vụ.

## Giới hạn hiện tại

- Gemini và gTTS cần kết nối Internet.
- Chất lượng phụ thuộc vào khả năng nhận diện của mô hình AI và chất lượng ảnh.
- Chưa có bộ dữ liệu đánh giá chính thức, ngưỡng độ chính xác hoặc nghiên cứu với
  người dùng khiếm thị.
- Chưa có retry, timeout, cache và kiểm soát chi phí API hoàn chỉnh.
- Hệ thống hiện hỗ trợ ảnh và PDF; chưa hỗ trợ DOCX.

