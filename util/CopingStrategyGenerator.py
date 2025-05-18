from openai import OpenAI
from typing import List, Dict
import sys
from pathlib import Path
parent_dir = Path('..')
sys.path.append(str(parent_dir.resolve()))
from config import DEEPSEEK_KEY

class CopingStrategyGenerator:
    def __init__(self):
        self.threshold = -0.3  # Minimum intensity for an emotion to be considered significant
        
    def suggest(self, emotions: Dict[str, float], journal_entry: str = None) -> List[str]:
        """
        Suggest coping strategies based on emotions detected and journal content.
        
        Args:
            emotions: Dictionary of emotions and their intensities
            journal_entry: Optional text from the user's journal entry to provide context
            
        Returns:
            A list of coping strategies tailored to the emotions and context
        """
        # Filter for significant negative emotions
        significant_emotions = {k: v for k, v in emotions.items() if v < self.threshold}
       
        if not significant_emotions:
            return []
            
        # Convert the emotions dict into a readable format
        emotion_summary = ", ".join([f"{emotion}: {intensity:.2f}" for emotion, intensity in significant_emotions.items()])
        
        # Create a context-aware prompt that includes journal content when available
        journal_context = f"\nContext from journal entry: \"{journal_entry}\"" if journal_entry else ""
        
        user_prompt = (
            f"A user is experiencing these emotional intensities: {emotion_summary}.{journal_context}\n"
            "Based on both the emotions and the context (if provided), suggest 3 specific coping strategies "
            "that are practical, emotionally supportive, and relevant to their situation.\n"
            "Each strategy should be brief but specific enough to be actionable.\n"
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
                    {"role": "system", "content": "You are a helpful mental wellness assistant specializing in personalized coping strategies."},
                    {"role": "user", "content": user_prompt}
                ]
            )
            raw_output = completion.choices[0].message.content
            
            # Extract bullet points into a list
            strategies = raw_output.split(",")
            strategies = [x[1:-1] if x.startswith('[') and x.endswith(']') else x for x in strategies]
            
            # Clean up and format strategies
            strategies = [s.strip() for s in strategies if s.strip()]
            return strategies if strategies else []
            
        except Exception as e:
            print(f"Error generating coping strategies: {e}")
            return []
       
# Example usage
if __name__ == "__main__":
    emotions = {
        "sadness": -0.5,
        "anger": -0.4,
        "surprise": 0.1
    }
    
    entry = "I feel really anxious and tired today. Nothing seems to be going right at work and my colleague keeps taking credit for my ideas."
    
    cope = CopingStrategyGenerator()
    strategies = cope.suggest(emotions, entry)
    print("Emotions:", emotions)
    print("Journal Entry:", entry)
    print("Coping Strategies:", strategies)