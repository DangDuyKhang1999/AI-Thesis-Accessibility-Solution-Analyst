from .models import StructuredDescription


def render_description(description: StructuredDescription) -> str:
    return description.summary.strip()
