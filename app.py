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

controls, content, inspector = st.columns([0.82, 1.75, 0.93], gap="medium")
with controls:
    with st.container(border=True, key="control_rail"):
        st.markdown('<div class="aurora-eyebrow">01 · Tài liệu đầu vào</div>', unsafe_allow_html=True)
        st.subheader("Tải nội dung cần phân tích")
        uploaded = st.file_uploader("Ảnh hoặc PDF", type=["png", "jpg", "jpeg", "webp", "pdf"])
        render_status("AI tự nhận diện tiếng Anh, Nhật hoặc Việt từ nội dung.")
        target_label = st.selectbox("Ngôn ngữ mô tả và audio", list(output_labels))
        analyze_clicked = st.button("Phân tích tài liệu", type="primary", use_container_width=True)

document = None
input_error = None
if uploaded:
    mime_type = uploaded.type or "application/octet-stream"
    try:
        document = InputAdapter().from_bytes(uploaded.getvalue(), uploaded.name, mime_type)
    except UnsupportedInputError as exc:
        input_error = str(exc)

with content:
    with st.container(border=True, key="analysis_workspace"):
        st.markdown('<div class="aurora-eyebrow">02 · Kết quả phân tích</div>', unsafe_allow_html=True)
        if input_error:
            st.error(input_error)
        elif not document:
            st.subheader("Sẵn sàng phân tích tài liệu")
            render_status("Tải ảnh hoặc PDF ở bảng điều khiển. Audio và mô tả sẽ xuất hiện tại đây, không nằm sau preview.")
            st.info("Hỗ trợ PNG, JPEG, WebP và PDF nhiều trang.")
        elif not analyze_clicked:
            st.subheader(f"{uploaded.name} đã sẵn sàng")
            render_status(f"Đã nhận {len(document.pages)} trang. Chọn ngôn ngữ và bắt đầu phân tích.")
        else:
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
                    results.append(
                        pipeline.run(page.data, page.mime_type, None, output_labels[target_label])
                    )
                    progress.progress(
                        index / len(document.pages),
                        text=f"Đã xử lý trang {index}/{len(document.pages)}",
                    )
            except Exception as exc:
                st.error(f"Xử lý thất bại: {exc}")
                st.stop()
            progress.empty()
            for page_number, result in enumerate(results, start=1):
                with st.container(border=True):
                    st.markdown(
                        f'<div class="aurora-eyebrow">Trang {page_number} · Nghe mô tả</div>',
                        unsafe_allow_html=True,
                    )
                    st.audio(result.audio_bytes, format=result.audio_mime_type)
                    st.subheader("Mô tả chi tiết")
                    st.write(result.rendered_text)
                    badges = "".join(
                        f'<span class="aurora-badge">{component.component_type.value.upper()}</span>'
                        for component in result.description.components
                    )
                    st.markdown(badges, unsafe_allow_html=True)
                    with st.expander("Cấu trúc được nhận diện", expanded=False):
                        for component in result.description.components:
                            st.markdown(
                                f"**{component.component_type.value.upper()} · {component.label}**"
                            )
                            for fact in component.facts:
                                st.write(f"• {fact}")
                            for relationship in component.relationships:
                                st.write(f"↳ {relationship}")

with inspector:
    with st.container(border=True, key="document_inspector"):
        st.markdown('<div class="aurora-eyebrow">03 · Ảnh tham chiếu</div>', unsafe_allow_html=True)
        if document:
            st.subheader(f"Toàn cảnh · {len(document.pages)} trang")
            with st.container(key="document_stage"):
                st.image(document.pages[0].data, use_container_width=True)
            with st.popover("Mở ảnh lớn", use_container_width=True):
                st.caption(f"{uploaded.name} · Trang 1/{len(document.pages)}")
                st.image(document.pages[0].data, use_container_width=True)
        elif input_error:
            st.error(input_error)
        else:
            st.subheader("Nguồn trực quan")
            render_status("Ảnh hoặc trang PDF sẽ được thu vừa toàn cảnh tại đây.")
            st.info("Preview không làm tăng chiều dài workspace.")
