# Midnight Aurora UI Implementation Plan

> **Trạng thái tài liệu:** Artifact lịch sử — kế hoạch đã đóng và được workflow
> hiện tại thay thế. Core UI có implementation, nhưng bước browser smoke bên dưới
> chưa có artifact tái chạy trong repo và không được xem là đã hoàn tất. Checkbox
> được giữ nguyên như bản kế hoạch gốc. Xem
> [backlog hiện hành](../../plan.md) và [trạng thái hiện tại](../../process.md).

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Thay toàn bộ presentation layer của app Streamlit bằng giao diện Midnight Aurora Glassmorphism responsive và dễ tiếp cận.

**Architecture:** CSS và markup presentation nằm trong `src/accessibility_analyst/ui.py`; `app.py` chỉ gọi helper và giữ workflow hiện tại. Không thay đổi input adapter, analyzer, summarizer, pipeline hoặc speech.

**Tech Stack:** Python 3.12, Streamlit, CSS3, unittest, Playwright smoke test.

## Global Constraints

- Không thêm frontend framework, JavaScript nghiệp vụ hoặc asset từ xa.
- Text quan trọng không dùng opacity; focus ring phải nhìn rõ.
- Desktop hai cột, viewport dưới 900px một cột.
- Giữ nguyên toàn bộ chức năng ảnh/PDF, auto-detect input, output Anh/Việt, summary, component và audio.

---

### Task 1: Midnight Aurora presentation layer

**Files:**
- Create: `src/accessibility_analyst/ui.py`
- Create: `tests/test_ui.py`
- Modify: `app.py`

**Interfaces:**
- Produces: `apply_midnight_aurora() -> None`, `render_header() -> None`, `render_status(message: str) -> None`.
- Consumes: Streamlit widgets và kết quả pipeline hiện có; không đổi signature nghiệp vụ.

- [ ] **Step 1: Viết failing tests cho CSS contract**

```python
from accessibility_analyst.ui import midnight_aurora_css

css = midnight_aurora_css()
self.assertIn("backdrop-filter: blur", css)
self.assertIn("@media (max-width: 900px)", css)
self.assertIn(":focus-visible", css)
self.assertIn("prefers-reduced-motion", css)
```

- [ ] **Step 2: Chạy RED**

Run: `$env:PYTHONPATH='src'; python -B -m unittest tests.test_ui -v`

Expected: FAIL vì `accessibility_analyst.ui` chưa tồn tại.

- [ ] **Step 3: Triển khai CSS và helper markup**

`midnight_aurora_css()` trả CSS navy/cyan/emerald, glass panels, widget overrides,
badge, responsive breakpoint, focus và reduced motion. `apply_midnight_aurora()`
inject CSS bằng `st.markdown`; `render_header()` tạo hero/status có semantic copy.

- [ ] **Step 4: Tích hợp vào app**

Gọi helper ngay sau `set_page_config`; bọc control/workspace/result bằng marker
classes và thêm badge component, summary card, audio card, empty/error/loading state.

- [ ] **Step 5: Chạy GREEN và regression**

Run: `$env:PYTHONPATH='src'; python -B -m unittest discover -s tests -v`

Run: `python -B -m compileall -q app.py src`

Expected: toàn bộ test PASS và compile exit `0`.

- [ ] **Step 6: Smoke test desktop/mobile**

Playwright xác nhận title, uploader, một combobox output, CTA tại viewport
1440×1000 và 390×844; computed style của app có nền tối và glass blur.
