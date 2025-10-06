# 🧠 neuroSOC

**neuroSOC** is a prototype that reimagines the Security Operations Center (SOC) workflow by integrating **AI** and **retrieval-augmented generation (RAG)**.  
It automatically summarizes incidents, correlates context from internal playbooks, and generates recommended next steps — reducing analyst triage time and surfacing institutional knowledge on demand.

---

## Live Demo  

[![Launch Demo](https://img.shields.io/badge/Launch%20Demo-00C6C2?style=for-the-badge&logo=streamlit&logoColor=white)](https://neurosoc.streamlit.app)

This hosted version runs **entirely in demo mode** — it showcases the workflow and interface without real API calls or external dependencies.  
For realistic results, clone the repo, disable demo mode, and add your own `OPENAI_API_KEY`.

---

## Demo-Only Mode

> **Note:** The deployed version of **neuroSOC** runs entirely in demo mode.  
> It always returns a **pre-generated summary** and **example response** to illustrate functionality.  
>  
> To run it in live, realistic mode, you’d need to:
> 1. Disable demo mode (`DEMO_MODE=False`)  
> 2. Add a valid `OPENAI_API_KEY` to your environment  
>  
> The demo exists purely to show the **end-to-end pipeline, UI, and reasoning flow** without requiring API usage.

---

## Overview

neuroSOC enhances SOC efficiency by combining incident data with internal playbooks using RAG — enabling automated reasoning, faster triage, and contextual recommendations for analysts.

---

## Features

- **RAG-powered reasoning** – LLM retrieves and reasons over relevant SOC playbooks.  
- **Automated incident summaries** – Converts raw alerts into structured insights.  
- **Knowledge transparency** – Displays which sources informed each recommendation.  
- **Interactive UI** – Streamlit-based demo for quick visualization and testing.

## Tech Stack

- **Python**  
- **FAISS** – Vector similarity search  
- **OpenAI / Bedrock APIs** – (used only in full version)  
- **Streamlit** – Web demo interface  
- **pandas / json** – Log parsing  

---

## Example Prompt (Full Version)

**System:**  
You are an expert SOC analyst who summarizes and contextualizes security incidents.  
Be concise, technical, and actionable.

**User:**  
Here are raw logs and the top 3 relevant playbooks.

Logs:
{incident_logs}

Playbooks:
{retrieved_docs}


**Task:**  
1. Summarize the likely incident type.  
2. Identify affected assets or users.  
3. Recommend remediation and next steps.  
4. Include references to the playbooks used.

---

## Future Roadmap

- Integrate live SIEM / Splunk ingestion  
- Add threat-intel enrichment (VirusTotal, AbuseIPDB)  
- Deploy to AWS Lambda + Step Functions for full automation  
- Fine-tune small models for on-prem SOCs  

---

## Impact

**neuroSOC** demonstrates how retrieval-augmented LLMs can enhance security operations by transforming noisy incident data into **actionable intelligence** — automating first-level triage and empowering analysts for deeper reasoning.


