

# If pdf contain images then run this script.

# import os
# from pdf2image import convert_from_path
# import pytesseract
# pytesseract.pytesseract.tesseract_cmd = r"C:\Users\star\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"
# import tiktoken
# from tqdm import tqdm

# # ===========
# # CONFIG
# # ===========
# pdf_path = "E:\Hikmah-AI\Hikmah_AI\docs\TaleemUnNahw.pdf"   # Path to your Urdu PDF
# tesseract_lang = "urd"               # Urdu language code
# temp_img_dir = "temp_pdf_images"     # Temporary folder for page images

# # ===========
# # STEP 1: Convert PDF pages to images
# # ===========
# os.makedirs(temp_img_dir, exist_ok=True)
# print("📄 Converting PDF pages to images...")
# pages = convert_from_path(pdf_path, dpi=300)

# # ===========
# # STEP 2: Extract Urdu text using Tesseract OCR
# # ===========
# print("🔍 Extracting Urdu text using OCR...")
# urdu_text = ""

# for i, page in enumerate(tqdm(pages, desc="Processing pages")):
#     img_path = os.path.join(temp_img_dir, f"page_{i+1}.png")
#     page.save(img_path, "PNG")

#     # Extract text with pytesseract
#     text = pytesseract.image_to_string(img_path, lang=tesseract_lang)
#     urdu_text += text + "\n"

# # ===========
# # STEP 3: Count tokens using tiktoken (GPT-4o encoder)
# # ===========
# print("🧮 Counting tokens with tiktoken...")

# encoding = tiktoken.encoding_for_model("gpt-4o")
# token_count = len(encoding.encode(urdu_text))

# print(f"\n📘 Urdu document contains approximately {token_count:,} tokens.")

# if token_count > 128000:
#     print("⚠️ WARNING: Text exceeds GPT-4o’s 128,000 token context limit.")
# else:
#     print("✅ Text fits within GPT-4o’s 128,000 token context window.")

# # ===========
# # (Optional) Cleanup temporary images
# # ===========
# import shutil
# shutil.rmtree(temp_img_dir)
# print("🧹 Temporary files cleaned up.")

# with open("nahw_urdu_text.txt", "w", encoding="utf-8") as f:
#     f.write(urdu_text)


# For Cleaned Image Processing

# import pytesseract
# from pdf2image import convert_from_path
# import cv2
# import os
# import numpy as np
# from tqdm import tqdm

# # ========= CONFIG =========
# pdf_path = "docs/TaleemUnNahw.pdf"
# tesseract_lang = "urd"
# temp_img_dir = "temp_pdf_images"
# output_file = "nahw_urdu_text_cleaned.txt"
# dpi = 300  # Use 300 instead of 400 to save memory

# os.makedirs(temp_img_dir, exist_ok=True)
# pytesseract.pytesseract.tesseract_cmd = r"C:\Users\star\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"

# urdu_text = ""

# # ========= PROCESS PAGE BY PAGE =========
# print("📄 Converting and processing each page safely...")

# from pdf2image.pdf2image import pdfinfo_from_path

# pdf_info = pdfinfo_from_path(pdf_path)
# total_pages = pdf_info["Pages"]

# for page_number in tqdm(range(1, total_pages + 1), desc="Processing PDF pages"):
#     # Convert one page at a time
#     images = convert_from_path(pdf_path, dpi=dpi, first_page=page_number, last_page=page_number)
#     page = images[0]
    
#     img_path = os.path.join(temp_img_dir, f"page_{page_number}.png")
#     page.save(img_path, "PNG")

#     # Preprocess image for clearer OCR
#     img = cv2.imread(img_path)
#     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#     gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
#     gray = cv2.medianBlur(gray, 3)
#     cv2.imwrite(img_path, gray)

#     # Urdu OCR
#     text = pytesseract.image_to_string(img_path, lang=tesseract_lang, config="--psm 6")
#     urdu_text += f"\n\n📄 صفحہ {page_number}:\n{text.strip()}\n"

#     # Cleanup this page image to free RAM
#     os.remove(img_path)

# # ========= SAVE CLEAN OCR TEXT =========
# with open(output_file, "w", encoding="utf-8") as f:
#     f.write(urdu_text)

# print(f"\n✅ Urdu OCR completed successfully! Saved as '{output_file}'.")


# enhacing text for best Cag performance

# import re

# # Load OCR Urdu text
# with open("docs/nahw_urdu_text_cleaned.txt", "r", encoding="utf-8") as f:
#     text = f.read()

# # Clean text (remove Latin artifacts)
# text = re.sub(r'[^\u0600-\u06FF\s\.\،\:\؛\؟\(\)\-]+', '', text)
# text = re.sub(r'\s+', ' ', text).strip()

