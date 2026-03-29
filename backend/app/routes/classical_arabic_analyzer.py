
import os
from openai import OpenAI
# We will use a specialized library for Arabic NLP.
# It's better equipped to handle morphology (Sarf) and grammar (Nahw).
import pyarabic.araby as araby

from fastapi import APIRouter, HTTPException

from ..models.schema import ArabicTextQuery


from groq import Groq

client = Groq(api_key=os.environ.get("OPENAI_API_KEY"))


# 1. Instantiate the router
router = APIRouter()


# Initialize the OpenAI client
# client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def analyze_classical_arabic_text(text: str, language: str):
    """
    Analyzes a classical Arabic text through the four lenses (Sarf, Nahw, Lughat, Balagah)
    and generates an explanation in the specified language.
    """

    # --- Step 1: Perform Initial Linguistic Analysis (Sarf & Nahw) ---
    # This is a simplified example. A real implementation would involve more advanced analysis.
    tokens = araby.tokenize(text)
    analysis_results = [f"Token: {token}" for token in tokens]
    structured_analysis = "\n".join(analysis_results)

    # --- Step 2: Build a Structured, Language-Specific Prompt for the LLM ---
    
    # Define lens names and instructions based on the requested language
    if language.lower() == 'urdu':
        lens_names = {
            "lughat": "لغت (Lexicology)",
            "irab": "إعراب (Syntax)",
            "sarf": "صرف (Morphology)",
            "balagah": "بلاغت (Rhetoric)",
            "fawaid": "فوائد (Benefits)"
        }
        language_instruction = "The response MUST be in Urdu."
    else:  # Default to English
        lens_names = {
            "lughat": "Lughat (Lexicology)",
            "irab": "I'rab (Syntax)",
            "sarf": "Sarf (Morphology)",
            "balagah": "Balagah (Rhetoric)",
            "fawaid": "Fawa'id (Benefits)"
        }
        language_instruction = "The response MUST be in English."

    system_prompt = f"""
You are an expert in classical Arabic linguistics, specializing in Sarf, Nahw, Lughat, and Balagah.
Your task is to explain a given Arabic text to a student.
You will be given a pre-computed linguistic analysis of the text.
Use this analysis to generate a comprehensive explanation covering the specified lenses.
{language_instruction}

**Linguistic Analysis Results:**
{structured_analysis}
"""

    user_prompt = f"""
Based on the provided linguistic analysis, please provide a detailed explanation for the following Arabic text: "{text}"

Explain it using the following lenses:
1.  **{lens_names['lughat']}:** (Provide word meanings, context, and etymology. For example, for 'al-nas', discuss its origin from 'an-nawas' or 'al-ins'.)
2.  **{lens_names['irab']}:** (Explain the grammatical roles of words, i'rab. Be detailed. For example: 'wa min an-nasi' - 'The waw is for resumption (isti'nafiyyah), the جار ومجرور is related to a deleted introductory predicate (khabar muqaddam)...'.)
3.  **{lens_names['sarf']}:** (Provide a word-by-word breakdown. For each word, specify its root, form, and any other relevant morphological details. For example: '﴿خَتَمَ﴾ فعل ماض ثلاثي مجرد، من مادّة (ختم)، غائب، مذكر، مفرد.')
4.  **{lens_names['balagah']}:** (Identify and explain any rhetorical devices, such as majaz, istiaarah, tashbih, etc. For example, explain the rhetorical device in 'khatama Allahu ala qulubihim'.)
5.  **{lens_names['fawaid']}:** (Include any additional interesting points or benefits, such as why a word is singular or plural, or why a particular grammatical structure is used.)
"""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]

    # --- Step 3: Call the OpenAI API for Explanation Generation ---
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"Error: {str(e)}"

# if __name__ == '__main__':
#     # Test the analyzer with a sample text
#     arabic_text = "بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ"
    
#     print("--- Running English Analysis ---")
    # explanation_en = analyze_classical_arabic_text(arabic_text, language="English")
    # print(f"Analysis for: '{arabic_text}'\n")
    # print(explanation_en)
    
    # print("\n" + "="*50 + "\n")
    
    # print("--- Running Urdu Analysis ---")
    # explanation_ur = analyze_classical_arabic_text(arabic_text, language="Urdu")
    # print(f"تحليل ل: '{arabic_text}'\n")
    # print(explanation_ur)



@router.post("/analyze-arabic")
async def analyze_arabic(query: ArabicTextQuery):
    try:
        explanation = analyze_classical_arabic_text(query.text, query.language)
        return {"explanation": explanation}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))