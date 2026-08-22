# Các vùng chính của repository

```text
README.md                      # Entry point cho người phát triển
app.py                         # Streamlit workflow production
src/accessibility_analyst/     # Adapter, schema, AI/TTS, pipeline và UI
tests/                         # Unit/repository contract tests
archive/happy-case-mvp/        # Snapshot app cũ, không phải runtime dependency
docs/                          # Tài liệu canonical và mục lục được guard
  references/                  # Nguồn gốc, proposal/snapshot lịch sử, paper
  superpowers/                 # Design/plan triển khai lịch sử có banner
_bmad/                         # BMAD tooling/config dùng trong repo
.agents/skills/                # Installed agent skills
_bmad-output/                  # Artifact làm việc local, bị Git ignore
```

Đây là bản đồ các vùng có ý nghĩa, không phải listing mọi file/cache. Luồng
runtime production chỉ đi qua `app.py` và `src/accessibility_analyst/`;
repository test kiểm tra source này không import `archive`.

Trong `docs/`, [process.md](process.md) là status SSOT; spec/architecture/plan có
vai trò riêng. `_bmad-output/` chứa spec và review artifact đang làm việc, không
được index như tài liệu canonical và có thể không tồn tại ở clone khác vì bị
ignore. Cache, virtual environment, `.env`, runtime logs và trạng thái công cụ
local cũng không thuộc source tree được version control.

Happy Case có entry point và README riêng dưới `archive/happy-case-mvp/`. Những
đường dẫn root/`happy_case_vn` trong snapshot ngày 07/06 chỉ là lịch sử và không
phải lệnh chạy hiện tại.

Root `requirements.txt` và `.env.example` hiện vẫn dùng chung cho cả production
và archive: `requests`, `pyttsx3` và `HF_TOKEN` chỉ phục vụ Happy Case cũ. Vì
chưa tách dependency/config archive, cài đặt canonical vẫn kéo theo các mục
legacy này dù `app.py` và package `src/` không sử dụng chúng.
