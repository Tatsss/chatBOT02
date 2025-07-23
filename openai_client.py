import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_openai_response_with_id(user_id, prompt, previous_response_id=None):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "user", "content": prompt}
        ],
        previous_response_id=previous_response_id
    )
    return {
        "reply": response.choices[0].message.content.strip(),
        "response_id": response.id
    }
