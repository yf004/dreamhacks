# PromptGenerator.py

from typing import List
from openai import OpenAI

import sys
from pathlib import Path

parent_dir = Path('..')
sys.path.append(str(parent_dir.resolve()))

from config import DEEPSEEK_KEY


# Set your OpenAI API key
class PromptGenerator:
    def __init__(self):
        self.base_prompt = (
            "You are a therapeutic journaling assistant. Based on the user's recent journal entries, "
            "suggest ONE helpful and emotionally introspective journaling prompt to guide their next entry. "
            "Output only the prompt without any additional text, without bolding or italicising.\n\n"
            "Focus on emotional clarity and self-understanding.\n\n"
        )

    def generate(self, recent_entries: List[str]) -> str:
        context = "\n".join([f"Entry {i+1}: {entry}" for i, entry in enumerate(recent_entries)])

        full_prompt = self.base_prompt + context + "\n\nJournaling Prompt:"

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
                    {"role": "user", "content": full_prompt}
                ]
            )
            suggestion = completion.choices[0].message.content
            if ':' in suggestion:
                suggestion = suggestion.split(':', 1)[1].strip()
            return suggestion

        except Exception as e:
            print(f"Error generating prompt: {e}")
            return "What is something you felt deeply but didn't express today?"
        
if __name__ == "__main__":
    generator = PromptGenerator()
    sample_entries = [
        "I’ve been feeling overwhelmed with school lately.",
        "Sometimes I just want to shut everything out and be alone.",
        "Today I felt okay, but there’s always this underlying stress."
    ]
    prompt = generator.generate(sample_entries)
    print("Suggested Journaling Prompt:", prompt)






