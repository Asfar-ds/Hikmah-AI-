


from fastapi import APIRouter, HTTPException, Depends, Header
from firebase_admin import credentials, firestore, auth
import firebase_admin, os, json
from pydantic import BaseModel 
from google.cloud import firestore as gcf
from groq import Groq

client = Groq(api_key=os.environ.get("OPENAI_API_KEY"))


router = APIRouter()

# -------------------------
# Initialize Firebase Admin
# -------------------------
if not firebase_admin._apps:
    if os.environ.get("FIREBASE_SERVICE_ACCOUNT"):  # for production
        info = json.loads(os.getenv("FIREBASE_SERVICE_ACCOUNT"))
        cred = credentials.Certificate(info)
    else:

        cred = credentials.Certificate("db-project.json")  # for local

        # cred = credentials.Certificate("serviceAccountKey.json")  # for local

        # cred = credentials.Certificate("db-project.json")  # for local
    firebase_admin.initialize_app(cred)

db = firestore.client()

# -------------------------
# Token Verification Helper
# -------------------------
async def verify_token(authorization: str = Header(...)):
    try:
        token = authorization.split("Bearer ")[1]
        decoded = auth.verify_id_token(token)
        return decoded
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

# -------------------------
# Models
# -------------------------
class UserData(BaseModel):
    name: str | None = None

# -------------------------
# Signup/Login (common entry)
# -------------------------


@router.post("/sync")
def sync_user(data: UserData, user=Depends(verify_token)):
    """
    Called on every signup or login.
    Ensures the user document exists in Firestore.
    """
    uid = user["uid"]
    email = user.get("email")

    user_ref = db.collection("users").document(uid)
    doc = user_ref.get()

    if not doc.exists:
        # Create user on first signup
        user_ref.set({
            "user_id": uid,
            "user_email": email,
            "user_name": data.name or "",
            "created_at": gcf.SERVER_TIMESTAMP
        })
        message = "User created in Firestore"
    else:
        # Optionally update name or last_login
        user_ref.update({
            "last_login": gcf.SERVER_TIMESTAMP
        })
        message = "User already exists; updated last_login"

    return {"message": message, "user_id": uid, "email": email}

# -------------------------
# Get User Profile
# -------------------------

@router.get("/user_profile")
def get_user_profile(user=Depends(verify_token)):
    uid = user["uid"]
    user_doc = db.collection("users").document(uid).get()
    if not user_doc.exists:
        raise HTTPException(status_code=404, detail="User not found")
    return user_doc.to_dict()