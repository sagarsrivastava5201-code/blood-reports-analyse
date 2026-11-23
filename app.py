# import streamlit as st
# from dotenv import load_dotenv

# load_dotenv()

# from report_analyzer import analyze_report
# from chatbot import stream_reply

# # ---------- PAGE CONFIG ----------
# st.set_page_config(
#     page_title="HealthLens",
#     page_icon="🩺",
#     layout="wide",
# )

# # ---------- CUSTOM CSS ----------
# st.markdown(
#     """
# <style>
# .main-title {
#     font-size: 2.2rem; font-weight: 800;
#     background: linear-gradient(90deg, #0ea5e9, #10b981);
#     -webkit-background-clip: text; -webkit-text-fill-color: transparent;
#     margin-bottom: 0;
# }
# .sub-title { color: #6b7280; margin-top: 0; margin-bottom: 1.2rem; }
# .disclaimer {
#     background: rgba(245, 158, 11, 0.12);
#     border-left: 4px solid #f59e0b;
#     padding: 0.7rem 1rem; border-radius: 6px; font-size: 0.9rem;
# }
# div.stButton > button { border-radius: 10px; font-weight: 600; }

# /* ---------- Responsive tweaks ---------- */
# .block-container { max-width: 1100px; }

# /* Tables (test results): never overflow the screen */
# div[data-testid="stMarkdownContainer"] table {
#     display: block;
#     width: 100%;
#     overflow-x: auto;          /* scroll sideways if still too wide */
#     border-collapse: collapse;
#     font-size: 0.95rem;
# }
# div[data-testid="stMarkdownContainer"] th,
# div[data-testid="stMarkdownContainer"] td {
#     padding: 6px 8px;
#     vertical-align: top;
# }

# @media (max-width: 640px) {
#     .block-container { padding: 1rem 0.8rem 3rem 0.8rem; }
#     .main-title { font-size: 1.6rem; }
#     .sub-title { font-size: 0.95rem; }
#     .disclaimer { font-size: 0.8rem; padding: 0.5rem 0.7rem; }

#     div[data-testid="stMarkdownContainer"] h2 { font-size: 1.15rem; }
#     div[data-testid="stMarkdownContainer"] p,
#     div[data-testid="stMarkdownContainer"] li { font-size: 0.92rem; line-height: 1.5; }

#     div[data-testid="stMarkdownContainer"] table { font-size: 0.78rem; }
#     div[data-testid="stMarkdownContainer"] th,
#     div[data-testid="stMarkdownContainer"] td {
#         padding: 4px 5px;
#         white-space: normal;       /* wrap text instead of stretching */
#         word-break: break-word;
#     }
#     div.stButton > button, div.stDownloadButton > button { width: 100%; }
# }
# </style>
# """,
#     unsafe_allow_html=True,
# )

# # ---------- SESSION STATE ----------
# st.session_state.setdefault("report_analysis", None)
# st.session_state.setdefault("messages", [])

# # ---------- SIDEBAR ----------
# with st.sidebar:
#     st.markdown("## 🩺 HealthLens")
#     page = st.radio("Menu", ["🧪 Blood Report Analyzer", "💬 Health Chatbot"], label_visibility="collapsed")
#     st.divider()
#     if st.session_state.report_analysis:
#         st.success("Report loaded ✅\nThe chatbot now knows about your report.")
#     else:
#         st.info("No report uploaded yet.")
#     if st.button("🗑️ Reset everything", use_container_width=True):
#         st.session_state.report_analysis = None
#         st.session_state.messages = []
#         st.rerun()

# st.markdown('<p class="main-title">HealthLens</p>', unsafe_allow_html=True)
# st.markdown('<p class="sub-title">Understand your blood report in simple language.</p>', unsafe_allow_html=True)
# st.markdown(
#     '<div class="disclaimer">⚠️ This is for general information only and is not a substitute for medical advice. '
#     "Please consult a doctor before making any health decision.</div><br>",
#     unsafe_allow_html=True,
# )

# # ---------- PAGE 1: REPORT ANALYZER ----------
# if page == "🧪 Blood Report Analyzer":
#     uploaded = st.file_uploader(
#         "Upload your blood report (PDF, PNG, JPG)",
#         type=["pdf", "png", "jpg", "jpeg"],
#     )

#     if uploaded and st.button("🔍 Analyze Report", type="primary"):
#         with st.spinner("Reading your report... this may take a moment"):
#             try:
#                 st.session_state.report_analysis = analyze_report(uploaded, uploaded.type)
#                 st.session_state.messages = []  # new report = fresh chat
#             except Exception as e:
#                 st.error(f"Error: {e}")

#     if st.session_state.report_analysis:
#         st.markdown(st.session_state.report_analysis)
#         st.download_button(
#             "⬇️ Download Analysis",
#             st.session_state.report_analysis,
#             file_name="healthlens_report_analysis.md",
#         )
#         st.info("You can now ask questions about this report on the 'Health Chatbot' page. 💬")

