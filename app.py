import streamlit as st
import json
from rag_pipeline import run_pipeline

st.set_page_config(page_title="NeuroSOC | AI-Augmented SOC", page_icon="🧠", layout="wide")

st.markdown("""
    <style>
        body { background-color: #0B0C10; color: #E6E6E6; }
        .stApp { background-color: #0B0C10; }
        h1, h2, h3 { color: #00C6C2; }
        .result-box {
            background-color: #1C1F26;
            border-radius: 10px;
            padding: 1rem;
            border-left: 4px solid #00C6C2;
        }
        .small-text { font-size: 0.9em; color: #B3B3B3; }
        .stButton>button {
            background-color: #00C6C2;
            color: #0B0C10;
            border-radius: 8px;
            font-weight: 600;
            border: none;
            height: 2.5em;
            width: 100%;
        }
        .stButton>button:hover { background-color: #08E2DD; color: #0B0C10; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1>🧠 NeuroSOC</h1>", unsafe_allow_html=True)
st.markdown("<h3>Adaptive AI for Security Operations</h3>", unsafe_allow_html=True)
st.divider()

col1, col2 = st.columns([1, 1.5])

with col1:
    st.subheader("📁 Incident Input")
    uploaded = st.file_uploader("Upload your log (.json/.log)", type=["json", "log", "txt"])
    manual_input = st.text_area("Or paste log data below:", height=220)
    run_btn = st.button("Run Analysis ▶")

with col2:
    st.subheader("🧠 AI Summary")

    if run_btn:
        if uploaded:
            content = uploaded.read().decode("utf-8")
        elif manual_input.strip():
            content = manual_input
        else:
            st.warning("Please upload or paste logs first.")
            st.stop()

        with st.spinner("Analyzing with NeuroSOC..."):
            summary = run_pipeline(content)

        st.markdown(f"<div class='result-box'>{summary}</div>", unsafe_allow_html=True)
        st.session_state["summary"] = summary

    elif "summary" in st.session_state:
        st.markdown(f"<div class='result-box'>{st.session_state['summary']}</div>", unsafe_allow_html=True)
    else:
        st.info("Upload or paste logs and click 'Run Analysis'.")

st.divider()
st.caption("FAISS retrieval + LLM reasoning pipeline | v1.0 — NeuroSOC")
