import datetime
import uuid
from typing import List, Dict
from openai import OpenAI  # Ensure correct import based on your actual client
from config import DEEPSEEK_KEY  # Assuming your API key is stored here

class TherapyChatbot:
    def __init__(self, journal_inputs):
        """Initialize the chatbot with optional journal context."""
        self.conversation_history = []
        self.session_start_time = datetime.datetime.now()
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=DEEPSEEK_KEY
        )
        self.session_id = str(uuid.uuid4())
        
        # Process journal inputs if provided
        if journal_inputs:
            for entry in journal_inputs:
                self.add_to_history("user", entry)
    
    def add_to_history(self, role: str, content: str) -> None:
        self.conversation_history.append({"role": role, "content": content})
    
    def get_recent_history(self, max_tokens: int = 4000) -> List[Dict[str, str]]:
        history = []
        token_count = 0
        for message in reversed(self.conversation_history):
            message_tokens = len(message["content"]) // 4
            if token_count + message_tokens > max_tokens:
                break
            history.insert(0, message)
            token_count += message_tokens
        return history
    
    def chat(self, message: str, mode="talk") -> str:
        system_prompt = (
            "You are a supportive, gentle listener. "
            "Respond in a warm, validating tone without offering solutions unless asked. "
            "Keep responses concise and focused on the user's emotional needs. "
            "Use reflective listening techniques to show empathy."
        ) if mode == "talk" else (
            "You are a cognitive behavioral therapist. "
            "Respond with practical advice, reflective questions, and coping strategies. "
            "Focus on identifying cognitive distortions, suggesting reframing techniques, "
            "and offering evidence-based coping mechanisms. "
            "Use a compassionate yet direct approach."
        )

        try:
            self.add_to_history("user", message)
            messages = [{"role": "system", "content": system_prompt}]
            recent_history = self.get_recent_history()
            messages.extend(recent_history)
            if len(recent_history) == 0:
                messages.append({"role": "user", "content": message})

            completion = self.client.chat.completions.create(
                extra_body={},
                model="deepseek/deepseek-r1:free",
                messages=messages,
                temperature=0.7,
                max_tokens=1024
            )
            response = completion.choices[0].message.content
            self.add_to_history("assistant", response)
            return response.strip()

        except Exception as e:
            print(f"OpenAI API error: {e}")
            return "I'm sorry, I can't respond right now. Please try again later."
    
    def summarize_session(self) -> str:
        if len(self.conversation_history) < 2:
            return "Not enough conversation data to summarize."
        try:
            summary_prompt = (
                "Summarize the main themes and issues discussed in this conversation. "
                "Include key insights, progress made, and potential areas for future focus. "
                "Be concise and focus on the therapeutic value of the exchange."
            )
            messages = [
                {"role": "system", "content": "You are a mental health professional summarizing a therapy session."},
                *self.get_recent_history(max_tokens=3000),
                {"role": "user", "content": summary_prompt}
            ]
            completion = self.client.chat.completions.create(
                extra_body={},
                model="deepseek/deepseek-r1:free",
                messages=messages,
                temperature=0.3,
                max_tokens=500
            )
            return completion.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error generating summary: {e}")
            return "Unable to generate session summary."
    
    def save_entire_history(self):
        try:
            return {
                'id': self.session_id,
                'time': self.session_start_time.isoformat(),
                'history': self.conversation_history
            }
        except Exception as e:
            print(f"Error saving conversation: {e}")
