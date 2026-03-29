
# from fastapi import FastAPI, Request
# from pydantic import BaseModel
# from typing import List

# app = FastAPI(title="Mock RAG API for Hikmah AI")

# # Request structure
# class RAGRequest(BaseModel):
#     lens: str
#     keywords: List[str]

# # Mock knowledge base
# mock_db = {
#     "sarf": "صرف عربی الفاظ کی ساخت اور صیغوں کی پہچان کا علم ہے۔",
#     "nahw": "نحو عربی جملوں کی ساخت اور الفاظ کے باہمی تعلق کا علم ہے۔",
#     "lugah": "لغہ عربی الفاظ کے معنی، مفہوم اور جڑوں کی تحقیق کا علم ہے۔",
#     "balagah": "بلاغہ زبان میں تاثیر، فصاحت اور بلاغت کے اصولوں کا علم ہے۔"
# }

# @app.post("/search")
# async def search_rag(data: RAGRequest):
#     lens = data.lens.lower()
#     context = mock_db.get(lens, "کوئی متعلقہ مواد نہیں ملا۔")

#     return {
#         "lens": lens,
#         "keywords": data.keywords,
#         "context": context,
#         "source": "Mock Knowledge Base",
#         "status": "success"
#     }

# @app.get("/")
# def root():
#     return {"message": "Mock RAG API is running!"}


"""
Hikmah AI — RAG ingestion + retrieval + LLM response pipeline
For Abdullah: stores Arabic-analyzed sentence records into Pinecone and
answers Urdu/Arabic user queries using RAG + LLM (final output in Urdu).

Requirements (install):
    pip install sentence-transformers pinecone-client openai pandas tqdm regex

Files & formats:
 - Recommended input: JSONL where each line is one JSON object with keys:
     {
       "sentence_ar": "الولدُ يكتبُ الدرسَ",
       "sarf": {...},         # optional dict or string (morphological analysis)
       "nahw": "...",         # syntactic analysis
       "lughat": "...",       # lexical meanings / urdu translations
       "balaghat": "...",     # rhetorical notes
       "source": "drive-file-1"   # provenance
     }
 - The loader will also accept CSV with columns: sentence_ar, sarf, nahw, lughat, balaghat
 - Or a plain TXT where blocks are separated by delim lines (simple parser included).

How to use:
  1. Populate YOUR_API_KEYS (Pinecone & OpenAI) or set env vars.
  2. Adjust INDEX_NAME and NAMESPACE if desired.
  3. Run `python hikmah_rag_pipeline.py` (or import functions into your n8n microservice).
"""

import os
import json
import re
from typing import List, Dict, Any, Optional
from pathlib import Path
from tqdm import tqdm

# # Embeddings
# from sentence_transformers import SentenceTransformer
# import numpy as np

# Pinecone
import pinecone
from pinecone import Pinecone, ServerlessSpec

# LLM (OpenAI)
import openai
from openai import OpenAI
# Optional: pandas for CSV loading
import pandas as pd

# ----------------------
# CONFIGURATION
# ----------------------
# Replace with your keys or set environment variables (preferred).
# ----------------------
# CONFIGURATION
# ----------------------
# Replace with your keys or set environment variables (preferred).
PINECONE_API_KEY = ("pcsk_6UNRFg_BA6fxWWDi9JVFwCCNBupK3tPPrqREbg6dmg87qo4UkiWuPDkwxYkNoqs6LpZL2x")
PINECONE_ENV = ("us-east-1")  # example
PINECONE_INDEX_NAME = ("db-for-5-lens-minilm") # <--- CHANGED for the new model
PINECONE_NAMESPACE = ("arabic_lenses")  # optional logical namespace

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
OPENAI_CHAT_MODEL = ("gpt-4o-mini")  # change if needed

# --- NEW EMBEDDING CONFIG ---
# We now use the OpenAI API instead of a local model
OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"
OPENAI_EMBEDDING_DIM = 1536 # 'text-embedding-3-small' has 1536 dimensions

# Chunking / RAG parameters
CHUNK_SIZE_TOKENS_APPROX = 400
TOP_K = 6
SIMILARITY_THRESHOLD = 0.55

pc = Pinecone(api_key=PINECONE_API_KEY)
print("Pinecone client initialized.")

