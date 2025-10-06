import streamlit as st
import json
from rag_pipeline import run_pipeline
import os
import time

# Force demo mode for Streamlit app
os.environ["DEMO_MODE"] = "True"

# ---- Demo JSON Log ----
demo_log = {
    "events": [
        {"event": "failed_login", "username": "admin", "source_ip": "192.168.1.5", "timestamp": "2024-07-01T08:45:21Z"},
        {"event": "failed_login", "username": "admin", "source_ip": "192.168.1.5", "timestamp": "2024-07-01T08:45:35Z"},
        {"event": "successful_login", "username": "admin", "source_ip": "192.168.1.5", "timestamp": "2024-07-01T08:45:40Z"}
    ]
}

# ---- Page Config ----
st.set_page_config(page_title="NeuroSOC | AI-Augmented SOC", page_icon="🧠", layout="wide")

# ---- Custom Styling ----
st.markdown("""
<style>
body { background-color: #0B0C10; color: #E6E6E6; }
.stApp { background-color: #0B0C10; }
h1, h2, h3 { color: #00C6C2; }

div[data-testid="column"]:first-child { flex: 1.3 !important; }
div[data-testid="column"]:last-child { flex: 1.2 !important; }

textarea, input[type="file"], button { font-size: 1.05rem !important; }

.result-box {
    background-color: #1C1F26;
    border-radius: 10px;
    padding: 1rem;
    border-left: 4px solid #00C6C2;
    opacity: 0;
    animation: fadeInPulse 1.2s ease forwards;
}
@keyframes fadeInPulse {
    0% { opacity: 0; transform: scale(0.98); box-shadow: 0 0 0px #00C6C2; }
    50% { opacity: 1; transform: scale(1.01); box-shadow: 0 0 14px #00C6C2; }
    100% { opacity: 1; transform: scale(1); box-shadow: 0 0 0px transparent; }
}

.result-footer {
    font-size: 0.85rem;
    color: #AAAAAA;
    text-align: right;
    margin-top: 0.5rem;
    font-style: italic;
}

.stButton>button {
    background-color: #00C6C2;
    color: #0B0C10;
    border-radius: 8px;
    font-weight: 600;
    border: none;
    height: 2.8em;
    width: 100%;
    font-size: 1.05rem;
}
.stButton>button:hover { background-color: #08E2DD; color: #0B0C10; }

/* Floating badges */
.demo-badge, .live-badge {
    position: fixed;
    top: 15px;
    right: 25px;
    padding: 6px 14px;
    border-radius: 8px;
    font-weight: 600;
    font-size: 0.9em;
    text-transform: uppercase;
    z-index: 9999;
    transition: opacity 1s ease-out;
}

.demo-badge {
    background-color: rgba(0, 198, 194, 0.15);
    border: 1px solid #00C6C2;
    color: #00E6E2;
    animation: pulse 1.5s infinite;
}

.badge-analyzing {
    background-color: rgba(0, 128, 255, 0.15);
    border: 1px solid #0096FF;
    color: #66CCFF;
    animation: glowBlue 1.5s infinite;
}
.badge-generating {
    background-color: rgba(255, 165, 0, 0.1);
    border: 1px solid #FFA500;
    color: #FFD580;
    animation: glowAmber 1.5s infinite;
}
.badge-finalizing {
    background-color: rgba(0, 200, 0, 0.1);
    border: 1px solid #00FF7F;
    color: #ADFFB2;
    animation: glowGreen 1.5s infinite;
}

@keyframes pulse {
    0% { box-shadow: 0 0 5px #00C6C2; }
    50% { box-shadow: 0 0 20px #00C6C2; }
    100% { box-shadow: 0 0 5px #00C6C2; }
}
@keyframes glowBlue {
    0% { box-shadow: 0 0 5px #0096FF; }
    50% { box-shadow: 0 0 20px #0096FF; }
    100% { box-shadow: 0 0 5px #0096FF; }
}
@keyframes glowAmber {
    0% { box-shadow: 0 0 5px #FFA500; }
    50% { box-shadow: 0 0 20px #FFA500; }
    100% { box-shadow: 0 0 5px #FFA500; }
}
@keyframes glowGreen {
    0% { box-shadow: 0 0 5px #00FF7F; }
    50% { box-shadow: 0 0 20px #00FF7F; }
    100% { box-shadow: 0 0 5px #00FF7F; }
}

/* Tooltip style */
.info-bubble {
    display:inline-block;
    background-color:#00C6C2;
    color:#0B0C10;
    font-weight:bold;
    border-radius:50%;
    width:18px;
    height:18px;
    text-align:center;
    line-height:18px;
    font-size:12px;
    margin-left:6px;
    animation:pulseInfo 2s infinite ease-in-out;
}
@keyframes pulseInfo {
    0%,100% { box-shadow:0 0 3px #00C6C2; transform:scale(1); }
    50% { box-shadow:0 0 12px #00E6E2; transform:scale(1.15); }
}
.tooltip-box {
    visibility:hidden;
    position:absolute;
    background-color:#1C1F26;
    color:#E6E6E6;
    text-align:left;
    border-radius:6px;
    padding:0.6rem;
    border:1px solid #00C6C2;
    font-size:0.85rem;
    width:240px;
    bottom:125%;
    left:50%;
    margin-left:-120px;
    opacity:0;
    transition:opacity 0.3s;
    z-index:100;
}
.info-container {
    position:relative;
    display:inline-flex;
    align-items:center;
    cursor:help;
}
.info-container:hover .tooltip-box {
    visibility:visible;
    opacity:1;
}
</style>
""", unsafe_allow_html=True)

