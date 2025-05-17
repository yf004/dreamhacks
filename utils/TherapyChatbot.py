
from openai import OpenAI
import json
import re
import sys
from pathlib import Path

parent_dir = Path('..')
sys.path.append(str(parent_dir.resolve()))

from config import DEEPSEEK_KEY
class TherapyChatbot:
    def chat(self, message: str, mode="talk") -> str:
        if mode == "talk":
            prompt = (
                f"You are a supportive, gentle listener. The user says:\n\n"
                f"{message}\n\n"
                f"Respond in a warm, validating tone without offering solutions unless asked."
            )
        else:
            prompt = (
                f"You are a cognitive behavioral therapist. The user presents the following problem:\n\n"
                f"{message}\n\n"
                f"Respond with practical advice, reflective questions, and coping strategies."
            )

        try:
            client = OpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=DEEPSEEK_KEY
            )

            completion = client.chat.completions.create(
                extra_body={},
                model="deepseek/deepseek-r1:free",
                messages=[
                    {"role": "system", "content": "You are a helpful mental wellness assistant."},
                    {"role": "user", "content": prompt}
                ]
            )
            response = completion.choices[0].message.content

            return response.strip()

        except Exception as e:
            print(f"OpenAI API error: {e}")
            return "I'm sorry, I can't respond right now. Please try again later."
