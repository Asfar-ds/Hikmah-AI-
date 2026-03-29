"""
sarf_rag_with_evaluator.py
Attach GPT-4-turbo evaluation to your Sarf RAG pipeline.
"""

import os
import re
import json
import time
import fitz
import faiss
import numpy as np
import pandas as pd
from collections import Counter
from sentence_transformers import SentenceTransformer
from openai import OpenAI
import nltk
from nltk.corpus import stopwords

# -----------------------
# Config
# -----------------------
PDF_FOLDER = "./sarf-books"
CLEANED_FOLDER = "./cleaned_sarf_books"
CHUNKS_CSV = "./RAG_chunks.csv"
RAG_CSV = "./RAG_ready_books.csv"
FAISS_INDEX_PATH = "./urdu_arabic_books.index"
EVAL_LOG = "sarf_rag_evals.jsonl"

EMBED_MODEL = "intfloat/multilingual-e5-base"
LLM_MODEL = "gpt-4-turbo"
TOP_K = 3
CHUNK_SIZE = 200
TEMPERATURE = 0.0
MAX_RETRIES = 5
RETRY_WAIT = 2

os.makedirs(CLEANED_FOLDER, exist_ok=True)
nltk.download('stopwords')

# -----------------------
# OpenAI Client Setup
# -----------------------
OPENAI_API_KEY = os.environ.get("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")

if not OPENAI_API_KEY:
    # Optional fallback (local only)
    OPENAI_API_KEY = "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"

if not OPENAI_API_KEY or "sk-" not in OPENAI_API_KEY:
    raise RuntimeError("Please set a valid OPENAI_API_KEY environment variable.")

print("✅ OpenAI API Key loaded successfully!")
client = OpenAI(api_key=OPENAI_API_KEY)

# -----------------------
# Text Cleaning Utilities
# -----------------------
arabic_stopwords = set(stopwords.words("arabic"))
custom_urdu = {"ہے", "ہیں", "تھا", "تھی", "کے", "کی", "کا", "میں", "سے", "پر", "اور", "کو", "نے", "یہ", "وہ", "ہم", "تم", "کر", "گیا", "گئی"}
arabic_stopwords.update(custom_urdu)

def clean_text(text: str) -> str:
    text = re.sub(r"[A-Za-z0-9]", "", str(text))
    text = re.sub(r"[^\u0600-\u06FF\s]", " ", text)
    return re.sub(r"\s+", " ", text).strip()

def tokenize(text: str):
    return re.findall(r"[\u0600-\u06FF]+", str(text))

def remove_stopwords(tokens):
    return [t for t in tokens if t not in arabic_stopwords]

def urdu_stemmer(word):
    suffixes = ["وں", "یں", "ات", "اتوں", "یاں", "یوں", "گی", "گا", "ی", "ے", "ا"]
    for suf in suffixes:
        if word.endswith(suf) and len(word) > len(suf) + 2:
            return word[:-len(suf)]
    return word

# -----------------------
# Process PDFs → Cleaned Text
# -----------------------
# Read PDFs, clean, stem, save (✅ Final OCR version with preprocessing)
# -----------------------
import cv2
import easyocr