# ----------------------
# UTIL: Arabic normalization
# ----------------------
def normalize_arabic(text: str) -> str:
    """
    Basic Arabic normalization to increase embedding/retrieval robustness.
    - Normalize different forms of Alef, remove tatweel, normalize Ya/AlefMaqsura, remove extra spaces.
    - We do NOT remove tashkeel (diacritics) by default; you can remove them if needed.
    """
    if text is None:
        return ""
    txt = text
    # Normalize Alef variants to bare Alef
    txt = re.sub(r"[إأآا]", "ا", txt)
    # Normalize Ya
    txt = re.sub(r"[يى]", "ي", txt)
    # Normalize Ta Marbuta to Ha? keep as is usually matters; optionally:
    # txt = re.sub(r"ة", "ه", txt)
    # Remove tatweel
    txt = re.sub(r"ـ+", "", txt)
    # Remove extra whitespace
    txt = re.sub(r"\s+", " ", txt).strip()
    return txt

# ----------------------
# Loader helpers
# ----------------------
def load_jsonl(path: str) -> List[Dict[str, Any]]:
    items = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                items.append(json.loads(line))
            except Exception as e:
                print("Skipping invalid JSON line:", e)
    return items

def load_csv(path: str) -> List[Dict[str, Any]]:
    df = pd.read_csv(path, dtype=str).fillna("")
    items = []
    for _, row in df.iterrows():
        items.append({
            "sentence_ar": row.get("sentence_ar", ""),
            "sarf": row.get("sarf", ""),
            "nahw": row.get("nahw", ""),
            "lughat": row.get("lughat", ""),
            "balaghat": row.get("balaghat", ""),
            "source": row.get("source", "")
        })
    return items

def load_plain_txt_blocks(path: str, block_delim="---") -> List[Dict[str, Any]]:
    """
    Very simple parser: split blocks by '---' and parse key: value lines.
    Each block should look like:
       sentence: ...
       sarf: ...
       nahw: ...
    """
    with open(path, "r", encoding="utf-8") as f:
        raw = f.read()
    blocks = raw.split(block_delim)
    items = []
    for b in blocks:
        lines = [l.strip() for l in b.strip().splitlines() if l.strip()]
        if not lines:
            continue
        record = {}
        for ln in lines:
            if ":" in ln:
                k, v = ln.split(":", 1)
                record[k.strip()] = v.strip()
        if "sentence" in record or "sentence_ar" in record:
            # normalize key names
            if "sentence" in record:
                record["sentence_ar"] = record.pop("sentence")
            items.append({
                "sentence_ar": record.get("sentence_ar", ""),
                "sarf": record.get("sarf", ""),
                "nahw": record.get("nahw", ""),
                "lughat": record.get("lughat", ""),
                "balaghat": record.get("balaghat", ""),
                "source": record.get("source", "local_txt")
            })
    return items

