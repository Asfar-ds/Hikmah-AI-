

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
class NahwQuery(BaseModel):
    question: str  # User query in Urdu or English

# ✅ Function to get GPT-4o response
def get_cag_response(user_urdu_query: str) -> str:
    """
    Generates a Sarf-based Urdu response using your local knowledge base (CAG system).
    """
    # SYSTEM PROMPT
    system_prompt = """
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
async def ask_sarf(query: NahwQuery):
    """
    Send a question to the Sarf CAG System and get a scholarly Urdu answer.
    """
    if not query.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty.")
    
    response = get_cag_response(query.question)
    return {"question": query.question, "answer": response}