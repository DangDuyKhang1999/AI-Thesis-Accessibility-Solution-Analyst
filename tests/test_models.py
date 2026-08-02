import unittest

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
            components=[
                VisualComponent(
                    component_type=ComponentType.CHART,
                    label="Doanh thu theo quý",
                    facts=["Q1: 10", "Q2: 12", "Q3: 15"],
                    relationships=["Q3 cao hơn Q1 50 phần trăm"],
                )
            ],
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
