from typing import Optional
from .base import LLMProvider
from .gemini import GeminiProvider
from .ollama import OllamaProvider

class LLMFactory:
    """Factory for creating LLM providers."""
    
    @staticmethod
    def create(api_key: Optional[str] = None) -> LLMProvider:
        """Create an LLM provider based on API key availability.
        
        Args:
            api_key: Optional Gemini API key
            
        Returns:
            LLMProvider instance (either GeminiProvider or OllamaProvider)
        """
        if api_key:
            return GeminiProvider(api_key)
        return OllamaProvider()
