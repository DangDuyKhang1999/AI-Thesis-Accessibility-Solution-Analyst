# Phân tích cây nguồn

```text
app.py                         # Production Streamlit entry point
src/accessibility_analyst/     # Core pipeline, narrative/TTS và UI helpers
tests/                         # Unit và repository hygiene tests
archive/happy-case-mvp/        # MVP cũ, độc lập production
docs/                          # Canonical project documentation
docs/references/               # Yêu cầu gốc và tài liệu nghiên cứu
_bmad/                         # BMAD tooling
.agents/skills/                # Installed agent skills
```

Luồng production chỉ đi qua `app.py` và `src/accessibility_analyst/`.
`archive/happy-case-mvp/` là nơi duy nhất lưu Happy Case cũ và không phải
dependency runtime của app.

Không còn `scripts/legacy/`; các script happy-case trùng lặp đã được xóa. Luồng
đang phát triển chỉ sử dụng `app.py`, package `src/` và test trong `tests/`.