def process_pdfs(pdf_folder=PDF_FOLDER, cleaned_folder=CLEANED_FOLDER):
    records = []
    pdf_files = [f for f in os.listdir(pdf_folder) if f.lower().endswith(".pdf")]
    if not pdf_files:
        print("❌ No PDFs found in", pdf_folder)
        return pd.DataFrame(records)

    # Initialize OCR reader (Urdu + Arabic)
    ocr = easyocr.Reader(['ur', 'ar'], gpu=False)

    for file_name in pdf_files:
        path = os.path.join(pdf_folder, file_name)
        print(f"\n📘 Processing: {file_name}")
        text = ""

        try:
            with fitz.open(path) as pdf:
                for page_num, page in enumerate(pdf, 1):
                    page_text = page.get_text("text")

                    # 🧩 If no extractable text, fallback to OCR
                    if not page_text.strip():
                        pix = page.get_pixmap()
                        img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(
                            pix.height, pix.width, pix.n
                        )

                        # 🧠 Preprocess image before OCR
                        try:
                            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                        except:
                            gray = img  # fallback for grayscale-only images

                        # Enhance contrast
                        gray = cv2.equalizeHist(gray)

                        # Threshold + denoise
                        _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
                        thresh = cv2.medianBlur(thresh, 3)

                        # Slightly enlarge for better recognition
                        resized = cv2.resize(thresh, None, fx=1.5, fy=1.5, interpolation=cv2.INTER_CUBIC)

                        # OCR detection
                        result = ocr.readtext(resized, detail=0)
                        page_text = " ".join(result)

                        if page_text.strip():
                            print(f"🟡 OCR used (with preprocessing) on page {page_num} of {file_name}")
                        else:
                            print(f"⚠️ OCR failed to extract text on page {page_num}")

                    text += page_text + "\n"

        except Exception as e:
            print(f"❌ Error reading {file_name}: {e}")
            continue

        # 🧹 Cleaning and tokenizing
        cleaned = clean_text(text)
        if not cleaned.strip():
            print(f"⚠️ Skipping {file_name} (no readable Urdu/Arabic text found).")
            continue

        tokens = tokenize(cleaned)
        filtered = remove_stopwords(tokens)
        stemmed = [urdu_stemmer(t) for t in filtered]
        final_text = " ".join(stemmed)

        # 📝 Save processed file
        out_path = os.path.join(cleaned_folder, f"stemmed_{file_name[:-4]}.txt")
        with open(out_path, "w", encoding="utf-8") as fw:
            fw.write(final_text)

        records.append({"book": file_name, "text": final_text})
        print(f"✅ Saved cleaned: {out_path}")

    if not records:
        print("❌ No valid text extracted from any PDFs.")
        return pd.DataFrame()

    df = pd.DataFrame(records)
    df.to_csv(RAG_CSV, index=False, encoding="utf-8-sig")
    print(f"\n✅ Cleaned DataFrame saved → {RAG_CSV}")
    return df


        


# -----------------------
# Chunking
# -----------------------
def split_into_chunks(text, max_words=CHUNK_SIZE):
    if not isinstance(text, str):
        text = str(text) if text is not None else ""
    words = text.split()
    return [" ".join(words[i:i + max_words]) for i in range(0, len(words), max_words)]

def build_chunks_df(rag_df):
    print("🧩 Building text chunks...")
    # ✅ Clean NaN & empty rows
    rag_df = rag_df.dropna(subset=["text"])
    rag_df = rag_df[rag_df["text"].str.strip() != ""]
    rag_df.reset_index(drop=True, inplace=True)
    print(f"✅ Cleaned DataFrame, remaining rows: {len(rag_df)}")

    chunks = []
    for _, row in rag_df.iterrows():
        for chunk in split_into_chunks(row["text"], CHUNK_SIZE):
            if chunk.strip():
                chunks.append({"book": row["book"], "chunk": chunk})

    chunks_df = pd.DataFrame(chunks)
    chunks_df.to_csv(CHUNKS_CSV, index=False, encoding="utf-8-sig")
    print(f"✅ Created {len(chunks_df)} chunks → {CHUNKS_CSV}")
    return chunks_df

# -----------------------
# Embeddings + FAISS
# -----------------------
def build_or_load_faiss(chunks_df, model_name=EMBED_MODEL, index_path=FAISS_INDEX_PATH):
    model = SentenceTransformer(model_name)
    if os.path.exists(index_path):
        print("📂 Loading existing FAISS index:", index_path)
        try:
            index = faiss.read_index(index_path)
            if index.d != model.get_sentence_embedding_dimension():
                print("⚠️ FAISS dimension mismatch — rebuilding index.")
                raise ValueError("Dimension mismatch")
            return model, index
        except Exception:
            pass

    print("🧠 Encoding embeddings with", model_name)
    embeddings = model.encode(chunks_df["chunk"].tolist(), show_progress_bar=True)
    emb_np = np.array(embeddings, dtype="float32")
    faiss.normalize_L2(emb_np)
    d = emb_np.shape[1]
    index = faiss.IndexFlatL2(d)
    index.add(emb_np)
    faiss.write_index(index, index_path)
    print(f"✅ FAISS index built & saved: {index_path} | vectors: {index.ntotal}")
    return model, index

