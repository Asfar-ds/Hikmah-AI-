import streamlit as st
import pandas as pd, numpy as np, faiss, os, re
from sentence_transformers import SentenceTransformer
from openai import OpenAI

# ---------------------------
# Config
# ---------------------------
INDEX_PATH = "./urdu_arabic_books.index"
CHUNKS_PATH = "./RAG_chunks.csv"
EMBED_MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
LLM_MODEL = "gpt-4-turbo"


# ---------------------------
# Load models and data
# ---------------------------
client = OpenAI(api_key=st.secrets["openai"]["api_key"])
embedder = SentenceTransformer(EMBED_MODEL)
index = faiss.read_index(INDEX_PATH)
chunks_df = pd.read_csv(CHUNKS_PATH)

# ---------------------------
# Helper functions
# ---------------------------
def clean_text(text):
    text = re.sub(r"[A-Za-z0-9]", "", str(text))
    text = re.sub(r"[^\u0600-\u06FF\s]", " ", text)
    return re.sub(r"\s+", " ", text).strip()

def search_chunks(query, top_k=3):
    q_emb = embedder.encode([query])
    q_np = np.array(q_emb, dtype="float32").reshape(1, -1)
    D, I = index.search(q_np, top_k)
    return [ {"book": chunks_df.iloc[i]["book"], "chunk": chunks_df.iloc[i]["chunk"]} for i in I[0] if i < len(chunks_df) ]

def generate_answer(query, passages):
    context = "\n\n".join([f"{p['book']}:\n{p['chunk']}" for p in passages])
    prompt = f"تم ایک ماہر اردو و عربی صرفی و نحوی تجزیہ کار ہو۔\nسوال: {query}\n\nعبارتیں:\n{context}\n\nسادہ اور جامع جواب دیں:"
    resp = client.chat.completions.create(
        model=LLM_MODEL,
        messages=[{"role":"user", "content": prompt}],
        temperature=0.5,
        max_tokens=500
    )
    return resp.choices[0].message.content.strip()

# ---------------------------
# Streamlit UI
# ---------------------------
st.title("🕌 Urdu Sarf Chatbot")
query = st.text_area("اپنا سوال درج کریں:")

if st.button("جواب حاصل کریں") and query.strip():
    with st.spinner("جواب تیار ہو رہا ہے..."):
        cleaned = clean_text(query)
        top_passages = search_chunks(cleaned)
        answer = generate_answer(cleaned, top_passages)

    st.markdown("### 🧠 جواب:")
    st.write(answer)

    st.markdown("### 📖 متعلقہ عبارتیں:")
    for p in top_passages:
        st.markdown(f"**{p['book']}** — {p['chunk']}")
