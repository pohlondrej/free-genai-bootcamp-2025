import os
import json
import requests
from typing import Dict

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

def translate_to_japanese(english_text: str) -> Dict[str, str]:
    """Translate English text to Japanese using Qwen model."""
    prompt = load_prompt()
    full_prompt = f"{prompt}\n\n{english_text}"
    
    response = requests.post('http://localhost:11434/api/generate',
                           json={
                               'model': 'qwen2.5:3b',
                               'prompt': full_prompt,
                               'stream': False,
                               'temperature': 0.1
                           })
    
    if response.status_code != 200:
        raise Exception(f"Ollama API error: {response.text}")
        
    try:
        llm_response = response.json()['response']
        # Find the JSON object in the response
        start = llm_response.find('{')
        end = llm_response.rfind('}') + 1
        if start == -1 or end == 0:
            raise ValueError("No JSON object found in response")
        
        result = json.loads(llm_response[start:end])
        
        # Validate translation
        if not validate_translation(result):
            raise ValueError("Invalid translation format")
            
        return {
            "translation": result["translation"].strip(),
            "english": result["english"].strip()
        }
        
    except Exception as e:
        print(f"Error translating text: {str(e)}")
        return {
            "translation": "",
            "english": english_text,
            "error": str(e)
        }

if __name__ == "__main__":
    # Test the translation
    test_text = "I would like to eat sushi."
    result = translate_to_japanese(test_text)
    print(json.dumps(result, ensure_ascii=False, indent=2))
