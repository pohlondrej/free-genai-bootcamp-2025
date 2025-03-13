import os
import requests
from typing import Dict
import re

def summarize_text(text: str) -> Dict[str, str]:
    """Simplify English text to be more understandable.
    
    Args:
        text: Complex English text to simplify
        
    Returns:
        Dict containing:
        - original: Original text
        - simplified: Simplified version of the text
    """
    # Load the prompt template
    prompt_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 
                              'prompts', 'simplify.txt')
    with open(prompt_path, 'r', encoding='utf-8') as f:
        prompt_template = f.read()
    
    # Create the full prompt
    full_prompt = f"{prompt_template}\n\n{text}"
    
    try:
        # Call Ollama API
        response = requests.post('http://localhost:11434/api/generate',
                               json={
                                   'model': 'qwen2.5:3b',
                                   'prompt': full_prompt,
                                   'stream': False
                               })
        
        if response.status_code != 200:
            return {
                "original": text,
                "simplified": f"Error: Failed to simplify text (HTTP {response.status_code})"
            }
            
        simplified = response.json()['response'].strip()
        
        # Validation
        if len(simplified) < 10:  # Too short to be valid
            return {
                "original": text,
                "simplified": "Error: Generated text too short"
            }
            
        # Check for non-English characters (except common punctuation)
        if re.search(r'[^\x00-\x7F]+', simplified):
            return {
                "original": text,
                "simplified": "Error: Generated text contains non-English characters"
            }
            
        # Check if output is significantly different from input
        if simplified == text:
            return {
                "original": text,
                "simplified": "Error: Generated text is identical to input"
            }
            
        return {
            "original": text,
            "simplified": simplified
        }
        
    except Exception as e:
        return {
            "original": text,
            "simplified": f"Error simplifying text: {str(e)}"
        }

if __name__ == "__main__":
    # Test the function
    test_text = """Elephants are the largest living land animals. Three living species are currently recognised: 
    the African bush elephant (Loxodonta africana), the African forest elephant (L. cyclotis), and the Asian 
    elephant (Elephas maximus). They are the only surviving members of the family Elephantidae and the order 
    Proboscidea; extinct relatives include mammoths and mastodons."""
    
    result = summarize_text(test_text)
    print("\nOriginal:")
    print(result["original"])
    print("\nSimplified:")
    print(result["simplified"])
