from typing import Dict, List
from openai import OpenAI
import sys
from pathlib import Path
parent_dir = Path('..')
sys.path.append(str(parent_dir.resolve()))
from config import DEEPSEEK_KEY
from .EmotionAnalyzer import EmotionAnalyzer
from .CopingStrategyGenerator import CopingStrategyGenerator

class JournalResponseGenerator:
    def __init__(self):
        self.emotion_analyzer = EmotionAnalyzer()
        self.strategy_generator = CopingStrategyGenerator()
        
    def generate_response(self, journal_entry: str) -> str:
        """
        Process a journal entry and generate a compassionate, personalized response.
        
        Args:
            journal_entry: The user's journal entry text
            
        Returns:
            A complete response acknowledging emotions and providing appropriate strategies
        """
        # Analyze emotions in the journal entry
        emotions = self.emotion_analyzer.analyze(journal_entry)
        
        # Get coping strategies if there are negative emotions
        strategies = self.strategy_generator.suggest(emotions, journal_entry)
        
        # Generate a complete response using the LLM
        return self._create_complete_response(journal_entry, emotions, strategies)
    
    def _create_complete_response(self, journal_entry: str, emotions: Dict[str, float], strategies: List[str]) -> str:
        """
        Create a cohesive response that acknowledges emotions and provides strategies.
        
        Args:
            journal_entry: The original journal entry
            emotions: Dictionary of emotions and their intensities
            strategies: List of coping strategies (if any)
            
        Returns:
            A complete, personalized response
        """
        # Format emotions for the prompt
        emotion_summary = ", ".join([f"{emotion} ({intensity:.2f})" for emotion, intensity in emotions.items()])
        
        # Format strategies for the prompt
        strategies_text = "\n- " + "\n- ".join(strategies) if strategies else "No specific strategies needed."
        
        prompt = (
            f"Below is a user's journal entry, followed by the emotions detected and suggested coping strategies.\n\n"
            f"Journal entry: '{journal_entry}'\n\n"
            f"Emotions detected: {emotion_summary}\n\n"
            f"Suggested strategies: {strategies_text}\n\n"
            f"Write a compassionate, personalized response that:\n"
            f"1. Acknowledges their feelings with empathy (reflecting the specific emotions detected)\n"
            f"2. Offers validation and understanding\n"
            f"3. Smoothly incorporates relevant coping strategies if negative emotions were detected\n"
            f"4. Maintains a supportive, gentle tone throughout\n"
            f"5. Keeps the response concise (around 150 words, 2 paragraphs)\n"
            f"Your response should flow naturally as if written by a supportive friend or therapist."
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
                    {"role": "system", "content": "You are an empathetic and supportive mental wellness assistant."},
                    {"role": "user", "content": prompt}
                ]
            )
            response = completion.choices[0].message.content
            return response
        except Exception as e:
            print(f"Error generating complete response: {e}")
            # Fallback response in case of API error
            return (
                f"I notice you might be feeling {emotion_summary}. "
                "Thank you for sharing your thoughts with me. "
                f"Consider trying: {'; '.join(strategies) if strategies else 'taking a moment for yourself today.'}"
            )

# Example usage
if __name__ == "__main__":
    responder = JournalResponseGenerator()
    entry = "I had a really tough day at work. My boss criticized my project in front of everyone and I felt so embarrassed. I can't stop replaying it in my head and wondering if I'm actually good at my job."
    response = responder.generate_response(entry)
    print("\nJournal Entry:")
    print(entry)
    print("\nGenerated Response:")
    print(response)