# Mục lục tài liệu dự án

`docs/process.md` là nguồn duy nhất cho trạng thái triển khai và mức độ kiểm
chứng hiện tại. `docs/spec.md` giữ contract ổn định; `docs/plan.md` giữ backlog.
Các file trong `superpowers/` và một số file trong `references/` là artifact lịch
sử, không phải trạng thái hiện hành.

## Tài liệu canonical

- **[architecture.md](./architecture.md)** — data flow và ranh giới module hiện tại.
- **[component-inventory.md](./component-inventory.md)** — lớp, hàm và schema đang có.
- **[development-guide.md](./development-guide.md)** — setup, validation gate và smoke test thủ công.
- **[plan.md](./plan.md)** — contract đã triển khai, validation còn thiếu và backlog.
- **[process.md](./process.md)** — trạng thái duy nhất, bằng chứng và giới hạn.
- **[project-overview.md](./project-overview.md)** — mục tiêu, phạm vi và stack hiện tại.
- **[source-tree-analysis.md](./source-tree-analysis.md)** — các vùng runtime, tài liệu và artifact local.
- **[spec.md](./spec.md)** — contract sản phẩm suy ra từ yêu cầu gốc.
- **[technology-stack.md](./technology-stack.md)** — vai trò và giới hạn của từng công nghệ.

## Artifact triển khai lịch sử

- **[Midnight Aurora design](./superpowers/specs/2026-08-03-midnight-aurora-ui-design.md)** — thiết kế hai vùng cũ, đã được UI ba vùng thay thế.
- **[Production codebase design](./superpowers/specs/2026-08-03-production-codebase-design.md)** — thiết kế foundation đã hoàn tất và được kiến trúc hiện tại thay thế.
- **[Midnight Aurora plan](./superpowers/plans/2026-08-03-midnight-aurora-ui.md)** — kế hoạch đã đóng/superseded; core UI có code nhưng bước browser smoke chưa có bằng chứng tái chạy.
- **[Production foundation plan](./superpowers/plans/2026-08-03-production-foundation.md)** — kế hoạch archive/model foundation đã hoàn tất.

## Nguồn và tài liệu nghiên cứu

- **[project-request.md](./references/project-request.md)** — yêu cầu gốc được bảo tồn.
- **[original-mvp-proposal.md](./references/original-mvp-proposal.md)** — đề xuất kỹ thuật ban đầu, không phải stack hiện tại.
- **[mvp-happy-case-status-2026-06-07.md](./references/mvp-happy-case-status-2026-06-07.md)** — snapshot Happy Case ngày 07/06/2026.
- **[research-paper.pdf](./references/research-paper.pdf)** — bản PDF bài báo tham khảo năm 2013.
- **[research-paper-mapping.md](./references/research-paper-mapping.md)** — citation, capability mapping và giới hạn suy rộng.

Mỗi file con của `docs/` phải xuất hiện đúng một lần trong mục lục này; test
repository hygiene kiểm tra inventory, target và anchor tương đối.
