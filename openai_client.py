import os
from openai import OpenAI

class OpenAIClient:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = "gpt-4o"  # または "o3-deep-research-2025-06-26" に変更可

    def get_reply(self, user_message, previous_response_id=None):
        try:
            if previous_response_id:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[{"role": "user", "content": user_message}],
                    previous_response_id=previous_response_id
                )
            else:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[{"role": "user", "content": user_message}]
                )

            ai_message = response.choices[0].message.content.strip()
            response_id = response.id
            return ai_message, response_id
        except Exception as e:
            print("Error:", e)
            return "エラーが発生しました。", None