# -----------------------
# Query Search
# -----------------------
def search_query(query, model, index, chunks_df, top_k=TOP_K):
    q_emb = model.encode([query])
    q_np = np.array(q_emb, dtype="float32")
    faiss.normalize_L2(q_np)
    D, I = index.search(q_np, top_k)
    results = []
    for idx in I[0]:
        if idx < len(chunks_df):
            results.append({
                "idx": int(idx),
                "chunk": chunks_df.iloc[idx]["chunk"],
                "book": chunks_df.iloc[idx]["book"]
            })
    return results

# -----------------------
# GPT-4 Evaluation
# -----------------------
EVAL_SYSTEM_PROMPT = (
    "You are an expert Arabic/Urdu linguistic evaluator. "
    "Given a user query and retrieved context chunks, decide whether the context answers the query.\n\n"
    "Respond in this strict format (no extra text):\n"
    "LABEL: <Relevant and accurate | Partially relevant | Irrelevant or incorrect>\n"
    "REASON: <one-sentence reason in English or Arabic>\n"
)

def call_openai_evaluator(query, retrieved_chunks, retries=MAX_RETRIES):
    joined = "\n\n".join([f"Chunk {i+1} (from {c['book']}):\n{c['chunk']}" for i, c in enumerate(retrieved_chunks)])
    user_message = f"Query: {query}\n\nRetrieved context:\n{joined}\n\nQuestion: Do these chunks answer the query?"
    for attempt in range(retries):
        try:
            resp = client.chat.completions.create(
                model=LLM_MODEL,
                messages=[
                    {"role": "system", "content": EVAL_SYSTEM_PROMPT},
                    {"role": "user", "content": user_message}
                ],
                temperature=TEMPERATURE,
                max_tokens=200,
            )
            return resp.choices[0].message.content.strip()
        except Exception as e:
            wait = RETRY_WAIT * (attempt + 1)
            print(f"⚠️ OpenAI API error ({attempt+1}/{retries}): {e}. Retrying in {wait}s...")
            time.sleep(wait)
    raise RuntimeError("OpenAI evaluation failed after retries.")

# -----------------------
# Logging
# -----------------------
def log_evaluation(query, retrieved, evaluation_text, out_file=EVAL_LOG):
    record = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "query": query,
        "retrieved": retrieved,
        "evaluation": evaluation_text
    }
    with open(out_file, "a", encoding="utf-8") as fw:
        fw.write(json.dumps(record, ensure_ascii=False) + "\n")

# -----------------------
# Run Pipeline + Evaluate
# -----------------------
def run_pipeline_and_evaluate(sample_queries):
    if os.path.exists(RAG_CSV):
        rag_df = pd.read_csv(RAG_CSV, encoding="utf-8-sig")
    else:
        rag_df = process_pdfs()

    if rag_df.empty:
        print("⚠️ No data to process. Exiting.")
        return

    chunks_df = build_chunks_df(rag_df)
    model, index = build_or_load_faiss(chunks_df)

    for q in sample_queries:
        print(f"\n\n=== QUERY ===\n{q}\n")
        retrieved = search_query(q, model, index, chunks_df, top_k=TOP_K)
        for i, r in enumerate(retrieved, 1):
            print(f"\n--- Retrieved {i} (book: {r['book']}) ---\n{r['chunk'][:400]}...\n")
        eval_text = call_openai_evaluator(q, retrieved)
        print("EVALUATION:\n", eval_text)
        log_evaluation(q, retrieved, eval_text)

# -----------------------
# Main
# -----------------------
if __name__ == "__main__":
    sample_queries = [
        "علم اور ایمان کا تعلق",
        "صرف کا ماضی فعل"
    ]
    run_pipeline_and_evaluate(sample_queries)



