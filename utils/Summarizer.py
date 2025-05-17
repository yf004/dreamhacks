from openai import OpenAI
from pathlib import Path
import sys

# Add parent directory to sys.path
parent_dir = Path('..')
sys.path.append(str(parent_dir.resolve()))

from config import DEEPSEEK_KEY

class Summarizer:
    def __init__(self):
        self.base_prompt = (
            "You are a helpful mental wellness assistant. Analyze the user's journal entry below, "
            "and provide a concise summary of recurring thoughts, concerns, or behaviors\n"
            "Keep it under 50 words, and do not include any additional text or bolding or italicising.\n\n"
        )

    def generate_insight(self, entry: str) -> str:
        try:
            client = OpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=DEEPSEEK_KEY
            )

            full_prompt = f"{self.base_prompt}\n\nJournal Entry:\n{entry}\n\nSummary and Insight:"

            completion = client.chat.completions.create(
                model="deepseek/deepseek-r1:free",
                messages=[
                    {"role": "system", "content": "You are a helpful mental wellness assistant."},
                    {"role": "user", "content": full_prompt}
                ]
            )
            raw = completion.choices[0].message.content
            return raw.strip()

        except Exception as e:
            print(f"Error generating journal insight: {e}")
            return -1
