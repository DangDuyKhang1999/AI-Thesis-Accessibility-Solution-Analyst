from pathlib import Path

from .models import InputDocument, InputPage


class UnsupportedInputError(ValueError):
    pass


class InputAdapter:
    IMAGE_TYPES = {"image/png", "image/jpeg", "image/webp"}

    def from_bytes(self, data: bytes, source_name: str, mime_type: str) -> InputDocument:
        if not data:
            raise UnsupportedInputError("Tệp đầu vào trống.")
        if mime_type in self.IMAGE_TYPES:
            return InputDocument(
                source_name=source_name,
                pages=[InputPage(index=1, data=data, mime_type=mime_type)],
            )
        if mime_type == "application/pdf" or Path(source_name).suffix.lower() == ".pdf":
            return self._from_pdf(data, source_name)
        raise UnsupportedInputError("Chỉ hỗ trợ PNG, JPEG, WebP và PDF.")

    def _from_pdf(self, data: bytes, source_name: str) -> InputDocument:
        import fitz

        try:
            pdf = fitz.open(stream=data, filetype="pdf")
        except Exception as exc:
            raise UnsupportedInputError("Không thể đọc tệp PDF.") from exc
        pages = []
        try:
            for index, page in enumerate(pdf, start=1):
                pixmap = page.get_pixmap(matrix=fitz.Matrix(1.5, 1.5), alpha=False)
                pages.append(InputPage(index=index, data=pixmap.tobytes("png"), mime_type="image/png"))
        finally:
            pdf.close()
        if not pages:
            raise UnsupportedInputError("PDF không có trang nào.")
        return InputDocument(source_name=source_name, pages=pages)
