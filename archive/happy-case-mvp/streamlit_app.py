import base64
import os
import tempfile
from pathlib import Path

import streamlit.components.v1 as components
import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import types

PROJECT_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(PROJECT_ROOT / ".env")
st.set_page_config(page_title="Happy Case MVP", page_icon="🎧", layout="wide")
st.markdown(
        """
        <style>
            header, [data-testid="stToolbar"], [data-testid="stDecoration"], #MainMenu, footer {
                visibility: hidden !important;
                display: none !important;
            }
            .block-container {
                padding-top: 0.35rem;
                padding-bottom: 1.0rem;
            }
            .hero-wrap {
                display: flex;
                align-items: flex-start;
                gap: 0.75rem;
                margin: 0 0 0.2rem 0;
            }
            .hero-accent {
                width: 6px;
                height: 2.45rem;
                border-radius: 999px;
                background: linear-gradient(180deg, #4f8cff 0%, #6ee7b7 100%);
                flex: 0 0 auto;
                margin-top: 0.18rem;
            }
            .hero-title {
                font-size: 2.05rem;
                font-weight: 800;
                line-height: 1.1;
                margin: 0;
                padding: 0;
                color: rgba(255, 255, 255, 0.98);
            }
            .hero-subtitle {
                font-size: 1rem;
                color: rgba(255, 255, 255, 0.72);
                margin: 0.25rem 0 0 0;
                padding: 0;
            }
            .mini-pill {
                display: inline-flex;
                align-items: center;
                gap: 0.4rem;
                margin-top: 0.55rem;
                padding: 0.35rem 0.65rem;
                border-radius: 999px;
                background: rgba(255, 255, 255, 0.06);
                border: 1px solid rgba(255, 255, 255, 0.08);
                color: rgba(255, 255, 255, 0.78);
                font-size: 0.82rem;
            }
            .field-label {
                font-size: 0.95rem;
                font-weight: 700;
                margin: 0 0 0.35rem 0;
                color: rgba(255, 255, 255, 0.9);
            }
            div[data-testid="stFileUploader"] {
                padding-top: 0 !important;
                margin-top: 0 !important;
            }
            div[data-testid="stFileUploaderDropzone"] {
                min-height: 4.25rem !important;
                padding: 0.4rem 0.6rem !important;
                border-radius: 14px !important;
            }
            div[data-testid="stFileUploaderDropzone"] button {
                min-height: 3.25rem !important;
                height: 3.25rem !important;
            }
            div[data-testid="stButton"] button {
                min-height: 4.25rem !important;
                height: 4.25rem !important;
                padding-top: 0 !important;
                padding-bottom: 0 !important;
            }
            .preview-frame {
                width: 100%;
                height: clamp(280px, 52vh, 430px);
                max-height: 430px;
                border: 1px solid rgba(49, 51, 63, 0.2);
                border-radius: 14px;
                overflow: hidden;
                background: #111;
                display: flex;
                align-items: center;
                justify-content: center;
            }
            .preview-frame img {
                max-width: 100%;
                max-height: 100%;
                width: auto;
                height: auto;
                object-fit: contain;
                display: block;
            }
        </style>
        """,
        unsafe_allow_html=True,
)


def build_prompt() -> str:
    return (
        "Ban la tro ly AI ho tro kha nang tiep can cho nguoi khiem thi trong doanh nghiep.\n"
        "Nhiem vu: Phan tich 1 hinh anh giao dien hoac tai lieu va mo ta BANG TIENG VIET, chi duoc viet van ban thuong, ro rang, de doc.\n\n"
        "Yeu cau xuat:\n"
        "- Hay viet thanh 1 doan van lien tuc, khong danh dau dau dong, khong bullet, khong numbering, khong markdown.\n"
        "- Khong dung ky tu dac biet nhu *, #, -, >, `, [ ], ( ), : o dau dong.\n"
        "- Khong them tieu de. Khong in ky hieu trang tri.\n\n"
        "Rang buoc:\n"
        "- Chi viet tieng Viet.\n"
        "- Khong suy doan vo can cu.\n"
        "- Neu khong doc duoc mot vung, ghi ro: 'Khong doc ro'.\n"
        "- Van phong gon, de nghe qua TTS.\n"
        "- Dau ra phai la van ban thuong, khong co ky tu lam TTS doc ten ky hieu."
    )


