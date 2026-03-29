# app/models/schemas.py

from pydantic import BaseModel, Field
from typing import Optional

# 1. Used by relevancy_bridge (the /chat endpoint)
class Query(BaseModel):
    user_input: str = Field(..., description="The user's text input for the chatbot.")
    language: str = Field(..., description="The language the response should be in.")

# 2. Used by classical_arabic_analyzer
class ArabicTextQuery(BaseModel):
    text: str = Field(..., description="The classical Arabic text to analyze.")
    language: str = "Urdu" # Default value for this field

# 3. Used by opportunity_explorer (the /opportunities endpoint)
class UserProfile(BaseModel):
    interests: str = Field(..., description="User's interests for career mapping.")
    background: str = Field(..., description="User's educational or professional background (e.g., Dars-e-Nizami).")

# 4. Used by opportunity_explorer (the /skillset endpoint)
class JobSelection(BaseModel):
    job_title: str = Field(..., description="The job title for which skill requirements are needed.")