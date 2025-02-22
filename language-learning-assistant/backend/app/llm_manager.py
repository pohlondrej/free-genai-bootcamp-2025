import json
from typing import Any, Dict, Optional
from litellm import completion
from .config import settings
from .prompts import *

class LLMManager:
    def __init__(self):
        self.model = settings.LLM_MODEL
        
    def _call_llm(self, prompt: str) -> Optional[Dict[str, Any]]:
        try:
            print(f"\nSending prompt to LLM: {prompt[:100]}...(truncated)")
            response = completion(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful Japanese language teaching assistant. Always respond with valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=settings.LLM_TEMPERATURE,
                api_key=settings.LLM_API_KEY,
                max_retries=settings.LLM_MAX_RETRIES,
                timeout=settings.LLM_TIMEOUT
            )
            
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
