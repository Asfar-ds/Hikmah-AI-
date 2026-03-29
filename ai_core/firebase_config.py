
# main.py
from fastapi import FastAPI, Depends, HTTPException, Header
from firebase_admin import credentials, firestore, auth
import firebase_admin, os, json

# --- initialize firebase admin ---
if not firebase_admin._apps:
    if os.getenv("FIREBASE_SERVICE_ACCOUNT"):
        info = json.loads(os.environ.get("FIREBASE_SERVICE_ACCOUNT"))
        cred = credentials.Certificate(info)
    else:
        cred = credentials.Certificate("serviceAccountKey.json")   # local dev only
    firebase_admin.initialize_app(cred)

db = firestore.client()
app = FastAPI()
