
# Chatbot.py
'''
class TherapyChatbot:
    def chat(self, message: str, mode="talk") -> str:
        if mode == "talk":
            prompt = f"You are a supportive, gentle listener. Respond to: {message}"
        else:
            prompt = f"You are a problem-solving therapist. Help the user with: {message}"
        return call_llm(prompt)


prompt = "Based on recent journal entries, suggest a helpful journaling prompt for emotional clarity."
# PromptGenerator.py
class PromptGenerator:
    def generate(self, recent_entries: List[str]) -> str:
        return "What is something that made you feel safe recently?"


# CopingStrategyGenerator.py
class CopingStrategyGenerator:
    def suggest(self, emotions: Dict[str, float]) -> List[str]:
        if emotions["sadness"] > 0.5:
            return ["Take a short walk", "Talk to a friend", "Do a 5-minute breathing exercise"]


prompt = "You are a therapy assistant. Analyze the user's journal entry and summarize recurring thoughts, concerns, or behaviors. Offer 1 reflection."
class JournalTherapist:
    def generate_insight(self, entry: str) -> str:
        return "You seem to be consistently stressed about school deadlines."

class EmotionAnalyzer:
    def analyze(self, text: str) -> Dict[str, float]:
        return {"joy": 0.2, "sadness": 0.6, "anger": 0.1, "calm": 0.1}
    




'''