# # Split by key Urdu words that indicate new topics
# sections = re.split(r'(?:باب|سبق|موضوع|فصل)\s*', text)

# structured_sections = []
# for i, sec in enumerate(sections):
#     sec = sec.strip()
#     if sec:
#         structured_sections.append(f"🟢 حصہ {i+1}:\n{sec}\n")

# # Save structured output
# with open("nahw_urdu_text_structured.txt", "w", encoding="utf-8") as f:
#     f.write("\n".join(structured_sections))

# print("✅ Structured Urdu text saved successfully as 'nahw_urdu_text_structured.txt'")


# Generate Embeddings (Knowledge Representation)

# from openai import OpenAI
# import json, os

# OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
# client = OpenAI(api_key=OPENAI_API_KEY)

# embeddings = []

# for i, filename in enumerate(sorted(os.listdir("chunks"))):
#     with open(f"chunks/{filename}", "r", encoding="utf-8") as f:
#         content = f.read()

#     response = client.embeddings.create(
#         model="text-embedding-3-large",  # multilingual-friendly
#         input=content
#     )

#     vector = response.data[0].embedding
#     embeddings.append({"id": filename, "embedding": vector})

# # Save all embeddings
# with open("docs/embeddings/nahw_embeddings.json", "w", encoding="utf-8") as f:
#     json.dump(embeddings, f)

# print("✅ Urdu embeddings saved successfully!")

# Call OpenAI API
from openai import OpenAI
import os
from pydantic import BaseModel
# router = APIRouter()

# ✅ Load OpenAI API Key
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

with open("./docs/nahw-o-sarf_urdu_text_cleaned.txt", "r", encoding="utf-8") as f:
    GLOBAL_URDU_KNOWLEDGE = f.read()


# ✅ Load the Urdu Knowledge Base
KB_PATH = GLOBAL_URDU_KNOWLEDGE

# try:
#     with open(KB_PATH, "r", encoding="utf-8") as f:
#         URDU_KNOWLEDGE = f.read()[:60000]  # Keep under token limits
# except FileNotFoundError:
#     raise RuntimeError(f"❌ Urdu knowledge base not found at {KB_PATH}")

# ✅ Define request schema
class SarfQuery(BaseModel):
    question: str  # User query in Urdu or English