# ----------------------
# Prepare records for embedding
# ----------------------
def prepare_records(raw_items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Each record will become one vector DB item.
    We create a `text_for_embedding` field that combines Arabic sentence + short Arabic analysis,
    but preserve structured fields in metadata so we can return them to LLM.
    """
    records = []
    for i, it in enumerate(raw_items):
        sent_ar = it.get("sentence_ar") or it.get("sentence") or ""
        sent_ar = normalize_arabic(sent_ar)
        # build compact textual witness for embeddings (prefer Arabic-first)
        parts = [sent_ar]
        # Include lens pieces so embedding captures morphological/syntactic words as text
        for lens_field in ("sarf", "nahw", "lughat", "balaghat"):
            val = it.get(lens_field)
            if val:
                # prefer Arabic strings; if the analysis is in Urdu, include both Arabic + Urdu markers.
                parts.append(str(val))
        text_for_embedding = " ||| ".join([p for p in parts if p])
        metadata = {
            "sentence_ar": sent_ar,
            "sarf": it.get("sarf", ""),
            "nahw": it.get("nahw", ""),
            "lughat": it.get("lughat", ""),
            "balaghat": it.get("balaghat", ""),
            "source": it.get("source", ""),
            "id": f"rec_{i}"
        }
        records.append({
            "id": metadata["id"],
            "text": text_for_embedding,
            "metadata": metadata
        })
    return records

# ----------------------
# Embeddings: initialize SentenceTransformer
# ----------------------
# def init_embedding_model(model_name: str = EMBEDDING_MODEL_NAME):
#     print("Loading embedding model:", model_name)
#     model = SentenceTransformer(model_name)
#     return model

# def embed_texts(model: SentenceTransformer, texts: List[str]) -> List[List[float]]:
#     """
#     Returns list of vectors (float32 lists).
#     We convert to Python lists for Pinecone.
#     """
#     embs = model.encode(texts, show_progress_bar=True, convert_to_numpy=True)
#     # Normalize vectors (helps cosine similarity if DB uses dot product)
#     # SentenceTransformer returns non-normalized vectors; keep as-is, but normalize now:
#     norms = np.linalg.norm(embs, axis=1, keepdims=True)
#     norms[norms == 0] = 1.0
#     embs = embs / norms
#     return embs.astype(np.float32).tolist()

def embed_texts_openai(texts: List[str], model: str = OPENAI_EMBEDDING_MODEL) -> List[List[float]]:
    """
    Embeds a list of texts using the OpenAI API.
    """
    if not texts:
        return []

    print(f"Embedding {len(texts)} texts using OpenAI model: {model}...")
    
    # OpenAI recommends replacing newlines for better performance
    texts_cleaned = [t.replace("\n", " ") for t in texts]

    try:
        # Call the OpenAI embeddings API
        response = client.embeddings.create(input=texts_cleaned, model=model)
        
        # Extract the embeddings from the response
        embeddings = [item.embedding for item in response.data]
        print("Embedding complete.")
        return embeddings
    except Exception as e:
        print(f"Error calling OpenAI embedding API: {e}")
        return []



from pinecone import Pinecone
def ensure_index(index_name: str = PINECONE_INDEX_NAME, dimension: int = OPENAI_EMBEDDING_DIM):
    """
    Create index if not exists using the new Pinecone client.
    """
    # Check if index already exists
    if index_name in pc.list_indexes().names():
        print(f"Pinecone index `{index_name}` already exists.")
        return

    # Create the index
    print(f"Creating Pinecone index `{index_name}` with dim={dimension}...")
    pc.create_index(
        name=index_name,
        dimension=dimension,
        metric="cosine",  # 'cosine' is standard for sentence embeddings
        spec=ServerlessSpec(
            cloud='aws',
            region=PINECONE_ENV  # Use your PINECONE_ENV variable here
        )
    )
    print(f"Created Pinecone index `{index_name}`.")

def upsert_records_to_pinecone(records: List[Dict[str, Any]], embeddings: List[List[float]],
                               index_name: str = PINECONE_INDEX_NAME, namespace: Optional[str] = PINECONE_NAMESPACE):
    idx = pc.Index(index_name)
    to_upsert = []
    for rec, emb in zip(records, embeddings):
        # Pinecone upsert expects: (id, vector, metadata)
        to_upsert.append((rec["id"], emb, rec["metadata"]))
    # Upsert in batches
    BATCH = 100
    for i in range(0, len(to_upsert), BATCH):
        batch = to_upsert[i:i+BATCH]
        idx.upsert(vectors=batch, namespace=namespace)
        print(f"Upserted batch {i}..{i+len(batch)} to Pinecone (ns={namespace})")

# ----------------------
# Retrieval
# ----------------------
def retrieve_by_query(query: str, index_name: str = PINECONE_INDEX_NAME,
                      namespace: Optional[str] = PINECONE_NAMESPACE, top_k: int = TOP_K, filter_lens: Optional[List[str]] = None):
    """
    Embed the query (Urdu or Arabic) using the OpenAI API, then query Pinecone.
    ...
    """
    query_norm = query.strip().replace("\n", " ")
    
    # Call OpenAI API for the single query
    try:
        response = client.embeddings.create(input=[query_norm], model=OPENAI_EMBEDDING_MODEL)
        q_vec = response.data[0].embedding
    except Exception as e:
        print(f"Error embedding query: {e}")
        return []

    # OpenAI embeddings are pre-normalized, no manual normalization needed.

    idx = pc.Index(index_name)
    # Query pinecone
    resp = idx.query(vector=q_vec, top_k=top_k*3, namespace=namespace, include_metadata=True, include_values=False)
    
    # ... (rest of the function is the same) ...
    filtered = []
    for match in resp.matches:
        md = match.metadata or {}
        score = float(match.score) if hasattr(match, "score") else None
        # compute simple similarity threshold (Pinecone returns cosine -> 0..1)
        if score is not None and score < SIMILARITY_THRESHOLD:
            continue
        if filter_lens:
            ok = False
            for lens in filter_lens:
                if md.get(lens):
                    ok = True
                    break
            if not ok:
                continue
        filtered.append({
            "id": match.id,
            "score": score,
            "metadata": md
        })
        if len(filtered) >= top_k:
            break
    return filtered

# ----------------------
# LLM: fuse context + user query -> Urdu response
# ----------------------
def build_prompt_for_llm(user_query_urdu: str, user_sentence_ar: Optional[str], retrieved_contexts: List[Dict[str, Any]], active_lens: List[str]) -> str:
    """
    Assemble a clear prompt for the LLM:
     - system instruction describing Hikmah AI and output language (Urdu)
     - lens activation header
     - include retrieved contexts (labelled)
     - user's Urdu query and Arabic sentence (if provided)
     - ask LLM to produce concise analysis in simple Urdu, cite evidence by record id.
    """
    system_instruction = (
        "آپ Hikmah AI کے عربی لسانی تجزیہ کار ہیں۔\n"
        "صارف کا سوال اردو/عربی میں ہوگا۔ جواب **سادہ اردو** میں دیں، مختصر اور واضح۔\n"
        "آپ کو صرف فعال لینس(س) کے مطابق تجزیہ کرنا ہے: SARF, NAHW, LUGHAT, BALAGHAT۔\n"
        "اگر ثبوت استعمال کریں تو ہر دعوے کے ساتھ حوالہ دیں: [id: rec_x]\n"
        "اگر آپ کو کوئی شکوک ہو تو 'ممکنہ متبادل' لکھیں۔\n\n"
    )
    lens_header = f"فعال لینس: {', '.join(active_lens)}\n\n"
    ctx_blocks = []
    for i, c in enumerate(retrieved_contexts):
        md = c.get("metadata", {})
        block = (
            f"--- CONTEXT {i+1} (id={c.get('id')}, score={c.get('score')}) ---\n"
            f"sentence_ar: {md.get('sentence_ar')}\n"
            f"sarf: {md.get('sarf')}\n"
            f"nahw: {md.get('nahw')}\n"
            f"lughat: {md.get('lughat')}\n"
            f"balaghat: {md.get('balaghat')}\n"
            f"source: {md.get('source')}\n\n"
        )
        ctx_blocks.append(block)
    ctx_text = "\n".join(ctx_blocks) if ctx_blocks else "کوئی متعلقہ حوالہ نہیں ملا۔\n"

    user_part = f"صارف کا سوال (اردو): {user_query_urdu}\n"
    if user_sentence_ar:
        user_part += f"صارف کا عربی جملہ: {user_sentence_ar}\n"

    instructions = (
        "\nہدایات:\n"
        "1) ہر لینس کے لئے الگ حصہ لکھیں (مثلاً: صرف، نحو، لغت، بلاغت)۔\n"
        "2) ہر دعوے کے ساتھ حوالہ دیں (مثلاً: [id: rec_12]) جب آپ حوالہ استعمال کریں۔\n"
        "3) جواب سادہ اور اردو میں ہو، ہر حصہ 2-5 جملوں تک محدود رکھیں۔\n"
        "4) اگر کوئی بات غیر یقینی ہو تو 'ممکنہ متبادل' دکھائیں۔\n"
    )

    prompt = system_instruction + lens_header + ctx_text + "\n" + user_part + instructions
    return prompt

def call_openai_chat(prompt: str, model: str = OPENAI_CHAT_MODEL, max_tokens: int = 400, temperature: float = 0.2) -> str:
    """
    Call OpenAI ChatCompletion (or similar). Uses messages format.
    """
    openai.api_key = OPENAI_API_KEY
    messages = [
        {"role": "system", "content": "You are an assistant for Arabic linguistic analysis. Output in Urdu."},
        {"role": "user", "content": prompt}
    ]
    resp = client.chat.completions.create(
        model=model,
        messages=messages,
        max_tokens=max_tokens,
        temperature=temperature
    )
    # Safety: check shape
    try:
        out = resp["choices"][0]["message"]["content"].strip()
    except Exception:
        out = str(resp)
    return out

# ----------------------
# End-to-end convenience functions
# ----------------------
def ingest_local_file_to_pinecone(local_path: str, pine_index_name: str = PINECONE_INDEX_NAME, namespace: str = PINECONE_NAMESPACE):
    """
    Loads a local file (jsonl/csv/txt), prepares records, computes embeddings, and upserts to Pinecone.
    """
    p = Path(local_path)
    if not p.exists():
        raise FileNotFoundError(local_path)
    suffix = p.suffix.lower()
    if suffix == ".jsonl" or suffix == ".json":
        raw_items = load_jsonl(local_path)
    elif suffix == ".csv":
        raw_items = load_csv(local_path)
    else:
        # treat as plain text blocks
        raw_items = load_plain_txt_blocks(local_path, block_delim="---")
    print(f"Loaded {len(raw_items)} raw items from {local_path}")

    records = prepare_records(raw_items)
    texts = [r["text"] for r in records]
    print(f"Embedding {len(texts)} records ...")
    embs = embed_texts_openai(texts, model=OPENAI_EMBEDDING_MODEL)
    print("Upserting to Pinecone ...")
    upsert_records_to_pinecone(records, embs, index_name=pine_index_name, namespace=namespace)
    print("Ingestion complete.")

def answer_user_query(user_query_urdu: str, user_sentence_ar: Optional[str], active_lens: List[str], index_name: str = PINECONE_INDEX_NAME, namespace: str = PINECONE_NAMESPACE):
    """
    Main runtime call from your n8n / webhook:
      - embed user_query_urdu (or user_sentence_ar if preferred)
      - retrieve relevant contexts filtered by lens
      - build prompt and call LLM to get final Urdu explanation
    """
    # Decide query text to embed: prefer Arabic sentence if provided, else Urdu query
    query_text = user_sentence_ar.strip() if user_sentence_ar else user_query_urdu.strip()
    # Normalize if Arabic
    if user_sentence_ar:
        query_text = normalize_arabic(query_text)

    # Retrieve top contexts; we prefer to request results that contain the lens info
    retrieved = retrieved = retrieve_by_query(query_text, index_name=index_name, namespace=namespace, top_k=TOP_K, filter_lens=active_lens)
    if not retrieved:
        # fallback: broaden search without lens filter
        retrieved = retrieve_by_query(query_text, index_name=index_name, namespace=namespace, top_k=TOP_K, filter_lens=None)

    prompt = build_prompt_for_llm(user_query_urdu, user_sentence_ar, retrieved, active_lens)
    llm_out = call_openai_chat(prompt, model=OPENAI_CHAT_MODEL)
    return llm_out, retrieved

# ----------------------
# Main runnable example
# ----------------------
if __name__ == "__main__":
    # === Step 0: Configuration checks ===
    if PINECONE_API_KEY.startswith("pcsk_") and not OPENAI_API_KEY:
        print("⚠️  You must set your OPENAI_API_KEY environment variable.")
        # exit()
    
    # === Step 1: init embedding model ===
    # NO LONGER NEEDED! We use the API.
    print("Using OpenAI API for embeddings. No local model to load.")

    # === Step 2: init pinecone & index (run this once) ===
    # The 'pc' client is already initialized globally at the top
    
    # We use the hardcoded dimension from our config
    print(f"Ensuring index '{PINECONE_INDEX_NAME}' with dimension {OPENAI_EMBEDDING_DIM}")
    ensure_index(PINECONE_INDEX_NAME, dimension=OPENAI_EMBEDDING_DIM)
    
    # === Step 3: Ingest local file (only run once or when updating data) ===
    # Put your local file path here.
    LOCAL_FILE_PATH = "E:\Hikmah AI\Hikmah_AI\docs\12-pages.json"  # change to your file
    if Path(LOCAL_FILE_PATH).exists():
        # Note: 'embed_model' is no longer passed in
        ingest_local_file_to_pinecone(LOCAL_FILE_PATH,
                                      pine_index_name=PINECONE_INDEX_NAME, namespace=PINECONE_NAMESPACE)
    else:
        print(f"Local file not found at {LOCAL_FILE_PATH}. Skipping ingestion step.")

    # === Step 4: Example of answering a user query (simulate webhook run) ===
    user_query_urdu = " کے معنی اور اس کے مشتقات کے بارے میں بتائیں۔"
    user_sentence_ar = "الرجیم"
    active_lens = ["sarf", "nahw"]

    print("\n--- Running retrieval & LLM generation (using OpenAI Embeddings) ---")
    # Note: 'embed_model' is no longer passed in
    answer_text, contexts = answer_user_query(user_query_urdu, user_sentence_ar, active_lens,
                                              index_name=PINECONE_INDEX_NAME, namespace=PINECONE_NAMESPACE)
    
    print("\n=== LLM Answer (Urdu) ===\n")
    print(answer_text)
    print("\n=== Retrieved Context Summaries ===\n")
    if contexts:
        for c in contexts:
            print(c["id"], "| score:", c.get("score"), "| sentence_ar:", c.get("metadata", {}).get("sentence_ar"))
    else:
        print("No contexts were retrieved.")