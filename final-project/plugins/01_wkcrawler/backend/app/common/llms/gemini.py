import json
import logging
from typing import Dict
from google import genai
from .base import LLMProvider
from ..utils.json_helper import extract_json_from_response

logger = logging.getLogger(__name__)

class GeminiProvider(LLMProvider):
    """Gemini LLM provider implementation."""
    
    def __init__(self, api_key: str):
        """Initialize Gemini client with API key."""
        self.client = genai.Client(api_key=api_key)
        
    async def call(self, prompt: str) -> Dict:
        """Call Gemini API with prompt and return response.
        
        Args:
            prompt: The prompt to send to Gemini
            
        Returns:
            Dict containing the parsed JSON response
            
        Raises:
            Exception if API call fails or response parsing fails
        """
        logger.info("Calling Gemini API")
        try:
            response = self.client.models.generate_content(
                model='gemini-2.0-flash',
                contents=prompt,
                config={
                    'response_mime_type': 'application/json',
                }
            )
            llm_response = response.text
            logger.debug(f"Raw LLM response:\n{llm_response}")
            
            return extract_json_from_response(llm_response)
            
        except Exception as e:
            logger.error(f"Gemini API call failed: {str(e)}")
            raise
