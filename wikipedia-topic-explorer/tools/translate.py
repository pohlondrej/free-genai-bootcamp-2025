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
            raise Exception("No JSON object found in response")
        
        result = json.loads(llm_response[start:end])
        return result
    except json.JSONDecodeError as e:
        raise Exception(f"Failed to parse translation response: {str(e)}")

if __name__ == "__main__":
    # Test the translation
    test_text = "I would like to eat sushi."
    result = translate_to_japanese(test_text)
    print(json.dumps(result, ensure_ascii=False, indent=2))
