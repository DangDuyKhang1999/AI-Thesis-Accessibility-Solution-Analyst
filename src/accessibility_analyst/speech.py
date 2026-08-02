import tempfile
from pathlib import Path

from .models import LanguageCode


class SpeechService:
    def synthesize(self, text: str, language: LanguageCode) -> tuple[bytes, str]:
        from gtts import gTTS

        if not text.strip():
            raise ValueError("Không thể tạo audio từ nội dung trống.")
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp:
            path = Path(temp.name)
        try:
            gTTS(text=text, lang=language.value).save(str(path))
            return path.read_bytes(), "audio/mpeg"
        finally:
            path.unlink(missing_ok=True)
