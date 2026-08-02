import os
import sys
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))
load_dotenv(ROOT / ".env")

from accessibility_analyst.analyzer import GeminiAnalyzerClient, VisualAnalyzer
from accessibility_analyst.input_adapter import InputAdapter, UnsupportedInputError
from accessibility_analyst.models import LanguageCode
from accessibility_analyst.pipeline import AccessibilityPipeline
from accessibility_analyst.speech import SpeechService
from accessibility_analyst.summarizer import GeminiSummarizer
from accessibility_analyst.ui import apply_midnight_aurora, render_header, render_status

st.set_page_config(page_title="Accessibility Solution Analyst", page_icon="🎧", layout="wide")
apply_midnight_aurora()
render_header()

output_labels = {"Tiếng Việt": LanguageCode.VIETNAMESE, "English": LanguageCode.ENGLISH}

controls, content = st.columns([1, 2])
with controls:
    with st.container(border=True):
        st.markdown('<div class="aurora-eyebrow">01 · Tài liệu đầu vào</div>', unsafe_allow_html=True)
        st.subheader("Tải nội dung cần phân tích")
        uploaded = st.file_uploader("Ảnh hoặc PDF", type=["png", "jpg", "jpeg", "webp", "pdf"])
        render_status("AI tự nhận diện tiếng Anh, Nhật hoặc Việt từ nội dung.")
        target_label = st.selectbox("Ngôn ngữ mô tả và audio", list(output_labels))
        analyze_clicked = st.button("Phân tích tài liệu", type="primary", use_container_width=True)

if uploaded:
    mime_type = uploaded.type or "application/octet-stream"
    try:
        document = InputAdapter().from_bytes(uploaded.getvalue(), uploaded.name, mime_type)
    except UnsupportedInputError as exc:
        st.error(str(exc))
        st.stop()

    with content:
        with st.container(border=True):
            st.markdown('<div class="aurora-eyebrow">02 · Workspace</div>', unsafe_allow_html=True)
            st.subheader(f"Xem trước · {len(document.pages)} trang")
            st.image(document.pages[0].data, use_container_width=True)

    if analyze_clicked:
        api_key = os.getenv("GEMINI_API_KEY", "").strip()
        if not api_key:
            st.error("Thiếu GEMINI_API_KEY trong file .env.")
            st.stop()
        pipeline = AccessibilityPipeline(
            VisualAnalyzer(GeminiAnalyzerClient(api_key)),
            GeminiSummarizer(api_key),
            SpeechService(),
        )
        results = []
        progress = st.progress(0, text="Đang phân tích tài liệu...")
        try:
            for index, page in enumerate(document.pages, start=1):
                results.append(pipeline.run(
                    page.data, page.mime_type,
                    None, output_labels[target_label],
                ))
                progress.progress(index / len(document.pages), text=f"Đã xử lý trang {index}/{len(document.pages)}")
        except Exception as exc:
            st.error(f"Xử lý thất bại: {exc}")
            st.stop()
        progress.empty()
        for page_number, result in enumerate(results, start=1):
            with st.container(border=True):
                st.markdown(f'<div class="aurora-eyebrow">03 · Kết quả trang {page_number}</div>', unsafe_allow_html=True)
                st.subheader("Mô tả chi tiết để nghe")
                st.write(result.rendered_text)
                badges = "".join(
                    f'<span class="aurora-badge">{component.component_type.value.upper()}</span>'
                    for component in result.description.components
                )
                st.markdown(badges, unsafe_allow_html=True)
                st.audio(result.audio_bytes, format=result.audio_mime_type)
                with st.expander("Cấu trúc được nhận diện", expanded=False):
                    for component in result.description.components:
                        st.markdown(f"**{component.component_type.value.upper()} · {component.label}**")
                        for fact in component.facts:
                            st.write(f"• {fact}")
                        for relationship in component.relationships:
                            st.write(f"↳ {relationship}")
else:
    with content:
        with st.container(border=True):
            st.markdown('<div class="aurora-eyebrow">02 · Workspace</div>', unsafe_allow_html=True)
            st.subheader("Nội dung trực quan sẽ xuất hiện tại đây")
            render_status("Tải ảnh hoặc PDF để xem trước, phân tích cấu trúc và tạo mô tả audio dễ tiếp cận.")
            st.info("Hỗ trợ PNG, JPEG, WebP và PDF nhiều trang.")
