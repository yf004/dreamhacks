from EmotionAnalyzer import EmotionAnalyzer
from CopingStrategyGenerator import CopingStrategyGenerator
from PromptGenerator import PromptGenerator
from Summarizer import Summarizer
from TherapyChatbot import TherapyChatbot

from typing import List, Dict

def get_emotion_analysis(entry: str) -> Dict[str, float]:
    """
    Analyzes the emotional content of a journal entry.
    
    Args:
        entry (str): The journal entry to analyze.
        
    Returns:
        Dict[str, float]: A dictionary with emotion names as keys and their intensities as values.
    """
    analyzer = EmotionAnalyzer()
    return analyzer.analyze(entry)

def get_coping_strategies(emotions: Dict[str, float]) -> List[str]:

    """
    Suggests coping strategies based on the analyzed emotions.
    
    Args:
        emotions (Dict[str, float]): A dictionary with emotion names as keys and their intensities as values.
        
    Returns:
        List[str]: A list of suggested coping strategies.
    """
    generator = CopingStrategyGenerator()
    return generator.suggest(emotions)

def get_journaling_prompt(recent_entries: List[str]) -> str:
    """
    Generates a journaling prompt based on recent journal entries.
    
    Args:
        recent_entries (List[str]): A list of recent journal entries.
        
    Returns:
        str: A suggested journaling prompt.
    """
    generator = PromptGenerator()
    return generator.generate(recent_entries)

def get_journal_summary(entry: str) -> str:
    """
    Generates an insight based on a journal entry.
    
    Args:
        entry (str): The journal entry to analyze.
        
    Returns:
        str: A summary and insight based on the journal entry.
    """
    summarizer = Summarizer()
    return summarizer.generate_insight(entry)