# # ---------- PAGE 2: CHATBOT ----------
# else:
#     if not st.session_state.report_analysis:
#         st.caption("Tip: Upload a report first and the chatbot will answer based on it. You can also ask general health questions.")

#     for m in st.session_state.messages:
#         with st.chat_message(m["role"]):
#             st.markdown(m["content"])

#     if prompt := st.chat_input("Type your question..."):
#         st.session_state.messages.append({"role": "user", "content": prompt})
#         with st.chat_message("user"):
#             st.markdown(prompt)

#         with st.chat_message("assistant"):
#             try:
#                 reply = st.write_stream(
#                     stream_reply(st.session_state.messages, st.session_state.report_analysis)
#                 )
#                 st.session_state.messages.append({"role": "assistant", "content": reply})
#             except Exception as e:
#                 st.error(f"Error: {e}")
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

# ---------- CUSTOM CSS (ORIGINAL) ----------
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

# ---------- NEW: THEME + HERO + INFO + FOOTER STYLES ----------
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,600;9..144,700&family=DM+Sans:wght@400;500;600&display=swap');

:root {
    --hl-bg: #f2f8f7;
    --hl-ink: #12302f;
    --hl-muted: #4f6a68;
    --hl-teal: #0f766e;
    --hl-teal-soft: #d8eeea;
    --hl-line: #cfe3df;
    --hl-card: #ffffff;
}