def _guess_mime_type(ext: str) -> str:
    if ext == ".png":
        return "image/png"
    if ext in {".jpg", ".jpeg"}:
        return "image/jpeg"
    if ext == ".webp":
        return "image/webp"
    return "application/octet-stream"


def _clean_plain_text(text: str) -> str:
    lines = []
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        while line.startswith(("- ", "* ", "> ", "# ")):
            line = line[2:].lstrip()
        if len(line) > 2 and line[0].isdigit() and line[1] in {".", ")"}:
            line = line[2:].lstrip()
        lines.append(line)

    cleaned = " ".join(lines)
    for ch in ("*", "#", "`", "[", "]"):
        cleaned = cleaned.replace(ch, "")
    while "  " in cleaned:
        cleaned = cleaned.replace("  ", " ")
    return cleaned.strip()


def _extract_audio_bytes_from_hf_response(response) -> bytes | None:
    ctype = response.headers.get("content-type", "")
    if "audio" in ctype or ctype in ("application/octet-stream",):
        return response.content

    try:
        payload = response.json()
    except Exception:
        return None

    def _try_extract(obj):
        if isinstance(obj, dict):
            for key in ("audio", "data", "mp3", "wav", "sound"):
                value = obj.get(key)
                if isinstance(value, str):
                    if value.startswith("data:") and ";base64," in value:
                        return base64.b64decode(value.split(";base64,", 1)[1])
                    try:
                        return base64.b64decode(value)
                    except Exception:
                        pass
            for value in obj.values():
                nested = _try_extract(value)
                if nested:
                    return nested
        if isinstance(obj, list):
            for item in obj:
                nested = _try_extract(item)
                if nested:
                    return nested
        return None

    return _try_extract(payload)


def generate_vietnamese_text(image_bytes: bytes, mime_type: str, api_key: str, model_name: str) -> str:
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model=model_name,
        contents=[
            build_prompt(),
            types.Part.from_bytes(data=image_bytes, mime_type=mime_type),
        ],
    )
    text = (response.text or "").strip()
    cleaned = _clean_plain_text(text)
    return _normalize_numbers_to_vn(cleaned)


def _normalize_numbers_to_vn(text: str) -> str:
    import re

    def _replace(match: re.Match) -> str:
        s = match.group(0)
        s_clean = s.replace(" ", "").replace(",", "")
        try:
            if "." in s_clean:
                val = float(s_clean)
            else:
                val = int(s_clean)
        except Exception:
            return s

        unit = None
        scaled = None
        if val >= 1_000_000_000:
            scaled = val / 1_000_000_000
            unit = "tỷ"
        elif val >= 1_000_000:
            scaled = val / 1_000_000
            unit = "triệu"
        elif val >= 1_000:
            scaled = val / 1_000
            unit = "nghìn"

        if unit is None:
            return s

        if abs(scaled - round(scaled)) < 1e-9:
            out = f"{int(round(scaled))} {unit}"
        else:
            out = f"{scaled:.1f} {unit}"
            out = out.replace(".0 ", " ")
        return out

    pattern = re.compile(r"(?<!\d)(\d{1,3}(?:[., ]\d{3})*(?:[.,]\d+)?)(?!\d)")
    return pattern.sub(_replace, text)