# ---- Header ----
st.markdown("<h1>🧠 NeuroSOC</h1>", unsafe_allow_html=True)
st.markdown("<h3>Adaptive AI for Security Operations</h3>", unsafe_allow_html=True)
st.divider()

# ---- Layout ----
col1, col2 = st.columns([1.3, 1.2])

with col1:
    st.subheader("📁 Incident Input")

    # Tooltip beside Use Demo Log
    st.markdown("""
    <div class="info-container">
        <strong>🔄 Use Demo Log</strong>
        <div class="info-bubble">i</div>
        <div class="tooltip-box">
            Demo mode uses a preloaded authentication anomaly log
            to demonstrate NeuroSOC’s incident analysis workflow.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ✅ Default demo ON
    use_demo = st.toggle("", value=True, label_visibility="collapsed")

    if use_demo:
        st.markdown("<div class='demo-badge'>Demo Mode Active</div>", unsafe_allow_html=True)
        st.info("Demo Mode Enabled — using built-in sample authentication anomaly log.")
        demo_text = json.dumps(demo_log, indent=2)
        st.text_area("Demo Log Preview:", demo_text, height=240, disabled=True)
        manual_input = demo_text
    else:
        uploaded = st.file_uploader("Upload your log (.json/.log)", type=["json", "log", "txt"])
        manual_input = st.text_area("Or paste log data below:", height=240)

    run_btn = st.button("Run Analysis ▶", use_container_width=True)

with col2:
    st.markdown("""
    <div class="info-container">
        <h3 style="display:inline;">🧠 AI Summary</h3>
        <div class="info-bubble">i</div>
        <div class="tooltip-box">
            This section displays the AI-generated incident summary, 
            including type, root cause, impacted assets, and recommended actions.
        </div>
    </div>
    """, unsafe_allow_html=True)

    if run_btn:
        if use_demo:
            summary = run_pipeline(json.dumps(demo_log))
            st.markdown("<div class='demo-badge'>Demo Mode Active</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='result-box'>{summary}</div>", unsafe_allow_html=True)
            st.markdown("<div class='result-footer'>Generated using FAISS retrieval + GPT reasoning pipeline — results may vary with log content.</div>", unsafe_allow_html=True)
            st.session_state["summary"] = summary
        else:
            content = None
            if uploaded:
                content = uploaded.read().decode("utf-8")
            elif manual_input.strip():
                content = manual_input
            else:
                st.warning("Please upload or paste logs first.")
                st.stop()

            badge_placeholder = st.empty()
            badge_placeholder.markdown("<div class='live-badge badge-analyzing'>Analyzing logs...</div>", unsafe_allow_html=True)
            time.sleep(1.2)
            badge_placeholder.markdown("<div class='live-badge badge-generating'>Generating summary...</div>", unsafe_allow_html=True)
            time.sleep(1.2)
            badge_placeholder.markdown("<div class='live-badge badge-finalizing'>Finalizing report...</div>", unsafe_allow_html=True)
            time.sleep(1.0)

            with st.spinner("Running NeuroSOC pipeline..."):
                summary = run_pipeline(content)
                time.sleep(0.5)

            badge_placeholder.empty()
            st.markdown(f"<div class='result-box'>{summary}</div>", unsafe_allow_html=True)
            st.markdown("<div class='result-footer'>Generated using FAISS retrieval + GPT reasoning pipeline — results may vary with log content.</div>", unsafe_allow_html=True)
            st.session_state["summary"] = summary
    elif "summary" in st.session_state:
        st.markdown(f"<div class='result-box'>{st.session_state['summary']}</div>", unsafe_allow_html=True)
        st.markdown("<div class='result-footer'>Generated using FAISS retrieval + GPT reasoning pipeline — results may vary with log content.</div>", unsafe_allow_html=True)
    else:
        st.info("Upload or paste logs and click 'Run Analysis'.")

st.divider()
st.caption("FAISS retrieval + LLM reasoning pipeline | v1.0 — NeuroSOC")