/* Light, calm page */
.stApp { background: var(--hl-bg); color: var(--hl-ink); font-family: 'DM Sans', sans-serif; }
[data-testid="stSidebar"] { background: #e6f2ef; border-right: 1px solid var(--hl-line); }
[data-testid="stSidebar"] * { color: var(--hl-ink); }
.stApp h1, .stApp h2, .stApp h3 { font-family: 'Fraunces', serif; color: var(--hl-ink); }
.stApp p, .stApp li, .stApp label, .stApp span { color: var(--hl-ink); }
div.stButton > button[kind="primary"] { background: var(--hl-teal); border: none; color: #fff; }
div.stButton > button[kind="primary"]:hover { background: #0b5d57; }
[data-testid="stFileUploader"] section { background: #fff; border: 1.5px dashed var(--hl-teal); border-radius: 14px; }

/* Hero */
.hl-hero {
    background: var(--hl-teal);
    border-radius: 20px;
    padding: 2.4rem 2.2rem;
    margin-bottom: 1.4rem;
}
.hl-hero h1 {
    font-family: 'Fraunces', serif; font-weight: 700;
    font-size: 2.4rem; line-height: 1.15; margin: 0 0 0.7rem 0;
    color: #ffffff !important; max-width: 20ch;
}
.hl-hero p { color: #dff3ef !important; font-size: 1.05rem; max-width: 60ch; margin: 0; line-height: 1.6; }
.hl-chips { display: flex; flex-wrap: wrap; gap: 0.5rem; margin-top: 1.2rem; }
.hl-chip {
    background: rgba(255,255,255,0.16); color: #fff !important;
    padding: 0.3rem 0.8rem; border-radius: 999px; font-size: 0.85rem;
}
.hl-chip span { color: #fff !important; }

/* Info cards */
.hl-section-title { font-family: 'Fraunces', serif; font-size: 1.5rem; margin: 1.6rem 0 0.2rem 0; }
.hl-section-sub { color: var(--hl-muted) !important; margin: 0 0 1rem 0; }
.hl-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 0.9rem; }
.hl-card {
    background: var(--hl-card); border: 1px solid var(--hl-line);
    border-radius: 14px; padding: 1.1rem 1.1rem 1.2rem 1.1rem;
}
.hl-card .ic { font-size: 1.5rem; }
.hl-card h4 { margin: 0.4rem 0 0.3rem 0; font-size: 1.02rem; font-weight: 600; }
.hl-card p { margin: 0; font-size: 0.9rem; line-height: 1.5; color: var(--hl-muted) !important; }

/* Blood test glossary strip */
.hl-terms { background: #fff; border: 1px solid var(--hl-line); border-radius: 14px; padding: 1rem 1.2rem; margin-top: 1rem; }
.hl-terms dl { display: grid; grid-template-columns: 9rem 1fr; gap: 0.5rem 1rem; margin: 0; }
.hl-terms dt { font-weight: 600; color: var(--hl-teal) !important; }
.hl-terms dd { margin: 0; color: var(--hl-muted) !important; font-size: 0.92rem; }

.hl-divider { height: 1px; background: var(--hl-line); margin: 1.6rem 0; border: 0; }

/* Footer */
.hl-footer { margin-top: 3rem; border-top: 1px solid var(--hl-line); padding-top: 1.8rem; }
.hl-footer-grid { display: grid; grid-template-columns: 1.3fr 1fr 1fr; gap: 1.5rem; }
.hl-doc { display: flex; gap: 1rem; align-items: flex-start; }
.hl-avatar {
    flex: 0 0 64px; height: 64px; border-radius: 50%;
    background: var(--hl-teal-soft); display: flex; align-items: center; justify-content: center;
    font-size: 1.9rem;
}
.hl-footer h4 { font-family: 'Fraunces', serif; margin: 0 0 0.4rem 0; font-size: 1.05rem; }
.hl-footer p, .hl-footer li { font-size: 0.9rem; color: var(--hl-muted) !important; line-height: 1.55; margin: 0 0 0.3rem 0; }
.hl-footer ul { padding-left: 1.1rem; margin: 0; }
.hl-emergency {
    background: #fdecec; border-left: 4px solid #dc2626; border-radius: 8px;
    padding: 0.7rem 1rem; margin-top: 1.4rem; font-size: 0.9rem;
}
.hl-emergency, .hl-emergency * { color: #7f1d1d !important; }
.hl-copy { text-align: center; color: var(--hl-muted) !important; font-size: 0.82rem; margin-top: 1.4rem; }

@media (max-width: 900px) {
    .hl-grid { grid-template-columns: repeat(2, 1fr); }
    .hl-footer-grid { grid-template-columns: 1fr; }
}
@media (max-width: 640px) {
    .hl-hero { padding: 1.5rem 1.2rem; border-radius: 16px; }
    .hl-hero h1 { font-size: 1.6rem; }
    .hl-hero p { font-size: 0.95rem; }
    .hl-grid { grid-template-columns: 1fr; }
    .hl-terms dl { grid-template-columns: 1fr; gap: 0.1rem; }
    .hl-terms dd { margin-bottom: 0.6rem; }
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

# ---------- NEW: TOP SECTION (HERO + HEALTH INFO) ----------
st.markdown(
    """
<div class="hl-hero">
<h1>Understand your blood report in plain language</h1>
<p>Upload your report and HealthLens will explain each test in simple words. You can also ask the chatbot your questions.</p>
<div class="hl-chips">
<div class="hl-chip">PDF, PNG or JPG</div>
<div class="hl-chip">Simple explanations</div>
<div class="hl-chip">Download your analysis</div>
</div>
</div>

<div class="hl-section-title">Learn about your health</div>
<p class="hl-section-sub">Small daily habits keep you healthy for the long run.</p>
<div class="hl-grid">
<div class="hl-card"><div class="ic">🩸</div><h4>Regular checkups</h4><p>A blood test once a year helps catch illness early.</p></div>
<div class="hl-card"><div class="ic">🥗</div><h4>Balanced diet</h4><p>Eat green vegetables, lentils and fruit with less oil and spice. Keep sugar and junk food low.</p></div>
<div class="hl-card"><div class="ic">🚶</div><h4>Walk daily</h4><p>At least 30 minutes of walking or light exercise a day is good for your heart and blood sugar.</p></div>
<div class="hl-card"><div class="ic">😴</div><h4>Enough sleep</h4><p>Adults need 7 to 8 hours of sleep every day. Too little sleep increases tiredness and stress.</p></div>
</div>

<div class="hl-terms">
<dl>
<dt>Hemoglobin</dt><dd>The protein that carries oxygen in your blood. Low levels can cause weakness or anemia.</dd>
<dt>Blood sugar</dt><dd>The amount of glucose in your blood. High levels can point to a risk of diabetes.</dd>
<dt>Cholesterol</dt><dd>A fatty substance in your blood. High levels raise the risk of heart disease.</dd>
<dt>Creatinine</dt><dd>A test that shows how well your kidneys are working.</dd>
</dl>
</div>
<hr class="hl-divider">
""",
    unsafe_allow_html=True,
)

# ---------- ORIGINAL: TITLE + DISCLAIMER ----------
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

# ---------- NEW: FOOTER ----------
st.markdown(
    """
<div class="hl-footer">
<div class="hl-footer-grid">
<div>
<h4>About the doctor</h4>
<div class="hl-doc">
<div class="hl-avatar">👨‍⚕️</div>
<div>
<p><b>sagar srivastava</b><br>MBBS, MD (General Medicine)</p>
<p>15+ years of experience. Specializes in reading blood reports and advising on the right tests.</p>
</div>
</div>
</div>
<div>
<h4>What HealthLens does</h4>
<ul>
<li>Explains your blood report in simple language</li>
<li>Flags values outside the normal range</li>
<li>Answers your questions through a chatbot</li>
</ul>
</div>
<div>
<h4>Contact</h4>
<p>Clinic: Lucknow, Uttar Pradesh<br>Hours: Monday to Saturday, 10 AM to 6 PM<br>Email: sagar@123gmail.com</p>
</div>
</div>
<div class="hl-emergency"><b>In an emergency:</b> if you have chest pain, trouble breathing or fainting, call 112 or 108 right away. Do not wait for a report.</div>
<p class="hl-copy">HealthLens is for general information only. It does not replace a doctor's advice.</p>
</div>
""",
    unsafe_allow_html=True,
)