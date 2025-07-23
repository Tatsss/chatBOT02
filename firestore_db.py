import os
import firebase_admin
from firebase_admin import credentials, firestore

# 初期化（1回のみ）
if not firebase_admin._apps:
    cred = credentials.Certificate("chatbot-cb433-firebase-adminsdk-fbsvc-13eabf3186.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()

def get_previous_response_id(user_id: str):
    doc = db.collection("users").document(user_id).get()
    if doc.exists:
        return doc.to_dict().get("last_response_id")
    return None

def update_response_id(user_id: str, response_id: str):
    db.collection("users").document(user_id).set({
        "last_response_id": response_id
    }, merge=True)
