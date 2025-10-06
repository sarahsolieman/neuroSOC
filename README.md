# 🧠 neuroSOC

**neuroSOC** is a prototype that reimagines the Security Operations Center (SOC) workflow by integrating **AI** and **retrieval-augmented generation (RAG)**.  
It automatically summarizes incidents, correlates context from internal playbooks, and generates recommended next steps — reducing analyst triage time and surfacing institutional knowledge on demand.

---

## Overview

neuroSOC enhances SOC efficiency by using RAG to combine incident data with internal playbooks, enabling automated reasoning and decision support for analysts.

---

## Features

- **RAG-powered reasoning** – LLM retrieves and reasons over relevant SOC playbooks.  
- **Automated incident summaries** – Converts raw alerts into clear, structured insights.  
- **Knowledge transparency** – Displays which sources informed each recommendation.  
- **Interactive UI** – Streamlit app for quick demo and testing.

```
Incident Logs  →  Embedding Generator  →  FAISS Index
                          ↓
                   Similarity Search
                          ↓
             Retrieved Playbooks + Logs
                          ↓
                  LLM (Claude / GPT / Bedrock)
                          ↓
            Summary + Root Cause + Mitigation
```

---

## Tech Stack

- Python  
- FAISS for vector search  
- OpenAI / AWS Bedrock for embeddings + LLM  
- Streamlit for UI  
- pandas / json for log parsing  

---

## Example Prompt

**System:**  
You are an expert SOC analyst who summarizes and contextualizes security incidents.  
Be concise, technical, and actionable.

**User:**  
Here are raw logs and the top 3 relevant playbooks.

```
Logs:
{incident_logs}

Playbooks:
{retrieved_docs}
```

**Task:**  
1. Summarize the likely incident type.  
2. Identify affected assets or users.  
3. Recommend remediation and next steps.  
4. Include references to the playbooks used.


## Future Ideas

- Integrate real Splunk / SIEM APIs for live data  
- Add threat-intel enrichment (VirusTotal, AbuseIPDB)  
- Deploy via AWS Step Functions + Lambda for full automation  
- Fine-tune smaller open models for on-prem SOCs  

---

## Impact

Demonstrates how retrieval-augmented LLMs can enhance security operations by transforming noisy incident data into actionable intelligence — automating first-level triage and freeing analysts for higher-order reasoning.

