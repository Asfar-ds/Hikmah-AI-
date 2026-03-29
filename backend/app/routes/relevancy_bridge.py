
import os
# from openai import OpenAI

from fastapi import APIRouter, HTTPException
from ..models.schema import Query

from groq import Groq

client = Groq(api_key=os.environ.get("OPENAI_API_KEY"))

# 1. Instantiate the router
router = APIRouter()


# Initialize the OpenAI client with the API key
# client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def get_chatbot_response(user_input: str, language: str) -> str:
    system_prompt = (

        "You help Islamic scholars bridge classical Dars e Nizami teachings with modern contexts by "
        "analyzing audience psychology, behavior patterns, and requirements to create relevant and "
        "engaging presentations for contemporary audiences."
        "You can response to user in the user selected language."

        "You are a helpful assistant that can respond in both English and Urdu. "
        "When a user asks a question, respond in the both languages english and urdu."

    )
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_input}
    ]
    
    try:
        # Call the OpenAI API
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",  # or use the specified model
            messages=messages
        )
        
        # Extract the assistant's reply
        return response.choices[0].message.content.strip()
    
    except Exception as e:
        return f"Error: {str(e)}"
    
# test
# user_input = "What is the difference between Dars-e-Nizami teachings and Islamic teachings?"
# response = get_chatbot_response(user_input, language="English")
# print("Response:", response)


@router.post("/") 
async def chat(query: Query):
    try:
        # Use the imported function
        response_text = get_chatbot_response(query.user_input, query.language)
        return {"response": response_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
