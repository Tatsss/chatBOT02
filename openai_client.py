import os
from openai import OpenAI

class OpenAIClient:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = "gpt-4o"
        self.system_prompt = os.getenv(
            "OPENAI_SYSTEM_PROMPT",
            "あなたは親切なアシスタントです。"
        )

    def get_reply(self, user_message, previous_response_id=None):
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user",   "content": user_message}
        ]
        try:
            if previous_response_id:
                response = self.client.responses.create(
                    model=self.model,
                    input=messages,
                    previous_response_id=previous_response_id
                )
            else:
                response = self.client.responses.create(
                    model=self.model,
                    input=messages,
                    store=True
                )

            # 応答テキストとレスポンスIDを取得
            ai_message  = response.output_text.strip()
            response_id = response.id
            return ai_message, response_id

        except Exception as e:
            print("Error:", e)
            return "エラーが発生しました。", None
