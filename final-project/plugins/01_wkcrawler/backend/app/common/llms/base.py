from abc import ABC, abstractmethod
from typing import Dict

class LLMProvider(ABC):
    """Base class for LLM providers."""
    
    @abstractmethod
    async def call(self, prompt: str) -> Dict:
        """Call the LLM with a prompt and return response as a dictionary.
        
        Args:
            prompt: The prompt to send to the LLM
            
        Returns:
            Dict containing the LLM response with ReAct format
        """
        pass
