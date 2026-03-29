from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
# from .routes.relevancy_bridge import get_chatbot_response
# from .routes.opportunity_explorer import UserProfile, JobSelection
from .routes import speech_servies
# from .routes.classical_arabic_analyzer import analyze_classical_arabic_text
from .routes import (
    relevancy_bridge,  # this one works
    classical_arabic_analyzer,  # for FiveLens
    opportunity_explorer,  # for Opportunity
    nahw_cag, # for Nahw lens
    authentication_api # for authentication
)
from starlette.middleware.base import BaseHTTPMiddleware
from uvicorn.middleware.proxy_headers import ProxyHeadersMiddleware

from fastapi import APIRouter
router = APIRouter()


# app = FastAPI()
app = FastAPI(redirect_slashes=False)


# This will fix the Mixed Content error by recognizing the original request as HTTPS.
# We set max_hops=1 because Nginx is the only proxy between FastAPI and the Azure LB.
app.add_middleware(ProxyHeadersMiddleware)



# from .routes.classical_arabic_analyzer import analyze_classical_arabic_text
# from .routes import (
#     relevancy_bridge,  # this one works
#     classical_arabic_analyzer,  # for FiveLens
#     opportunity_explorer  # for Opportunity
# )


# CORS config
origins = [
    "https://hikmah-ai-hui3.vercel.app",
    "https://hikmah-ai-s2ep.vercel.app",
    "https://hikmah-ai-nnjx.vercel.app",
    "http://localhost:3000",
    "http://localhost:5173", 
    "http://127.0.0.1:3000",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:80"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the new speech services router
app.include_router(speech_servies.router, prefix="/speech", tags=["speech"])


class Query(BaseModel):
    user_input: str
    language: str

class ArabicTextQuery(BaseModel):
    text: str
    language: str = "Urdu"

# Register your routers
app.include_router(relevancy_bridge.router, prefix="/chat", tags=["chat"])
app.include_router(classical_arabic_analyzer.router, prefix="/analyze-arabic", tags=["arabic"])
app.include_router(opportunity_explorer.router, tags=["opportunities"])
app.include_router(nahw_cag.router, prefix="/sarf", tags=["sarf"])
app.include_router(authentication_api.router, prefix="/auth", tags=["auth"]) # <-- Integrate the auth API


# @app.post("/chat")
# async def chat(query: Query):
#     try:
#         # Call the chatbot response function
#         response_text = get_chatbot_response(query.user_input, query.language)
#         return {"response": response_text}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# @app.post("/opportunities")
# async def opportunities(profile: UserProfile):
#     try:
#         response_text = get_job_opportunities(profile)
#         return {"response": response_text}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# @app.post("/skillset")
# async def skillset(job: JobSelection):
#     try:
#         response_text = get_skillset_for_job(job)
#         return {"response": response_text}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


# @app.post("/analyze-arabic")
# async def analyze_arabic(query: ArabicTextQuery):
#     try:
#         explanation = analyze_classical_arabic_text(query.text, query.language)
#         return {"explanation": explanation}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    return {"message": "Backend is running"}