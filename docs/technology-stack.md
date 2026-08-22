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
| Chuẩn hóa thông tin | JSON text, `json.loads`, Pydantic | Kiểm tra response parse được và khớp hình dạng/enum đã khai báo; không xác minh nội dung với ảnh |
| Diễn giải dễ nghe | Gemini text generation và heuristic hậu xử lý | Yêu cầu narrative có nhãn, rồi thay marker/nối dữ liệu chưa khớp theo chuỗi hoặc token |
| Cung cấp khả năng tiếp cận | gTTS, giao diện Streamlit | Chuyển nội dung cuối thành MP3 và cho phép đọc/nghe/đối chiếu trên cùng giao diện |

## Vì sao cần hai lượt AI

Hệ thống không yêu cầu AI nhìn ảnh rồi lập tức tạo voice. Cách đó khó kiểm soát
việc bỏ sót số liệu, lặp nội dung hoặc suy diễn sai. Thay vào đó:

- Lượt thứ nhất tập trung vào **hiểu và trích xuất**: ảnh có những thành phần nào,
  chứa dữ kiện gì và các dữ kiện quan hệ ra sao.
- Kết quả được đưa về **dữ liệu có cấu trúc** để kiểm tra tính hợp lệ.
- Lượt thứ hai tập trung vào **diễn đạt**: biến dữ liệu đã chuẩn hóa thành lời tự
  nhiên phù hợp với người nghe.

Cách tách này tạo ranh giới để **có thể** đánh giá độc lập extraction và
narrative. Repository hiện chưa có dataset/rubric thực hiện hai phép đánh giá đó.

## Vai trò của từng công nghệ chính

### Gemini multimodal

Gemini được dùng cho phần mà OCR tuyến tính không biểu diễn: suy luận về ý nghĩa
trực quan. Prompt yêu cầu mô hình xác định bảng, biểu đồ, sơ đồ, vùng giao diện;
giữ số liệu, đơn vị, xu hướng, thứ bậc, so sánh; đồng thời chọn mã nguồn Anh,
Nhật hoặc Việt. Độ đúng của các kết quả này chưa được kiểm chứng độc lập.

### JSON text và Pydantic

Prompt yêu cầu Gemini trả đúng một JSON object và SDK cấu hình MIME
`application/json`; code không truyền SDK response schema. `response.text` được
`json.loads`, sau đó Pydantic kiểm tra enum, field dư và các constraint đã khai
báo. Kết quả parse/schema lỗi làm pipeline dừng trước composition, nhưng kết quả
hợp schema vẫn có thể sai dữ kiện, thiếu component hoặc chứa list rỗng.

### Gemini text generation

Lượt AI thứ hai không xem lại ảnh. Nó nhận source/target metadata và components;
overview ban đầu của analyzer bị loại khỏi payload. Prompt yêu cầu bốn đoạn
**Tổng quan**, **Số liệu chi tiết**, **Phân tích số liệu**, **Nhận định** hoặc nhãn
Anh tương ứng. Code chưa parse để bảo đảm đủ bốn đoạn hay đúng thứ tự.

### Hậu xử lý ngôn ngữ

AI vẫn có thể tạo số thứ tự hoặc diễn đạt khác chuỗi structured data. Lớp hậu xử
lý thay marker `1–4` khớp regex và dùng substring/tập token để quyết định
fact/relationship nào cần nối thêm. Đây là fallback best-effort; nó không xác
minh tương đương ngữ nghĩa, factual completeness hoặc việc narrative không lặp.

### gTTS

gTTS chuyển bản mô tả cuối cùng sang MP3 tiếng Việt hoặc tiếng Anh. Văn bản trên
màn hình và văn bản dùng để tạo voice là cùng một nội dung, giúp người dùng và
người đánh giá có thể đối chiếu.

### Streamlit và thiết kế giao diện

Streamlit cung cấp ba vùng desktop: controls, analysis và document inspector;
dưới 900px CSS xếp chúng thành một cột. CSS có rule tương phản, `focus-visible`
và `prefers-reduced-motion`; unit test chỉ kiểm tra source contract của các rule,
không phải browser rendering, WCAG, keyboard hay screen-reader audit.

## Luồng công nghệ tổng quát

```text
Ảnh hoặc PDF
  → chuẩn hóa từng trang
  → AI hiểu nội dung trực quan
  → JSON parse được và Pydantic shape validation
  → AI diễn giải thành lời tự nhiên
  → marker/coverage heuristic
  → văn bản dễ nghe
  → âm thanh MP3
```

## Giá trị của cách tiếp cận

- Không dừng ở OCR mà truyền đạt cả cấu trúc và quan hệ của dữ liệu.
- Tách extraction và narrative thành hai giai đoạn có thể thiết kế đánh giá riêng.
- Hỗ trợ đầu vào Anh–Nhật–Việt và đầu ra Anh–Việt.
- Giữ văn bản và voice nhất quán để thuận tiện kiểm chứng.
- Service boundaries cho phép thay provider, nhưng chưa có interface/contract test
  đầy đủ cho mọi provider thay thế.

## Giới hạn hiện tại

- Gemini và gTTS cần kết nối Internet.
- Chất lượng phụ thuộc vào model/ảnh; schema validation không phát hiện factual error.
- Chưa có bộ dữ liệu đánh giá chính thức, ngưỡng độ chính xác hoặc nghiên cứu với
  người dùng khiếm thị.
- Chưa có retry, timeout, cache, giới hạn upload/page hoặc kiểm soát chi phí API.
- Hệ thống hiện hỗ trợ ảnh và PDF; chưa hỗ trợ DOCX.
- PDF được xử lý tuần tự theo trang nhưng inspector chỉ preview trang đầu; chưa có
  tổng hợp cấp tài liệu.
