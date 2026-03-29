# =====================================================
# 🌙 Urdu Sarf Chatbot (Streamlit + OCR + FAISS + GPT)
# =====================================================

import streamlit as st
from sentence_transformers import SentenceTransformer
from openai import OpenAI
import pandas as pd, numpy as np, faiss, re, os

# ---------------------------
# ✅ Setup Models & Files
# ---------------------------
INDEX_PATH = "./urdu_arabic_books.index"
CHUNKS_PATH = "./RAG_chunks.csv"
EMBED_MODEL = "intfloat/multilingual-e5-base"
LLM_MODEL = "gpt-4-turbo"

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", "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"))
embedder = SentenceTransformer(EMBED_MODEL)
index = faiss.read_index(INDEX_PATH)
chunks_df = pd.read_csv(CHUNKS_PATH)

# ---------------------------
# 🔠 Text Cleaner
# ---------------------------
def clean_text(text):
    text = re.sub(r"[A-Za-z0-9]", "", str(text))
    text = re.sub(r"[^\u0600-\u06FF\s]", " ", text)
    return re.sub(r"\s+", " ", text).strip()

# ---------------------------
# 🔍 Retrieve from FAISS
# ---------------------------
def search_query(query, top_k=3):
    q_emb = embedder.encode([query])
    q_np = np.array(q_emb, dtype="float32")
    faiss.normalize_L2(q_np)
    D, I = index.search(q_np, top_k)
    results = []
    for idx in I[0]:
        if idx < len(chunks_df):
            results.append({
                "book": chunks_df.iloc[idx]["book"],
                "chunk": chunks_df.iloc[idx]["chunk"]
            })
    return results

# ---------------------------
# 💬 LLM Urdu Answer
# ---------------------------
def llm_urdu_response(query, passages):
    joined = "\n\n".join([f"📘 {p['book']}:\n{p['chunk']}" for p in passages])
    prompt = f"""
    تم ایک ماہر اردو و عربی صرفی و نحوی تجزیہ کار ہو۔
    سوال: {query}

    درج ذیل عبارتوں کو دیکھ کر جامع، سادہ، اور درست اردو میں جواب دو۔
    عبارتیں:
    {joined}

    آخر میں خلاصہ دو تاکہ قاری کو آسان فہم وضاحت ملے۔
    """
    resp = client.chat.completions.create(
        model=LLM_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5,
        max_tokens=400
    )
    return resp.choices[0].message.content.strip()

# ---------------------------
# ⚖️ LLM Evaluator
# ---------------------------
def llm_evaluator(query, passages):
    joined = "\n\n".join([f"{i+1}. {p['chunk']}" for i, p in enumerate(passages)])
    prompt = f"""
    You are an Urdu linguistic evaluator.
    Query: {query}
    Context:
    {joined}

    LABEL: <Relevant and accurate | Partially relevant | Irrelevant>
    REASON: <one line Urdu or English>
    """
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )
    return resp.choices[0].message.content.strip()

# ---------------------------
# 🎨 Streamlit UI
# ---------------------------
st.set_page_config(page_title="🕌 Urdu Sarf Chatbot", layout="centered")
st.title("🕌 Urdu Sarf Chatbot (RAG + LLM)")
st.caption("Urdu & Arabic Grammar Assistant using FAISS + GPT")

query = st.text_area("✍️ اپنا سوال درج کریں:", height=120, placeholder="مثلاً: فعل ماضی کی تعریف بتائیں۔")

if st.button("🔍 جواب حاصل کریں"):
    if query.strip():
        with st.spinner("جواب تیار ہو رہا ہے... ⏳"):
            q = clean_text(query)
            passages = search_query(q)
            answer = llm_urdu_response(q, passages)
            evaluation = llm_evaluator(q, passages)

        st.markdown("### 🧠 جواب:")
        st.write(answer)

        st.markdown("### 📖 متعلقہ عبارتیں:")
        for p in passages:
            st.markdown(f"**{p['book']}** — {p['chunk']}")

        st.markdown("### 🧾 جائزہ:")
        st.code(evaluation, language="text")
    else:
        st.warning("براہ کرم کوئی سوال درج کریں۔")

st.markdown("---")
st.caption("Developed by 🌸 Javeria Jameel — Urdu NLP + RAG System")
