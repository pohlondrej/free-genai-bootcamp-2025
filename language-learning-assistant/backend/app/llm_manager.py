import json
from typing import Any, Dict, Optional
from time import sleep
from litellm import completion, ModelResponse
from .config import settings
from .prompts import *

class LLMError(Exception):
    """Base class for LLM-related errors"""
    pass

class LLMManager:
    def __init__(self):
        self.model = settings.LLM_MODEL
        self.backoff_factor = 2
        
    def _call_llm_with_retry(self, prompt: str) -> ModelResponse:
        """Call LLM with exponential backoff retry"""
        attempts = 0
        last_error = None
        
        while attempts < settings.LLM_MAX_RETRIES:
            try:
                return completion(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": "You are a helpful Japanese language teaching assistant. Always respond with valid JSON."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=settings.LLM_TEMPERATURE,
                    api_key=settings.LLM_API_KEY,
                    timeout=settings.LLM_TIMEOUT
                )
            except Exception as e:
                last_error = e
                attempts += 1
                if attempts < settings.LLM_MAX_RETRIES:
                    sleep_time = self.backoff_factor ** attempts
                    print(f"Attempt {attempts} failed. Retrying in {sleep_time}s...")
                    sleep(sleep_time)
                
        raise LLMError(f"Failed after {attempts} attempts. Last error: {last_error}")
        
    def _call_llm(self, prompt: str) -> Optional[Dict[str, Any]]:
        try:
            print(f"\nSending prompt to LLM: {prompt[:100]}...(truncated)")
            response = self._call_llm_with_retry(prompt)
            
            if not response or not response.choices:
                print("No response received from LLM")
                return None
                
            content = response.choices[0].message.content.strip()
            print(f"\nReceived response from LLM: {content}")
            
            # Remove any markdown formatting if present
            if content.startswith("```json"):
                content = content.split("```json")[1]
            if content.endswith("```"):
                content = content.split("```")[0]
            
            content = content.strip()
            print(f"\nAttempting to parse as JSON: {content}")
            
            return json.loads(content)
        except Exception as e:
            print(f"\nLLM API Error: {str(e)}")
            if 'response' in locals():
                print(f"Raw response: {response}")
            return None

    def generate_vocabulary(self):
        response = self._call_llm(VOCABULARY_PROMPT)
        if response and "words" in response:
            return response["words"]
        return None
        
    def generate_comprehension(self):
        return self._call_llm(COMPREHENSION_PROMPT)
        
    def generate_recall(self):
        return self._call_llm(RECALL_PROMPT)
