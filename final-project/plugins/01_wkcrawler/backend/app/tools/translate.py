import os
import json
import logging
from typing import Dict
from common.llms import LLMProvider

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_prompt() -> str:
    """Load the translation prompt."""
    prompt_path = os.path.join(os.path.dirname(__file__), '..', 
                             'prompts', 'translate.txt')
    with open(prompt_path, 'r', encoding='utf-8') as f:
        return f.read()

def validate_translation(response: Dict) -> bool:
    """Validate translation response."""
    # Check required fields
    required_fields = ["translation", "english"]
    if not all(field in response and response[field] for field in required_fields):
        return False
        
    # Ensure translation contains Japanese characters
    has_japanese = any(ord(c) > 0x3000 for c in response["translation"])
    if not has_japanese:
        return False
        
    # Ensure English text matches input
    if not response["english"].strip():
        return False
        
    return True

async def translate_to_japanese(english_text: str, llm_provider: LLMProvider) -> Dict[str, str]:
    """Translate English text to Japanese using LLM.
    
    Args:
        english_text: Text to translate
        llm_provider: LLM provider to use for translation
        
    Returns:
        Dict containing:
        - english: Original English text
        - translation: Japanese translation
    """
    # Load and prepare prompt
    prompt_template = load_prompt()
    full_prompt = f"{prompt_template}\n\n{english_text}"
    
    try:
        # Get response from LLM
        response = await llm_provider.call(full_prompt)
        
        # If response is string, try to extract JSON
        if isinstance(response, str):
            # Find the JSON object in the response
            start = response.find('{')
            end = response.rfind('}') + 1
            if start == -1 or end == 0:
                raise ValueError("No JSON object found in response")
            
            response = json.loads(response[start:end])
        
        # Validate translation
        if not validate_translation(response):
            raise ValueError("Invalid translation format")
            
        return {
            "translation": response["translation"].strip(),
            "english": response["english"].strip()
        }
        
    except Exception as e:
        logger.error(f"Error translating text: {e}")
        return {
            "translation": "",
            "english": english_text,
            "error": str(e)
        }

if __name__ == "__main__":
    # Test the translation
    test_text = "I would like to eat sushi."
    try:
        from common.llms import LLMFactory
        import asyncio
        
        async def test():
            llm = LLMFactory.create()
            result = await translate_to_japanese(test_text, llm)
            print(json.dumps(result, ensure_ascii=False, indent=2))
            
        asyncio.run(test())
    except Exception as e:
        print(f"Error: {e}")
