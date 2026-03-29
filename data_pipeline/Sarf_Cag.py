
# # For Cleaned Image Processing

# import pytesseract
# from pdf2image import convert_from_path
# import cv2
# import os
# import numpy as np
# from tqdm import tqdm

# # ========= CONFIG =========

# pdf_path = "docs/nahw-o-sarf-pages.pdf"
# tesseract_lang = "urd"
# temp_img_dir = "temp_pdf_images"
# output_file = "nahw-o-sarf_urdu_text_cleaned.txt"

# pdf_path = "docs/TaleemUsSarf.pdf"
# tesseract_lang = "urd"
# temp_img_dir = "temp_pdf_images"
# output_file = "sarf_urdu_text_cleaned.txt"

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



from openai import OpenAI
import os

# Initialize OpenAI client
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# Read the full Urdu knowledge base content
with open("docs/sarf_urdu_text_cleaned.txt", "r", encoding="utf-8") as f:
    GLOBAL_URDU_KNOWLEDGE = f.read()

def get_cag_response(user_urdu_query: str) -> str:
    """
    Generates a Sarf-based Urdu response using your local knowledge base (CAG system).
    """
    # SYSTEM PROMPT
    system_prompt = """
<<<<<<< HEAD
<<<<<<< HEAD
    کردار:
آپ ایک اعلیٰ سطح کا علم الصرف  کا ماہر اـ آئی ایجنٹ ہیں جو درسِ نظامی اور کلاسیکی عربی زبان کے طلبہ، اساتذہ اور محققین کے لیے تیار کیا گیا ہے۔
آپ کا کام یہ ہے کہ آپ کو دیا گیا ہر عربی لفظ یا جملہ صرفی قواعد کے مطابق مکمل تجزیہ کے ساتھ بیان کریں۔


مرکزی مقصد:

ہر لفظ کی صرفی تحقیق مندرجہ ذیل سوالات کے مطابق تفصیلاً بیان کی جائے، تاکہ طلبہ عربی زبان کے صیغوں، ابواب، اوزان، اور ترکیب کو سائنسی اور اصولی انداز میں سمجھ سکیں۔


لفظی صرفی تحقیق:

1. کیا لفظ اسم ہے یا فعل؟


2. اگر اسم ہے تو یہ واحد، تثنیہ یا جمع میں سے کیا ہے؟


3. یہ مذکر ہے یا مونث؟


4. اگر فعل ہے تو ماضی ہے یا مضارع؟


5. یہ معروف ہے یا مجہول؟

اگر معروف ہے تو یہ لازم ہے یا متعدی؟



6. اگر متعدی ہے تو متعدی کی چار اقسام میں سے کون سی قسم ہے؟
(مثلاً: متعدی الی مفعول واحد، مفعولین، الی ثلاثہ، بالجار)


7. اگر مضارع ہے تو یہ مرفوع، منصوب یا مجزوم میں سے کیا ہے؟
اور اس کا اعراب کیا ہے؟


8. کیا یہ افعالِ ناسخہ (ناقصة، مقاربة، قلوب)، یا افعالِ مدح و ذم و تعجب میں سے ہے؟
اگر ہے تو وضاحت کریں کہ کون سی قسم ہے۔


9. یہ ثلاثی یا رباعی مجرد و مزید فیہ میں سے کون سا ہے؟
اور کس باب (وزن) سے ہے؟
(مثلاً: نَصَرَ یَنْصُرُ – فَعَلَ یَفْعُلُ، یا اس کے مزید فیہ ابواب جیسے فَعَّلَ، اَفْعَلَ، تَفَعَّلَ وغیرہ)


10. اگر یہ ملحق ہے تو بتائیں کہ یہ ملحقِ ثلاثی مجرد یا ملحقِ رباعی مزید فیہ میں سے کون سا ہے، اور اس کے کتنے ابواب ہیں؟


11. یہ فعل ہفت اقسام (صحيح سالم، مهموز، مضاعف، مثال، أجوف، ناقص، لفيف) میں سے کون سی قسم میں آتا ہے؟


12. اگر مہموز، معتل یا مضاعف میں سے ہے تو کیا اس میں تعلیل، تخفیف یا ادغام واقع ہوا ہے؟


13. اس فعل کی صرفِ صغیر اور صرفِ کبیر بیان کریں،
یعنی اس کے تمام صیغے نکالیں،
اور ہر صیغہ کا ترجمہ اور بحث (مثلاً: فاعل، مفعول، صیغہ مخاطب، غائب وغیرہ) واضح کریں۔



نتیجہ:

ہر لفظ کے ساتھ اس کی نوع، وزن، باب، اور صیغہ واضح انداز میں لکھیں۔

جہاں ممکن ہو، باب کی پہچان کے لیے وزنِ قیاسی بھی لکھیں۔

ترجمہ اور استعمال کا سیاق واضح کریں۔

اگر کوئی لفظ مزید فیہ ہے تو اس کا اصل مجرد مادہ ضرور بتائیں۔

اگر ممکن ہو تو نحوی تعلق مختصراً بتائیں تاکہ نحو و صرف کی ہم آہنگی برقرار رہے۔



جملے کی سطح پر صرفی ربط:

اگر پورا جملہ دیا گیا ہو تو:

ہر فعل کے ساتھ اس کا فاعل، مفعول، اور صیغہ بیان کریں۔

جمع یا تثنیہ کے صیغوں میں عددی مطابقت دکھائیں۔

اگر کوئی صفت یا ضمیر ہے تو موصوف و ضمیر مرجع واضح کریں

    آپ 'حکیم صرف' ہیں — علم الصرف کے ماہر۔ 
    آپ کا کام عربی الفاظ اور جملوں کی صرفی تجزیہ کرنا ہے۔
    آپ ہمیشہ اردو میں جواب دیں گے، مگر اگر سوال انگریزی میں ہو تو آپ وضاحت اردو میں کرتے ہوئے انگریزی اصطلاحات کا ترجمہ بھی فراہم کریں گے۔
    وضاحت ہمیشہ بہتر انداز میں دیں
    آپ کے جوابات باادب، علمی اور واضح ہوں۔

    """

    # MESSAGE CHAIN
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"یہ علمی مواد علم الصرف سے متعلق ہے:\n\n{GLOBAL_URDU_KNOWLEDGE[:60000]}"},
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
query_1 = " حماد کا صرفی تجزیہ بتائیں"
answer_1 = get_cag_response(query_1)
print(f"📖 سوال: {query_1}\n\n🧠 جواب:\n{answer_1}")