from fastapi import FastAPI, Request
from pydantic import BaseModel
from openai_client import OpenAIClient
from firestore_db import FirestoreDB
import os
import uvicorn
import requests

app = FastAPI()
openai_client = OpenAIClient()
db = FirestoreDB()

LINE_ACCESS_TOKEN = os.getenv("LINE_ACCESS_TOKEN")

class LineWebhookEvent(BaseModel):
    replyToken: str
    type: str
    message: dict
    source: dict

class LineWebhookBody(BaseModel):
    events: list[LineWebhookEvent]

@app.get("/")
def read_root():
    return {"message": "LINE chatbot is up and running."}

@app.post("/webhook")
async def webhook(body: LineWebhookBody):
    if not body.events:
        return {"status": "no events"}

    event = body.events[0]
    if event.type != "message" or event.message.get("type") != "text":
        return {"status": "unsupported message type"}

    user_id = event.source["userId"]
    user_message = event.message["text"]

    last_response_id = db.get_last_response_id(user_id)
    ai_response, response_id = openai_client.get_reply(user_message, last_response_id)

    db.log_conversation(user_id, user_message, ai_response, response_id)

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {LINE_ACCESS_TOKEN}"
    }
    payload = {
        "replyToken": event.replyToken,
        "messages": [{"type": "text", "text": ai_response}]
    }
    requests.post("https://api.line.me/v2/bot/message/reply", headers=headers, json=payload)

    return {"status": "success"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=int(os.getenv("PORT", 10000)), reload=True)
