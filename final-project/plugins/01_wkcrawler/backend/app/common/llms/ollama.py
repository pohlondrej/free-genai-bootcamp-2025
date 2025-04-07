import json
import logging
import requests
from typing import Dict
from .base import LLMProvider
from ..utils.json_helper import extract_json_from_response

logger = logging.getLogger(__name__)

class OllamaProvider(LLMProvider):
    """Ollama LLM provider implementation."""
    
    async def call(self, prompt: str) -> Dict:
        """Call Ollama API with prompt and return response.
        
        Args:
            prompt: The prompt to send to Ollama
            
        Returns:
            Dict containing the parsed JSON response
            
        Raises:
            Exception if API call fails or response parsing fails
        """
        logger.info("Calling Ollama API")
        try:
            response = requests.post(
                'http://localhost:11434/api/generate',
                json={
                    'model': 'qwen2.5:7b',
                    'prompt': prompt,
                    'stream': False,
                    'temperature': 0.1
                }
            )
            
            if response.status_code != 200:
                raise Exception(f"Ollama API error: {response.text}")
                
            llm_response = response.json()['response']
            logger.debug(f"Raw LLM response:\n{llm_response}")
            
            return extract_json_from_response(llm_response)
            
        except Exception as e:
            logger.error(f"Ollama API call failed: {str(e)}")
            raise
