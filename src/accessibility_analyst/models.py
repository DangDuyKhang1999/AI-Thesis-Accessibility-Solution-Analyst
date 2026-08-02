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


class InputPage(BaseModel):
    model_config = ConfigDict(extra="forbid")
    index: int = Field(ge=1)
    data: bytes
    mime_type: str


class InputDocument(BaseModel):
    model_config = ConfigDict(extra="forbid")
    source_name: str = Field(min_length=1)
    pages: list[InputPage] = Field(min_length=1)
