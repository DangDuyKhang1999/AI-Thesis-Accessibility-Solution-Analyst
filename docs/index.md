# Project Documentation Index

## Tổng quan nhanh

- **Loại:** Python Streamlit monolith
- **Entry point:** `app.py`
- **Kiến trúc:** multimodal AI pipeline/service
- **Trạng thái:** MVP chức năng; evaluation nghiên cứu chưa hoàn tất
- **Cập nhật:** 2026-08-03 — narrative/voice có nhãn ngữ nghĩa, chống lặp dữ
  kiện, UI tương phản đồng bộ và 32 test tự động

## Tài liệu chính

- **[architecture.md](./architecture.md)** - Kiến trúc pipeline và invariants
- **[component-inventory.md](./component-inventory.md)** - Module, model và UI helpers
- **[development-guide.md](./development-guide.md)** - Thiết lập, chạy và kiểm thử
- **[plan.md](./plan.md)** - Việc hoàn thành và bước tiếp theo
- **[process.md](./process.md)** - Tiến độ, bằng chứng và khoảng trống
- **[project-overview.md](./project-overview.md)** - Mục tiêu và công nghệ hiện tại
- **[source-tree-analysis.md](./source-tree-analysis.md)** - Cấu trúc repository có chú thích
- **[spec.md](./spec.md)** - Đặc tả chuẩn theo yêu cầu đề tài
- **[technology-stack.md](./technology-stack.md)** - Tổng quan cách công nghệ giải quyết bài toán accessibility

## Thiết kế và implementation plans

- **[Midnight Aurora design](./superpowers/specs/2026-08-03-midnight-aurora-ui-design.md)** - Glassmorphism accessibility UI
- **[Production codebase design](./superpowers/specs/2026-08-03-production-codebase-design.md)** - Ranh giới archive và production
- **[Midnight Aurora plan](./superpowers/plans/2026-08-03-midnight-aurora-ui.md)** - Kế hoạch triển khai giao diện
- **[Production foundation plan](./superpowers/plans/2026-08-03-production-foundation.md)** - Archive và model foundation

## Nguồn tham chiếu

- **[project-request.md](./references/project-request.md)** - Yêu cầu gốc và phạm vi chính
- **[original-mvp-proposal.md](./references/original-mvp-proposal.md)** - Đề xuất MVP ban đầu
- **[mvp-happy-case-status-2026-06-07.md](./references/mvp-happy-case-status-2026-06-07.md)** - Snapshot MVP lịch sử
- **[research-paper.pdf](./references/research-paper.pdf)** - Bài báo nghiên cứu tham khảo

## Bắt đầu

Xem [development-guide.md](./development-guide.md), cấu hình `.env`, rồi chạy
`streamlit run app.py`.
