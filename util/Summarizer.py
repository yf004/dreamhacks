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
            "You are a mental wellness assistant creating reference summaries for journal entries. "
            "Create a concise, factual summary of the journal entry that: "
            "1) Captures key themes, emotions, events, and concerns "
            "2) Preserves important details for future reference "
            "3) Uses neutral, objective language "
            "4) Would help someone quickly recall this entry's content months later "
            "5) Avoids interpretations or advice\n\n"
            "Keep the summary under 50 words. Format as a single paragraph with no additional text, "
            "no headers, no bullet points, and no formatting like bold or italics."
        )

    def generate_insight(self, entry: str) -> str:
        try:
            client = OpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=DEEPSEEK_KEY
            )

            full_prompt = f"{self.base_prompt}\n\nJournal Entry:\n{entry}\n\nSummary:"

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