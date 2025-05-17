from typing import Dict
from transformers import pipeline
from openai import OpenAI
import json
import re
import sys
from pathlib import Path

parent_dir = Path('..')
sys.path.append(str(parent_dir.resolve()))

from config import DEEPSEEK_KEY


class EmotionAnalyzer:
    def extract_first_between_braces(input_string):
        match = re.search(r'\{(.*?)\}', input_string)
        return match.group(0) if match else None

    def analyze(self, text: str) -> Dict[str, float]:
        prompt = (
            "Analyze the following journal entry and return the emotion scores. "
            "Emotions can be: e.g., joy, sadness, anger, fear, surprise, disgust, etc. "
            "and the values should be floats between -1 and 1 such that the sum of their absolute values is 1.\n"
            "Negative emotions should have a negative value while positive emotions should have a positive value.\n"
            "Output should be in in the exact format without any additional text: [emotion],[score],[emotion],[score], etc...\n"
            "For both emotion and score, each should be wrapped in square brackets and separated by a comma.\n\n"
            f"Entry:\n{text}\n\nEmotion Scores:"
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
            raw = completion.choices[0].message.content
            print("AI response:", raw)

            emotion_scores = raw.split(",")
            emotion_scores = [x[1:-1] if x.startswith('[') and x.endswith(']') else x for x in emotion_scores]
            emotion_scores = {emotion_scores[i]: float(emotion_scores[i + 1]) for i in range(0, len(emotion_scores), 2)}
            print ("Parsed emotion scores:", emotion_scores)

            return emotion_scores

        except Exception as e:
            print(f"OpenAI API error: {e}")
            return {}


# Example usage
if __name__ == "__main__":
    analyzer = EmotionAnalyzer()
    entry = "I feel really anxious and tired today. Nothing seems to be going right."
    emotions = analyzer.analyze(entry)
    print(emotions)
