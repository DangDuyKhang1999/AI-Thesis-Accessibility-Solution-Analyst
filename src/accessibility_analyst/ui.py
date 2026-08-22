import streamlit as st


def midnight_aurora_css() -> str:
    return """
    <style>
    :root {
        --midnight: #06111f;
        --glass: rgba(8, 25, 42, 0.88);
        --glass-strong: rgba(12, 35, 57, 0.94);
        --border: rgba(184, 235, 250, 0.34);
        --cyan: #67e8f9;
        --emerald: #5eead4;
        --text: #f4fbff;
        --muted: #d9e9f2;
        --on-bright: #02131b;
    }
    .stApp {
        color: var(--text);
        background:
            radial-gradient(circle at 12% 8%, rgba(26, 101, 145, .52), transparent 31%),
            radial-gradient(circle at 88% 12%, rgba(40, 61, 145, .42), transparent 30%),
            radial-gradient(circle at 58% 92%, rgba(9, 105, 92, .35), transparent 34%),
            var(--midnight);
        background-attachment: fixed;
    }
    [data-testid="stHeader"] { background: transparent; }
    [data-testid="stToolbar"], #MainMenu, footer { visibility: hidden; }
    .block-container { max-width: 1440px; padding: 2rem 2.25rem 4rem; }
    .aurora-hero {
        display: flex; align-items: center; justify-content: space-between; gap: 1.25rem;
        padding: 1.45rem 1.6rem; margin-bottom: 1.35rem; border-radius: 24px;
        background: linear-gradient(115deg, rgba(22, 69, 105, .64), rgba(12, 46, 57, .54));
        border: 1px solid var(--border); backdrop-filter: blur(22px);
        -webkit-backdrop-filter: blur(22px); box-shadow: 0 24px 70px rgba(0, 0, 0, .28);
    }
    .aurora-brand { display:flex; align-items:center; gap: .85rem; }
    .aurora-logo { width:46px;height:46px;display:grid;place-items:center;border-radius:15px;
        background:linear-gradient(135deg,var(--cyan),var(--emerald));color:#06202c;font-size:1.35rem;
        box-shadow:0 0 28px rgba(103,232,249,.26); }
    .aurora-hero h1 { margin:0; font-size:clamp(1.45rem,3vw,2.15rem); letter-spacing:-.035em; color:var(--text); }
    .aurora-hero p { margin:.3rem 0 0; color:var(--muted); font-size:.95rem; }
    .aurora-status { white-space:nowrap; padding:.5rem .8rem; border-radius:999px;
        background:rgba(94,234,212,.09); border:1px solid rgba(94,234,212,.24); color:#b8fff1; font-size:.8rem; }
    .aurora-status::before { content:""; display:inline-block; width:7px;height:7px;border-radius:50%;
        background:var(--emerald);margin-right:.5rem;box-shadow:0 0 12px var(--emerald); }
    [data-testid="stVerticalBlockBorderWrapper"] {
        border: 1px solid var(--border) !important; border-radius: 22px !important;
        background: var(--glass) !important; backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px); box-shadow: 0 18px 48px rgba(0,0,0,.22);
    }
    [data-testid="stVerticalBlockBorderWrapper"] > div { padding: .4rem; }
    h1,h2,h3,h4,p,label,[data-testid="stMarkdownContainer"] { color:var(--text); }
    small,[data-testid="stCaptionContainer"],[data-testid="stWidgetLabel"] p { color:var(--muted) !important; }
    .aurora-eyebrow { color:var(--cyan); text-transform:uppercase; letter-spacing:.13em;
        font-size:.72rem;font-weight:750;margin-bottom:.35rem; }
    .aurora-copy { color:var(--muted); line-height:1.65; }
    [data-testid="stFileUploaderDropzone"] { background:rgba(6,17,31,.45); border:1px dashed rgba(103,232,249,.46);
        border-radius:16px; transition:border-color .2s,background .2s,transform .2s; }
    [data-testid="stFileUploaderDropzone"]:hover { border-color:var(--cyan);background:rgba(31,95,119,.25);transform:translateY(-1px); }
    [data-testid="stFileUploaderDropzone"] button { background:linear-gradient(100deg,var(--cyan),var(--emerald));
        border:0;color:#02131b !important;font-weight:800; }
    [data-testid="stFileUploaderDropzone"] button p { color:#02131b !important; }
    [data-baseweb="select"] > div { background:rgba(6,17,31,.78);border-color:var(--border);border-radius:13px;
        color:var(--text) !important; }
    [data-baseweb="select"] span,[data-baseweb="select"] svg,[role="listbox"],[role="option"] {
        color:var(--text) !important; }
    [role="listbox"] { background:var(--glass-strong) !important; }
    [data-testid="stBaseButton-primary"] { border:0;border-radius:13px;font-weight:800;color:#02131b !important;
        background:linear-gradient(100deg,var(--cyan),var(--emerald));box-shadow:0 12px 28px rgba(71,211,207,.19); }
    [data-testid="stBaseButton-primary"] p { color: #02131b !important; }
    [data-testid="stBaseButton-primary"]:hover { color:#02131b !important;filter:brightness(1.08);transform:translateY(-1px); }
    [data-testid="stBaseButton-primary"]:hover p { color:#02131b !important; }
    button:focus-visible, input:focus-visible, [role="combobox"]:focus-visible, summary:focus-visible {
        outline:3px solid var(--cyan) !important;outline-offset:3px !important; }
    [data-testid="stAlert"] { background:rgba(11,36,55,.96);border:1px solid var(--border);border-radius:15px;
        color:var(--text) !important; }
    [data-testid="stAlert"] p,[data-testid="stAlert"] svg { color:var(--text) !important;fill:currentColor; }
    [data-testid="stImage"] img { border-radius:17px;box-shadow:0 16px 45px rgba(0,0,0,.25); }
    .st-key-control_rail,.st-key-analysis_workspace,.st-key-document_inspector {
        min-height:min(680px,calc(100vh - 190px)) !important;
    }
    .st-key-document_stage {
        height:min(54vh,540px) !important;max-height:min(54vh,540px) !important;
        display:flex;align-items:center;justify-content:center;overflow:hidden !important;
        border-radius:15px;background:rgba(3,13,24,.42);padding:.65rem;
    }
    .st-key-document_stage [data-testid="stImage"] { width:100%;height:100%;display:flex;align-items:center;justify-content:center; }
    .st-key-document_stage [data-testid="stImage"] > div { width:100%;height:100%;display:flex;align-items:center;justify-content:center; }
    .st-key-document_stage [data-testid="stImage"] img {
        display:block;width:auto !important;max-width:100% !important;height:auto !important;
        max-height:min(50vh,500px) !important;margin:auto;object-fit:contain;
    }
    .st-key-document_inspector [data-testid="stPopover"] button {
        width:100%;border:1px solid var(--border);background:rgba(6,17,31,.78);color:var(--text) !important;
    }
    .st-key-document_inspector [data-testid="stPopover"] button p,
    .st-key-document_inspector [data-testid="stPopover"] button svg { color:var(--text) !important;fill:currentColor; }
    [data-testid="stExpander"] { background:rgba(7,21,36,.44);border:1px solid var(--border);border-radius:16px;overflow:hidden; }
    [data-testid="stExpander"] summary,[data-testid="stExpander"] summary p,[data-testid="stExpander"] summary svg {
        color:var(--text) !important;fill:currentColor; }
    [data-testid="stAudio"] { border-radius:14px;overflow:hidden;margin-top:.65rem; }
    [data-testid="stProgress"] { background:rgba(6,17,31,.96);border-radius:12px;overflow:hidden; }
    [data-testid="stProgress"] > div > div { background:linear-gradient(90deg,var(--cyan),var(--emerald)); }
    [data-testid="stProgress"] [data-testid="stMarkdownContainer"] p,
    [data-testid="stProgress"] p { color:#02131b !important;font-weight:800;text-shadow:none !important; }
    hr { border-color:rgba(164,220,238,.13); }
    .aurora-badge { display:inline-flex;padding:.28rem .58rem;margin:0 .35rem .35rem 0;border-radius:999px;
        background:rgba(103,232,249,.1);border:1px solid rgba(103,232,249,.2);color:#b8f5ff;
        font-size:.72rem;font-weight:750;letter-spacing:.06em; }
    @media (max-width: 900px) {
        .block-container { padding:1rem .85rem 3rem; }
        .aurora-hero { align-items:flex-start;flex-direction:column;padding:1.1rem; }
        .aurora-status { white-space:normal; }
        [data-testid="stHorizontalBlock"] { flex-direction:column; }
        [data-testid="column"] { width:100% !important;flex:1 1 auto !important; }
    }
    @media (prefers-reduced-motion: reduce) {
        *,*::before,*::after { scroll-behavior:auto !important;transition:none !important;animation:none !important; }
    }
    </style>
    """


def apply_midnight_aurora() -> None:
    st.markdown(midnight_aurora_css(), unsafe_allow_html=True)


def render_header() -> None:
    st.markdown("""
    <section class="aurora-hero">
      <div class="aurora-brand">
        <div class="aurora-logo">◈</div>
        <div><h1>Accessibility Solution Analyst</h1>
        <p>Ảnh hoặc PDF → phân tích cấu trúc → tóm tắt thông minh → audio</p></div>
      </div>
      <div class="aurora-status">AI sẵn sàng · Tự nhận diện ngôn ngữ</div>
    </section>
    """, unsafe_allow_html=True)


def render_status(message: str) -> None:
    st.markdown(f'<div class="aurora-copy">{message}</div>', unsafe_allow_html=True)
