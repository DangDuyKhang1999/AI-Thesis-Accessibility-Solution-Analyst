# Yêu cầu đề tài gốc

> **Trạng thái tài liệu:** Nguồn yêu cầu gốc được bảo tồn để truy vết; không phải
> báo cáo trạng thái hay thiết kế kỹ thuật hiện hành. Xem
> [đặc tả canonical](../spec.md) và [trạng thái hiện tại](../process.md).

Đề tài: Hệ thống AI giúp chuyển đổi tài liệu và giao diện phần mềm doanh nghiệp thành mô tả âm thanh dễ tiếp cận cho nhân viên khiếm thị.
Vấn đề: 
Trong doanh nghiệp thường có dashboard, tài liệu kỹ thuật, ERD, bảng thống kê doanh thu, biểu đồ phân tích dữ liệu,...
Các công cụ screen reader hiện nay chỉ đọc nội dung văn bản theo thứ tự tuyến tính, nhưng không mô tả được cấu trúc của dữ liệu hoặc bố cục giao diện.
Mô hình sử dụng LLM: đề xuất xây dựng hệ thống sử dụng LLM để tự động:
Phân tích nội dung tài liệu hoặc giao diện phần mềm doanh nghiệp. 
Nhận diện các thành phần thông tin như bảng dữ liệu, biểu đồ, sơ đồ hoặc layout giao diện.
Chuyển đổi các thành phần này thành mô tả ngôn ngữ tự nhiên có cấu trúc.
Chuyển mô tả văn bản thành âm thanh để hỗ trợ người khiếm thị.
Input đa ngôn ngữ (Anh – Nhật – Việt) → LLM xử lý → dịch sang ngôn ngữ (Anh – Việt)→ chuyển thành âm thanh.
