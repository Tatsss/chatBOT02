import os
from openai import OpenAI

class OpenAIClient:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = "gpt-4o"  # 必要に応じて他モデルに変更可

    def get_reply(self, user_message, previous_response_id=None):
        try:
            if previous_response_id:
                response = self.client.responses.create(
                    model=self.model,
                    input=[{"role": "user", "content": user_message}],
                    previous_response_id=previous_response_id
                )
            else:
                # 初回は store=True でサーバに会話状態を保存
                response = self.client.responses.create(
                    model=self.model,
                    input=[{"role": "user", "content": user_message}],
                    store=True
                )

            # 応答テキストとレスポンスIDを取得
            ai_message = response.output_text.strip()
            response_id = response.id
            return ai_message, response_id

        except Exception as e:
            print("Error:", e)
            return "エラーが発生しました。", None
