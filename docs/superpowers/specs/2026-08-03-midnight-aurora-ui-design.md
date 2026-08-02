# Midnight Aurora Glassmorphism UI Design

## Mục tiêu

Thiết kế lại presentation layer của `app.py` theo Glassmorphism chuyên nghiệp,
dễ đọc và phù hợp sản phẩm hỗ trợ accessibility. Không thay đổi analyzer,
summarizer, input adapter, pipeline hoặc TTS.

## Visual language

- Nền navy sâu với các vùng sáng cyan và emerald dạng radial gradient.
- Glass panel dùng nền trắng trong suốt nhẹ, blur vừa phải, viền sáng mảnh và
  shadow mềm; không làm mờ nội dung bên trong.
- Chữ chính gần trắng, chữ phụ xanh xám; tất cả nội dung quan trọng giữ độ
  tương phản cao.
- Cyan–emerald dùng cho CTA, focus ring, progress và trạng thái hoạt động.
- Bo góc 18–24px; spacing rộng, ít chi tiết trang trí gây nhiễu.

## Bố cục và trạng thái

- Header glass hiển thị tên sản phẩm, mô tả pipeline và trạng thái AI.
- Desktop dùng hai cột: control panel bên trái và workspace bên phải.
- Control panel chứa uploader, thông báo AI tự nhận diện ngôn ngữ nguồn,
  lựa chọn ngôn ngữ đầu ra và CTA phân tích.
- Workspace hiển thị empty state, preview hoặc kết quả tùy trạng thái.
- Kết quả mỗi trang là một glass card; summary và audio nằm trước, chi tiết
  component nằm trong accordion phía dưới.
- Component `TABLE`, `CHART`, `DIAGRAM`, `LAYOUT` dùng badge nhất quán.
- Loading, progress, warning và error dùng panel cùng visual language.
- Dưới 900px, bố cục chuyển thành một cột và giữ CTA dễ thao tác.

## Accessibility

- Không dựa riêng vào màu sắc để biểu thị trạng thái hoặc loại component.
- Focus ring rõ; button và input giữ hành vi native của Streamlit.
- Glass chỉ là lớp nền, không giảm opacity của text hoặc nội dung tương tác.
- Motion chỉ dùng transition ngắn và tắt khi hệ điều hành yêu cầu reduced motion.

## Ranh giới triển khai

- CSS được cô lập trong một module presentation để `app.py` không phình thêm.
- UI tiếp tục dùng widget Streamlit; không chèn JavaScript điều khiển nghiệp vụ.
- Dữ liệu và thứ tự pipeline hiện tại được giữ nguyên.
- Không thêm framework frontend, asset từ xa hoặc dependency UI mới.

## Kiểm thử

- App compile và toàn bộ unit test hiện tại phải đạt.
- Smoke test xác nhận title, uploader, target-language select và CTA hiển thị.
- Sau upload, preview xuất hiện; sau xử lý, summary, audio và component panel
  vẫn truy cập được.
- Kiểm tra viewport desktop và mobile để xác nhận chuyển từ hai cột sang một cột.
