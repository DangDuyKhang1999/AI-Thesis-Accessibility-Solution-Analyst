# Production Foundation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Lưu Happy Case MVP vào archive có thể chạy lại và dựng package production đầu tiên với schema mô tả accessibility có cấu trúc.

**Architecture:** MVP cũ trở thành ứng dụng tham chiếu độc lập trong `archive/happy-case-mvp/`; code production không import từ archive. Package `src/accessibility_analyst` bắt đầu bằng các model thuần dữ liệu để analyzer, translation, speech và pipeline dùng chung ở các vòng sau.

**Tech Stack:** Python 3.12, Streamlit, Pydantic 2.x, unittest, Google Gen AI SDK.

## Global Constraints

- Input phải hỗ trợ tiếng Anh, Nhật và Việt; output phải hỗ trợ tiếng Anh và Việt.
- Model phải biểu diễn bảng dữ liệu, biểu đồ, sơ đồ và layout giao diện.
- Mô tả phải giữ cấu trúc, quan hệ và điểm nổi bật, không chỉ chứa OCR tuyến tính.
- Key chỉ được đọc từ `.env` ở project root và không được đưa vào archive hoặc Git.
- Code production không được import module từ `archive/`.

---

### Task 1: Archive Happy Case MVP mà vẫn chạy được

**Files:**
- Move: `streamlit_app.py` → `archive/happy-case-mvp/streamlit_app.py`
- Move: `run_happy_case.py` → `archive/happy-case-mvp/run_happy_case.py`
- Move: `assets/samples/bar.png` → `archive/happy-case-mvp/assets/samples/bar.png`
- Move: `assets/samples/bar-2.png` → `archive/happy-case-mvp/assets/samples/bar-2.png`
- Create: `archive/happy-case-mvp/README.md`
- Modify: `tests/test_repository_hygiene.py`

**Interfaces:**
- Consumes: `.env` tại project root với `GEMINI_API_KEY` và `HF_TOKEN` tùy chọn.
- Produces: lệnh `streamlit run archive/happy-case-mvp/streamlit_app.py` và sample mặc định nằm trong archive.

- [ ] **Step 1: Viết test thất bại cho cấu trúc archive**

```python
def test_happy_case_mvp_is_archived_and_root_entrypoint_is_released(self):
    archive = ROOT / "archive" / "happy-case-mvp"
    self.assertTrue((archive / "streamlit_app.py").is_file())
    self.assertTrue((archive / "run_happy_case.py").is_file())
    self.assertTrue((archive / "README.md").is_file())
    self.assertFalse((ROOT / "streamlit_app.py").exists())
    self.assertFalse((ROOT / "run_happy_case.py").exists())
```

- [ ] **Step 2: Chạy test để xác nhận thất bại đúng lý do**

Run: `python -B -m unittest tests.test_repository_hygiene.RepositoryHygieneTests.test_happy_case_mvp_is_archived_and_root_entrypoint_is_released -v`

Expected: FAIL vì `archive/happy-case-mvp/streamlit_app.py` chưa tồn tại.

- [ ] **Step 3: Di chuyển file và sửa đường dẫn project root**

Trong cả hai Python entry point, định nghĩa root bằng vị trí cố định của archive:

```python
PROJECT_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(PROJECT_ROOT / ".env")
```

`run_happy_case.py` gọi chính xác:

```python
app_path = PROJECT_ROOT / "archive" / "happy-case-mvp" / "streamlit_app.py"
```

README ghi hai lệnh:

```powershell
streamlit run archive/happy-case-mvp/streamlit_app.py
python archive/happy-case-mvp/run_happy_case.py
```

- [ ] **Step 4: Chạy test archive và toàn bộ regression suite**

Run: `python -B -m unittest discover -s tests -v`

Expected: tất cả test PASS; test source/key quét cả file Python mới trong archive.

- [ ] **Step 5: Smoke-check import/compile**

Run: `python -B -m compileall -q archive/happy-case-mvp`

Expected: exit code `0`.

