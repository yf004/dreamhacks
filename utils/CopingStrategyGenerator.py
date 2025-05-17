
from openai import OpenAI
from typing import List, Dict

import sys
from pathlib import Path
from EmotionAnalyzer import EmotionAnalyzer

parent_dir = Path('..')
sys.path.append(str(parent_dir.resolve()))

from config import DEEPSEEK_KEY

class CopingStrategyGenerator:
    def __init__(self):
        self.threshold = -0.3  # Minimum intensity for an emotion to be considered significant

    def suggest(self, emotions: Dict[str, float]) -> List[str]:
        # Filter for significant emotions
        significant_emotions = {k: v for k, v in emotions.items() if v < self.threshold}
        
        if not significant_emotions:
            return []

        # Convert the emotions dict into a readable format
        emotion_summary = ", ".join([f"{emotion}: {intensity:.2f}" for emotion, intensity in significant_emotions.items()])
        user_prompt = (
            f"A user is currently experiencing the following emotional intensities: {emotion_summary}.\n"
            "Suggest 3 coping strategies tailored to these emotions. Make sure they are practical, emotionally supportive, and brief.\n"
            "Use the EXACT format: [strategy 1],[strategy 2],[strategy 3].\n"
            "Each strategy should be wrapped in square brackets and separated by only a comma.\n"
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
                    {"role": "user", "content": user_prompt}
                ]
            )

            raw_output = completion.choices[0].message.content
            # Extract bullet points into a list
            strategies = raw_output.split(",")
            strategies = [x[1:-1] if x.startswith('[') and x.endswith(']') else x for x in strategies]

            return strategies if strategies else []

        except Exception as e:
            print(f"Error generating coping strategies: {e}")
            return []
        

# Example usage
if __name__ == "__main__":
    
    # analyzer = EmotionAnalyzer()
    # entry = "I feel really anxious and tired today. Nothing seems to be going right."
    # emotions = analyzer.analyze(entry)
    emotions = {
        "sadness": -0.5,
        "anger": -0.4,
        "surprise": 0.1
    }
    cope = CopingStrategyGenerator()
    strategies = cope.suggest(emotions)
    print("Emotions", emotions)
    print("Coping Strategies:", strategies)
    


