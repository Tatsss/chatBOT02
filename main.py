from fastapi import FastAPI, Request
from pydantic import BaseModel
from openai_client import get_openai_response_with_id
from firestore_db import get_previous_response_id, update_response_id
import uvicorn

app = FastAPI()

class LineWebhookBody(BaseModel):
    events: list

@app.get("/")
def read_root():
    return {"message": "LINE chatbot is up and running."}

@app.post("/webhook")
async def line_webhook(body: LineWebhookBody):
    try:
        event = body.events[0]
        user_id = event["source"]["userId"]
        user_message = event["message"]["text"]

        previous_id = get_previous_response_id(user_id)
        result = get_openai_response_with_id(user_id, user_message, previous_id)

        update_response_id(user_id, result["response_id"])

        return {"reply": result["reply"]}

    except Exception as e:
        print(f"Error: {e}")
        return {"reply": "エラーが発生しました。"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=10000)