# ✅ Function to get GPT-4o response
def get_cag_response(user_urdu_query: str) -> str:
    """
    Generates a Sarf-based Urdu response using your local knowledge base (CAG system).
    """
    # SYSTEM PROMPT
    system_prompt = """
     کردار (Role):
    آپ ایک اعلیٰ سطح کا علم النحو کا ماہر  ایجنٹ ہیں جو درسِ نظامی اور کلاسیکی عربی زبان کے طلبہ و محققین کی مدد کے لیے تیار کیا گیا ہے۔
    آپ کا بنیادی کام عربی الفاظ اور جملوں کی مکمل نحوی  تحقیق و تشریح کرنا ہے، بالکل اسی اصولی و مدرساتی طرز پر جسے قدیم نحواء نے بیان کیا ہے۔



مرکزی مقصد:

آپ کو دیا گیا ہر عربی لفظ یا جملہ نحوی تحقیق کے مندرجہ ذیل اصولوں کے مطابق مکمل طور پر تجزیہ کیا جائے، اور آخر میں پورے جملے کی ترکیب اور اردو ترجمہ فراہم کیا جائے۔



لفظی (Word-Level) نحوی تحقیق:

1. اگر اسم ہے تو اس کی علامتِ اسم کیا ہے؟


2. اگر فعل ہے تو اس کی علامتِ فعل کیا ہے؟


3. یہ معرب ہے یا مبنی؟


4. اگر معرب ہے تو منصرف ہے یا غیر منصرف؟ اگر غیر منصرف ہے تو اس کے دو اسباب کیا ہیں؟


5. اسم غیر متمکن کی کتنی قسمیں ہیں؟ اور یہ کس قسم میں سے ہے؟


6. یہ معرفہ ہے یا نکرہ؟ اگر معرفہ ہے تو معرفہ کی کون سی قسم (علم، ضمیر، اسمِ اشارہ، اسمِ موصول، معرف باللام، مضاف الی المعرفہ) ہے؟


7. یہ مذکر ہے یا مونث؟


8. یہ واحد، تثنیہ یا جمع میں سے کیا ہے؟


9. اگر جمع ہے تو جمعِ قلت ہے یا جمعِ کثرت؟ سالم ہے یا مکسر؟


10. اسم متمکن کی سولہ اقسام میں سے کون سی ہے، اور اس کا اعراب کیا ہے؟


11. کیا یہ اسمائے عاملہ میں سے ہے؟ اگر ہے تو کون سی قسم ہے؟


12. کیا یہ توابع میں سے ہے؟ اگر ہے تو کون سا تابع (نعت، تاکید، عطف، بدل) ہے؟


13. اگر معرب ہے تو یہ مرفوع، منصوب یا مجرور میں سے کیا ہے؟ اور اس کا عامل کیا ہے؟



جملے کی ترکیب (Sentence-Level Analysis):

ہر دو الفاظ کے باہمی تعلق کی نوعیت واضح کرو:

فعل و فاعل

مبتداء و خبر

موصوف و صفت

مضاف و مضاف الیہ

حال و ذو الحال

مستثنی و مستثنی منہ

ممیز و تمیز

عامل و معمول


Grammatical Rule پھر ہر تعلق کے حکم کی وضاحت کرو۔



جملے کی درجہ بندی (Sentence Classification):

آخر میں ان سوالات کے جوابات دو:

1. کیا عبارت مرکب مفید ہے یا مرکب غیر مفید؟


2. اگر مرکب مفید ہے تو وہ جملہ اسمیہ، جملہ فعلیہ، جملہ شرطیہ یا جملہ ظرفیہ میں سے کیا ہے؟


3. کیا یہ جملہ خبریہ ہے یا انشائیہ؟


4. اگر مرکب غیر مفید ہے تو وہ تین اقسام میں سے کس میں داخل ہے؟

اگر جملے میں کوئی حرف ہو تو اس کے لیے:

1. اس کی علامتِ حرف کیا ہے؟

2. یہ مبنی ہے یا معرب؟

3. کیا یہ حروفِ عاملہ میں سے ہے یا غیر عاملہ میں سے؟

اگر عاملہ ہے تو یہ اسم پر عمل کرتا ہے یا فعل پر؟

اگر غیر عاملہ ہے تو حروفِ معانی کی کس قسم (حرفِ عطف، استثناء، شرط، ایجاب وغیرہ) سے ہے؟

4. اگر عاملہ ہے تو کیا یہ عامل دراسم ہے یا عامل درفعل؟

5. اگر عامل دراسم ہے تو اس کی پانچ یا سات اقسام میں سے کون سی ہے؟

6. اگر یہ فعلِ مضارع پر داخل ہے تو ناصب ہے یا جازم؟

7. اگر غیر عاملہ ہے تو اس کا معنی یا استعمال کیا ہے؟

8. حروفِ معانی کتنے ہیں اور یہ کس معنی کے لیے استعمال ہوا ہے؟


نتیجہ (Output Requirements):

تحقیق کو واضح اور منظم انداز میں درجہ وار (Structured Format) میں پیش کریں۔

ہر لفظ کے بعد مکمل نحوی تشریح لکھیں۔

آخر میں پورے جملے کا اردو ترجمہ اور نحوی قاعدہ بیان کریں۔

جہاں ممکن ہو، علم الصرف اور بلاغت سے متعلق پہلوؤں کا بھی ربط مختصراً ذکر کریں۔

    آپ 'حکیم نحو' ہیں — علم النحو کے ماہر۔ 
    آپ کا کام عربی الفاظ اور جملوں کا نحوی تجزیہ کرنا ہے۔
    آپ ہمیشہ اردو میں جواب دیں گے، مگر اگر سوال انگریزی میں ہو تو آپ وضاحت اردو میں کرتے ہوئے انگریزی اصطلاحات کا ترجمہ بھی فراہم کریں گے۔
    وضاحت ہمیشہ درج ذیل انداز میں دیں:
    🔹 تعریف:  
    🔹 مثال:  
    🔹 نوٹ:
    آپ کے جوابات باادب، علمی اور واضح ہوں۔

    """

    # MESSAGE CHAIN
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"یہ علمی مواد علم النحو و صرف سے متعلق ہے:\n\n{GLOBAL_URDU_KNOWLEDGE[:60000]}"},
        {"role": "user", "content": f"صارف کا سوال: {user_urdu_query}"}
    ]

    # API CALL
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            temperature=0.1,
            max_tokens=1024
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"⚠️ API Error: {e}"

# 🧪 Test Query
query_1 =  "اس ایت کی نحوی ترکیب بیان کرو إِيَّاكَ نَعْبُدُ وَإِيَّاكَ نَسْتَعِينُ"
answer_1 = get_cag_response(query_1)
print(f"📖 سوال: {query_1}\n\n🧠 جواب:\n{answer_1}")
