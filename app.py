import streamlit as st
from dotenv import load_dotenv

load_dotenv()

from report_analyzer import analyze_report
from chatbot import stream_reply

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="HealthLens",
    page_icon="🩺",
    layout="wide",
)

# ---------- CUSTOM CSS ----------
st.markdown(
    """
<style>
.main-title {
    font-size: 2.2rem; font-weight: 800;
    background: linear-gradient(90deg, #0ea5e9, #10b981);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    margin-bottom: 0;
}
.sub-title { color: #6b7280; margin-top: 0; margin-bottom: 1.2rem; }
.disclaimer {
    background: rgba(245, 158, 11, 0.12);
    border-left: 4px solid #f59e0b;
    padding: 0.7rem 1rem; border-radius: 6px; font-size: 0.9rem;
}
div.stButton > button { border-radius: 10px; font-weight: 600; }

/* ---------- Responsive tweaks ---------- */
.block-container { max-width: 1100px; }

/* Tables (test results): never overflow the screen */
div[data-testid="stMarkdownContainer"] table {
    display: block;
    width: 100%;
    overflow-x: auto;          /* scroll sideways if still too wide */
    border-collapse: collapse;
    font-size: 0.95rem;
}
div[data-testid="stMarkdownContainer"] th,
div[data-testid="stMarkdownContainer"] td {
    padding: 6px 8px;
    vertical-align: top;
}

@media (max-width: 640px) {
    .block-container { padding: 1rem 0.8rem 3rem 0.8rem; }
    .main-title { font-size: 1.6rem; }
    .sub-title { font-size: 0.95rem; }
    .disclaimer { font-size: 0.8rem; padding: 0.5rem 0.7rem; }

    div[data-testid="stMarkdownContainer"] h2 { font-size: 1.15rem; }
    div[data-testid="stMarkdownContainer"] p,
    div[data-testid="stMarkdownContainer"] li { font-size: 0.92rem; line-height: 1.5; }

    div[data-testid="stMarkdownContainer"] table { font-size: 0.78rem; }
    div[data-testid="stMarkdownContainer"] th,
    div[data-testid="stMarkdownContainer"] td {
        padding: 4px 5px;
        white-space: normal;       /* wrap text instead of stretching */
        word-break: break-word;
    }
    div.stButton > button, div.stDownloadButton > button { width: 100%; }
}
</style>
""",
    unsafe_allow_html=True,
)

# ---------- SESSION STATE ----------
st.session_state.setdefault("report_analysis", None)
st.session_state.setdefault("messages", [])

# ---------- SIDEBAR ----------
with st.sidebar:
    st.markdown("## 🩺 HealthLens")
    page = st.radio("Menu", ["🧪 Blood Report Analyzer", "💬 Health Chatbot"], label_visibility="collapsed")
    st.divider()
    if st.session_state.report_analysis:
        st.success("Report loaded ✅\nThe chatbot now knows about your report.")
    else:
        st.info("No report uploaded yet.")
    if st.button("🗑️ Reset everything", use_container_width=True):
        st.session_state.report_analysis = None
        st.session_state.messages = []
        st.rerun()

st.markdown('<p class="main-title">HealthLens</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Understand your blood report in simple language.</p>', unsafe_allow_html=True)
st.markdown(
    '<div class="disclaimer">⚠️ This is for general information only and is not a substitute for medical advice. '
    "Please consult a doctor before making any health decision.</div><br>",
    unsafe_allow_html=True,
)

# ---------- PAGE 1: REPORT ANALYZER ----------
if page == "🧪 Blood Report Analyzer":
    uploaded = st.file_uploader(
        "Upload your blood report (PDF, PNG, JPG)",
        type=["pdf", "png", "jpg", "jpeg"],
    )

    if uploaded and st.button("🔍 Analyze Report", type="primary"):
        with st.spinner("Reading your report... this may take a moment"):
            try:
                st.session_state.report_analysis = analyze_report(uploaded, uploaded.type)
                st.session_state.messages = []  # new report = fresh chat
            except Exception as e:
                st.error(f"Error: {e}")

    if st.session_state.report_analysis:
        st.markdown(st.session_state.report_analysis)
        st.download_button(
            "⬇️ Download Analysis",
            st.session_state.report_analysis,
            file_name="healthlens_report_analysis.md",
        )
        st.info("You can now ask questions about this report on the 'Health Chatbot' page. 💬")

# ---------- PAGE 2: CHATBOT ----------
else:
    if not st.session_state.report_analysis:
        st.caption("Tip: Upload a report first and the chatbot will answer based on it. You can also ask general health questions.")

    for m in st.session_state.messages:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])

    if prompt := st.chat_input("Type your question..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            try:
                reply = st.write_stream(
                    stream_reply(st.session_state.messages, st.session_state.report_analysis)
                )
                st.session_state.messages.append({"role": "assistant", "content": reply})
            except Exception as e:
                st.error(f"Error: {e}")