# Mapping bài báo nghiên cứu tham khảo

> **Trạng thái tài liệu:** Companion nghiên cứu hiện hành. File này giải thích
> paper hỗ trợ phần nào của [đặc tả](../spec.md) và phần nào dự án tự mở rộng;
> không biến kết quả của paper thành bằng chứng cho implementation hiện tại.

## Citation

Azadeh Nazemi và Iain Murray, “A Method to Provide Accessibility for Visual
Components to Vision Impaired,” *International Journal of Human Computer
Interaction (IJHCI)*, volume 4, issue 1, 2013, trang 54–69.

Nguồn local: [research-paper.pdf](research-paper.pdf).

## Phạm vi và phương pháp của paper

- Paper tập trung bar chart, pie chart, line chart và function graph.
- GraphicReader dùng OCR/image processing, biểu diễn trung gian XML, sinh textual
  summary rồi chuyển qua text-to-speech.
- Phương pháp kết hợp **passive description** (mô tả toàn bộ/overview) với
  **active exploration** (người dùng điều hướng từng trường dữ liệu) để giảm tải
  trí nhớ và xây mental model.
- Paper nhấn mạnh text equivalent có thứ bậc để truyền cấu trúc của graphic.
- Kết luận thừa nhận Visual Extraction Module giả định chart đơn giản tạo bằng
  GNUPLOT với vị trí title/axis/tick/label theo format đó; cần nghiên cứu thêm cho
  layout và digital format khác.

## Mapping sang capability

| Capability | Paper hỗ trợ ở mức khái niệm | Không được suy ra |
| --- | --- | --- |
| CAP-2/CAP-3: hiểu và nhận diện cấu trúc | Cần trích xuất label, value, axis, trend và quan hệ thay vì chỉ OCR tuyến tính | Paper không chứng minh Gemini nhận diện đúng table, diagram, enterprise UI hoặc layout tự do |
| CAP-4: mô tả có cấu trúc | Text summary, hierarchy và overview + detail giúp truyền message/mental model | Không chứng minh bốn nhãn narrative hiện tại là tối ưu hoặc heuristic coverage là đúng |
| CAP-6: audio | Textual equivalent có thể được truyền bằng synthesized speech | Không đánh giá gTTS, tiếng Việt/Anh hiện tại hoặc listening clarity của dự án |
| Active exploration | Người dùng nên có khả năng chọn phần chart cần khám phá | App hiện chỉ cung cấp narrative thụ động và expander chi tiết, chưa có field-level navigation có hướng dẫn |

CAP-1 về định dạng input và CAP-5 về Anh/Nhật/Việt → Anh/Việt là phạm vi dự án,
không được paper này chứng minh.

## Giới hạn bằng chứng

Paper báo cáo accuracy khoảng 98% cho line chart và 98,7% cho pie chart trong
thiết lập của tác giả. Không được chuyển các con số đó sang dự án vì khác dữ liệu,
thuật toán, model, chart format và protocol đánh giá. Repo hiện chưa có dataset
hoặc phép tái lập paper.

Paper cũng không chứng minh:

- factual accuracy hoặc structural coverage của `gemini-2.5-flash-lite`;
- parsing bảng, sơ đồ, ERD, screenshot phần mềm hoặc PDF doanh nghiệp đa dạng;
- translation Anh/Nhật/Việt, TTS song ngữ hoặc accessibility conformance;
- user study cho UI Streamlit hiện tại.

Vì vậy paper là cơ sở định hướng cho structured description + audio và nhu cầu
active exploration, không phải acceptance evidence. Trạng thái validation của
dự án nằm tại [process.md](../process.md) và backlog tại [plan.md](../plan.md).