def build_audio_bytes(text: str, hf_token: str) -> tuple[bytes, str]:
    import requests

    hf_url = "https://api-inference.huggingface.co/models/suno/bark"
    headers = {"Authorization": f"Bearer {hf_token}"}
    try:
        response = requests.post(hf_url, headers=headers, json={"inputs": text}, timeout=120, stream=True)
        if response.status_code == 200:
            audio_bytes = _extract_audio_bytes_from_hf_response(response)
            if audio_bytes:
                return audio_bytes, "audio/mpeg"
    except Exception:
        # Network/DNS issues should not surface to the UI because the app has local fallbacks.
        pass

    try:
        import pyttsx3

        engine = pyttsx3.init()
        voices = engine.getProperty("voices") or []
        vi_voice = None
        for voice in voices:
            blob = " ".join(str(getattr(voice, attr, "")) for attr in ("id", "name", "languages")).lower()
            if "vietnam" in blob or "vietnamese" in blob or " vi" in blob or "vi-" in blob:
                vi_voice = voice
                break

        if vi_voice is not None:
            engine.setProperty("voice", vi_voice.id)
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
                temp_path = Path(temp_file.name)
            engine.save_to_file(text, str(temp_path))
            engine.runAndWait()
            audio_bytes = temp_path.read_bytes()
            temp_path.unlink(missing_ok=True)
            return audio_bytes, "audio/wav"
    except Exception:
        pass

    from gtts import gTTS

    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
        temp_path = Path(temp_file.name)
    gTTS(text=text, lang="vi").save(str(temp_path))
    audio_bytes = temp_path.read_bytes()
    temp_path.unlink(missing_ok=True)
    return audio_bytes, "audio/mpeg"


def render_autoplay_audio(audio_bytes: bytes, audio_mime: str) -> None:
    encoded = base64.b64encode(audio_bytes).decode("utf-8")
    html = f"""
    <audio controls autoplay style="width: 100%;" onloadedmetadata="this.play().catch(() => {{}})">
        <source src="data:{audio_mime};base64,{encoded}" type="{audio_mime}">
        Trinh duyet cua ban khong ho tro audio.
    </audio>
    """
    components.html(html, height=90)


def render_large_image(image_bytes: bytes) -> None:
    st.image(image_bytes, use_container_width=True)


st.markdown(
    """
    <div class="hero-wrap">
        <div class="hero-accent"></div>
        <div>
            <div class="hero-title">Happy Case MVP</div>
            <div class="hero-subtitle">Upload ảnh, nhận mô tả tiếng Việt và nghe audio ngay trên web.</div>
            <div class="mini-pill">Model: gemini-2.5-flash-lite</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

upload_col, action_col = st.columns([4.9, 1.6], vertical_alignment="bottom")

with upload_col:
    st.markdown("<div class='field-label'>Chọn một ảnh</div>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("", type=["png", "jpg", "jpeg", "webp"], label_visibility="collapsed")

with action_col:
    generate_clicked = st.button("Sinh audio", type="primary", use_container_width=True)

model_name = "gemini-2.5-flash-lite"

if uploaded_file:
    image_bytes = uploaded_file.read()
    preview_col, result_col = st.columns([4.9, 1.6], vertical_alignment="top")

    with preview_col:
        render_large_image(image_bytes)

    if generate_clicked:
        api_key = os.getenv("GEMINI_API_KEY", "").strip()
        hf_token = os.getenv("HF_TOKEN", "").strip()

        if not api_key:
            st.error("Thiếu GEMINI_API_KEY.")
        else:
            with st.spinner("Đang phân tích ảnh và tạo âm thanh..."):
                try:
                    text = generate_vietnamese_text(
                        image_bytes=image_bytes,
                        mime_type=_guess_mime_type(Path(uploaded_file.name).suffix.lower()),
                        api_key=api_key,
                        model_name=model_name,
                    )
                    with result_col:
                        st.markdown("<div class='field-label'>Nội dung đã sinh</div>", unsafe_allow_html=True)
                        st.text_area("Văn bản thuần", value=text, height=360, label_visibility="visible")

                        audio_bytes, audio_mime = build_audio_bytes(text=text, hf_token=hf_token)
                        st.markdown("<div class='field-label'>Nghe trực tiếp</div>", unsafe_allow_html=True)
                        render_autoplay_audio(audio_bytes, audio_mime)
                except Exception as exc:
                    st.error(f"Xử lý thất bại: {exc}")
else:
    st.info("Hãy tải một ảnh lên để bắt đầu.")
