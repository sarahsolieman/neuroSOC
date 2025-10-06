import os
import json
import faiss
import numpy as np
import openai
from pathlib import Path

DEMO_MODE = False
openai.api_key = os.getenv("OPENAI_API_KEY")
EMBED_MODEL = "text-embedding-3-small"
LLM_MODEL = "gpt-4o-mini"
KB_DIR = "./knowledge_base"
INDEX_FILE = "./faiss_index.bin"

def load_md_files(folder):
    docs = []
    for path in Path(folder).rglob("*.md"):
        with open(path, "r", encoding="utf-8") as f:
            docs.append({"title": path.stem, "content": f.read()})
    return docs

def build_faiss_index(docs):
    print("Building FAISS index...")
    embeddings = [
        openai.embeddings.create(model=EMBED_MODEL, input=d["content"])["data"][0]["embedding"]
        for d in docs
    ]
    dim = len(embeddings[0])
    index = faiss.IndexFlatL2(dim)
    index.add(np.array(embeddings).astype("float32"))
    faiss.write_index(index, INDEX_FILE)
    print(f"Indexed {len(docs)} playbooks.")
    return index, docs

def load_faiss_index():
    docs = load_md_files(KB_DIR)
    if not Path(INDEX_FILE).exists():
        return build_faiss_index(docs)
    index = faiss.read_index(INDEX_FILE)
    return index, docs

def retrieve_docs(query, index, docs, top_k=3):
    q_emb = openai.embeddings.create(model=EMBED_MODEL, input=query)["data"][0]["embedding"]
    q_emb = np.array(q_emb).astype("float32").reshape(1, -1)
    D, I = index.search(q_emb, top_k)
    return [docs[i]["content"] for i in I[0]]

def make_prompt(log_text, retrieved_docs):
    return f"""
You are an experienced SOC analyst.
Analyze the incident logs below using the provided playbooks.
Summarize the incident in bullet points.

Logs:
{log_text}

Relevant Playbooks:
{retrieved_docs}

Output:
1. Incident Type
2. Root Cause
3. Affected Assets
4. Recommended Response Actions
5. Which playbooks informed your reasoning
"""

def run_pipeline(log_text, top_k=3):
    index, docs = load_faiss_index()
    retrieved = retrieve_docs(log_text, index, docs, top_k)
    prompt = make_prompt(log_text, "\n\n".join(retrieved))

    response = openai.chat.completions.create(
        model=LLM_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )
    return response.choices[0].message.content

if __name__ == "__main__":
    with open("incident_case.json") as f:
        case = json.load(f)
    log_text = "\n".join([str(e) for e in case["timeline"]])
    print(run_pipeline(log_text))


# Demo Mode Helper Function

import os
import json
from pathlib import Path

def save_demo_artifacts(summary_text, docs=None, faiss_index=None):
    """
    Saves the current pipeline outputs so they can be reused in demo mode.

    Creates a 'demo/' folder (if it doesn’t exist) and writes:
      - summary.md     : the generated summary
      - docs.json      : the document chunks used to build the index (optional)
      - index.faiss    : the FAISS index file (optional)
    """

    demo_dir = Path("demo")
    demo_dir.mkdir(exist_ok=True)

    # 1. Save the summary text
    summary_path = demo_dir / "summary.md"
    summary_path.write_text(summary_text)
    print(f"[✓] Saved summary to {summary_path}")

    # 2. Save document chunks (if provided)
    if docs is not None:
        docs_path = demo_dir / "docs.json"
        docs_path.write_text(json.dumps(docs, indent=2))
        print(f"[✓] Saved docs to {docs_path}")

    # 3. Save FAISS index (if provided)
    if faiss_index is not None:
        try:
            import faiss
            index_path = demo_dir / "index.faiss"
            faiss.write_index(faiss_index, str(index_path))
            print(f"[✓] Saved FAISS index to {index_path}")
        except ImportError:
            print("[!] FAISS not installed — skipped saving index.")

    print("[✓] Demo artifacts saved successfully.")