- [ ] **Step 6: Commit**

```powershell
git add -- archive/happy-case-mvp tests/test_repository_hygiene.py
git commit -m "refactor: archive completed happy case mvp"
```

### Task 2: Dựng model dữ liệu production có cấu trúc

**Files:**
- Create: `src/accessibility_analyst/__init__.py`
- Create: `src/accessibility_analyst/models.py`
- Create: `tests/test_models.py`
- Modify: `requirements.txt`

**Interfaces:**
- Consumes: dữ kiện đã được analyzer trích xuất dưới dạng Python values.
- Produces: `LanguageCode`, `ComponentType`, `VisualComponent`, `StructuredDescription` và `AccessibilityResult`.

- [ ] **Step 1: Viết test thất bại cho model và validation**

```python
from pydantic import ValidationError

from accessibility_analyst.models import (
    ComponentType,
    LanguageCode,
    StructuredDescription,
    VisualComponent,
)


class StructuredDescriptionTests(unittest.TestCase):
    def test_represents_visual_structure_and_relationships(self):
        description = StructuredDescription(
            source_language=LanguageCode.JAPANESE,
            target_language=LanguageCode.VIETNAMESE,
            summary="Doanh thu tăng qua ba quý.",
            components=[VisualComponent(
                component_type=ComponentType.CHART,
                label="Doanh thu theo quý",
                facts=["Q1: 10", "Q2: 12", "Q3: 15"],
                relationships=["Q3 cao hơn Q1 50 phần trăm"],
            )],
        )
        self.assertEqual(description.components[0].component_type, ComponentType.CHART)

    def test_rejects_empty_summary(self):
        with self.assertRaises(ValidationError):
            StructuredDescription(
                source_language=LanguageCode.ENGLISH,
                target_language=LanguageCode.VIETNAMESE,
                summary="",
                components=[],
            )
```

- [ ] **Step 2: Chạy test để xác nhận module chưa tồn tại**

Run: `$env:PYTHONPATH='src'; python -B -m unittest tests.test_models -v`

Expected: FAIL với `ModuleNotFoundError: No module named 'accessibility_analyst'`.

- [ ] **Step 3: Khai báo dependency và triển khai model tối thiểu**

Thêm `pydantic>=2.8,<3` vào `requirements.txt`. Triển khai:

```python
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field


class LanguageCode(StrEnum):
    ENGLISH = "en"
    JAPANESE = "ja"
    VIETNAMESE = "vi"


class ComponentType(StrEnum):
    TABLE = "table"
    CHART = "chart"
    DIAGRAM = "diagram"
    LAYOUT = "layout"


class VisualComponent(BaseModel):
    model_config = ConfigDict(extra="forbid")
    component_type: ComponentType
    label: str = Field(min_length=1)
    facts: list[str] = Field(default_factory=list)
    relationships: list[str] = Field(default_factory=list)


class StructuredDescription(BaseModel):
    model_config = ConfigDict(extra="forbid")
    source_language: LanguageCode
    target_language: LanguageCode
    summary: str = Field(min_length=1)
    components: list[VisualComponent] = Field(default_factory=list)


class AccessibilityResult(BaseModel):
    model_config = ConfigDict(extra="forbid", arbitrary_types_allowed=True)
    description: StructuredDescription
    rendered_text: str = Field(min_length=1)
    audio_bytes: bytes | None = None
    audio_mime_type: str | None = None
```

- [ ] **Step 4: Chạy unit test model**

Run: `$env:PYTHONPATH='src'; python -B -m unittest tests.test_models -v`

Expected: 2 test PASS.

- [ ] **Step 5: Chạy toàn bộ suite và compile package**

Run: `$env:PYTHONPATH='src'; python -B -m unittest discover -s tests -v`

Run: `python -B -m compileall -q src`

Expected: cả hai lệnh exit code `0`.

- [ ] **Step 6: Commit**

```powershell
git add -- requirements.txt src/accessibility_analyst tests/test_models.py
git commit -m "feat: add structured accessibility models"
```
