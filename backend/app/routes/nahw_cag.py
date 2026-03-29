
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from openai import OpenAI
import os

router = APIRouter()

# ✅ Load OpenAI API Key
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# with open("../docs/nahw-o-sarf_urdu_text_cleaned.txt", "r", encoding="utf-8") as f:
#     GLOBAL_URDU_KNOWLEDGE = f.read()


# ✅ Load the Urdu Knowledge Base
# KB_PATH = GLOBAL_URDU_KNOWLEDGE

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
    آپ ایک اعلیٰ سطح کا علم النحو (Arabic Syntax) کا ماہر AI ایجنٹ ہیں جو درسِ نظامی اور کلاسیکی عربی زبان کے طلبہ و محققین کی مدد کے لیے تیار کیا گیا ہے۔
    آپ کا بنیادی کام عربی الفاظ اور جملوں کی مکمل نحوی (Syntactic) تحقیق و تشریح کرنا ہے، بالکل اسی اصولی و مدرساتی طرز پر جسے قدیم نحواء نے بیان کیا ہے۔



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
    """

    # MESSAGE CHAIN
    messages = [
        {"role": "system", "content": system_prompt},
        # {"role": "user", "content": f"یہ علمی مواد علم النحو و صرف سے متعلق ہے:\n\n{GLOBAL_URDU_KNOWLEDGE[:60000]}"},
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

# ✅ API Endpoint
@router.post("/ask")
async def ask_sarf(query: SarfQuery):
    """
    Send a question to the Nahw CAG System and get a scholarly Urdu answer.
    """
    if not query.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty.")
    
    response = get_cag_response(query.question)
    return {"question": query.question, "answer": response}