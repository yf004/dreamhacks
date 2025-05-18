from openai import OpenAI
import json
import re
import sys
from pathlib import Path
import os
from typing import List, Dict, Any
import datetime
import time

# Path setup for importing config
parent_dir = Path('..')
sys.path.append(str(parent_dir.resolve()))

from config import DEEPSEEK_KEY

class TherapyChatbot:
    def __init__(self):
        """Initialize the chatbot with conversation history and settings."""
        self.conversation_history = []
        self.session_start_time = datetime.datetime.now()
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=DEEPSEEK_KEY
        )
        
    def add_to_history(self, role: str, content: str) -> None:
        """Add a message to the conversation history."""
        self.conversation_history.append({"role": role, "content": content})
    
    def get_recent_history(self, max_tokens: int = 4000) -> List[Dict[str, str]]:
        """Get recent conversation history within token limit."""
        history = []
        token_count = 0
        
        # Add messages from newest to oldest until we hit the token limit
        for message in reversed(self.conversation_history):
            # Approximate token count (1 token ≈ 4 chars)
            message_tokens = len(message["content"]) // 4
            if token_count + message_tokens > max_tokens:
                break
            
            history.insert(0, message)
            token_count += message_tokens
            
        return history
    
    def chat(self, message: str, mode="talk") -> str:
        """Process user message and generate a response."""
        if mode == "talk":
            system_prompt = (
                "You are a supportive, gentle listener. "
                "Respond in a warm, validating tone without offering solutions unless asked. "
                "Keep responses concise and focused on the user's emotional needs. "
                "Use reflective listening techniques to show empathy."
            )
        else:  # mode == "therapy"
            system_prompt = (
                "You are a cognitive behavioral therapist. "
                "Respond with practical advice, reflective questions, and coping strategies. "
                "Focus on identifying cognitive distortions, suggesting reframing techniques, "
                "and offering evidence-based coping mechanisms. "
                "Use a compassionate yet direct approach."
            )

        try:
            # Add user message to history
            self.add_to_history("user", message)
            
            # Prepare messages for API call
            messages = [{"role": "system", "content": system_prompt}]
            
            # Add recent conversation history
            recent_history = self.get_recent_history()
            messages.extend(recent_history)
            
            # If no history was included, add the current message
            if len(recent_history) == 0:
                messages.append({"role": "user", "content": message})
            
            # Make API call
            completion = self.client.chat.completions.create(
                extra_body={},
                model="deepseek/deepseek-r1:free",
                messages=messages,
                temperature=0.7,  # Add some creativity
                max_tokens=1024   # Reasonable response length
            )
            
            response = completion.choices[0].message.content
            
            # Add assistant response to history
            self.add_to_history("assistant", response)
            
            return response.strip()

        except Exception as e:
            error_message = f"OpenAI API error: {e}"
            print(error_message)
            return "I'm sorry, I can't respond right now. Please try again later."
    
    def summarize_session(self) -> str:
        """Generate a summary of the therapy session."""
        if len(self.conversation_history) < 2:
            return "Not enough conversation data to summarize."
        
        try:
            summary_prompt = (
                "Summarize the main themes and issues discussed in this conversation. "
                "Include key insights, progress made, and potential areas for future focus. "
                "Be concise and focus on the therapeutic value of the exchange."
            )
            
            # Prepare messages for summary
            messages = [
                {"role": "system", "content": "You are a mental health professional summarizing a therapy session."},
                *self.get_recent_history(max_tokens=3000),
                {"role": "user", "content": summary_prompt}
            ]
            
            completion = self.client.chat.completions.create(
                extra_body={},
                model="deepseek/deepseek-r1:free",
                messages=messages,
                temperature=0.3,  # More factual
                max_tokens=500    # Short summary
            )
            
            return completion.choices[0].message.content.strip()
        
        except Exception as e:
            print(f"Error generating summary: {e}")
            return "Unable to generate session summary."
    
    def save_conversation(self, filename=None) -> str:
        """Save the conversation history to a file."""
        if not filename:
            # Generate a timestamp-based filename
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"therapy_session_{timestamp}.json"
        
        try:
            # Create a logs directory if it doesn't exist
            logs_dir = Path("./logs")
            logs_dir.mkdir(exist_ok=True)
            
            # Save conversation data
            session_data = {
                "session_start": self.session_start_time.isoformat(),
                "session_end": datetime.datetime.now().isoformat(),
                "conversation": self.conversation_history
            }
            
            with open(logs_dir / filename, 'w') as f:
                json.dump(session_data, f, indent=2)
            
            return f"Conversation saved to {logs_dir / filename}"
        
        except Exception as e:
            error_message = f"Error saving conversation: {e}"
            print(error_message)
            return "Failed to save the conversation."


# Example usage with a simple command line interface
def main():
    print("Welcome to TherapyBot!")
    print("Type 'exit' to end the session, 'mode' to switch modes, or 'summary' to get a session summary.")
    
    chatbot = TherapyChatbot()
    mode = "talk"  # Default mode
    
    while True:
        user_input = input("\nYou: ").strip()
        
        if user_input.lower() == 'exit':
            print("\nEnding session...")
            # Generate and show summary
            print("\nSession Summary:")
            print(chatbot.summarize_session())
            # Save conversation
            save_result = chatbot.save_conversation()
            print(save_result)
            print("Thank you for using TherapyBot. Take care!")
            break
            
        elif user_input.lower() == 'mode':
            if mode == "talk":
                mode = "therapy"
                print("Switched to therapy mode. I'll provide more structured therapeutic advice.")
            else:
                mode = "talk"
                print("Switched to talk mode. I'll focus on listening and validation.")
            continue
            
        elif user_input.lower() == 'summary':
            summary = chatbot.summarize_session()
            print(f"\nSession Summary:\n{summary}")
            continue
            
        # Regular conversation
        response = chatbot.chat(user_input, mode=mode)
        print(f"\nTherapyBot ({mode} mode): {response}")


if __name__ == "__main__":
    main()