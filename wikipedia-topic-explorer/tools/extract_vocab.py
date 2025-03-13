import json
import os
from typing import List, Dict

def load_prompt() -> str:
    """Load the vocabulary extraction prompt template."""
    prompt_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 
                              'prompts', 'vocabulary.txt')
    with open(prompt_path, 'r', encoding='utf-8') as f:
        return f.read()

def validate_vocab_entry(entry: Dict) -> bool:
    """Validate a vocabulary entry."""
    # All fields must be present and non-empty
    required_fields = ["word", "reading", "romaji", "meaning"]
    if not all(field in entry and entry[field] for field in required_fields):
        return False
        
    # Don't include particles unless they're part of a compound
    if entry["word"] in ["は", "が", "の", "に", "を", "で", "へ"]:
        return False
        
    # Don't include entries with spaces or invalid characters
    if any(c in entry["reading"] for c in [" ", "_", "-"]):
        return False
    if any(c in entry["romaji"] for c in [" ", "_"]):
        return False
        
    return True

def extract_vocabulary(text: str) -> List[Dict[str, str]]:
    """Extract vocabulary from Japanese text using Ollama."""
    import requests

    # Load and prepare prompt
    prompt_template = load_prompt()
    full_prompt = f"{prompt_template}\n\n{text}"
    
    # Call Ollama API
    response = requests.post('http://localhost:11434/api/generate',
                           json={
                               'model': 'qwen2.5:3b',
                               'prompt': full_prompt,
                               'stream': False,
                               'temperature': 0.1  # Low temperature for consistent output
                           })
    
    if response.status_code != 200:
        raise Exception(f"Ollama API error: {response.text}")
    
    # Extract JSON from response
    try:
        result = response.json()['response']
        # Find the JSON array in the response
        start = result.find('[')
        end = result.rfind(']') + 1
        if start == -1 or end == 0:
            raise ValueError("No JSON array found in response")
        vocab_json = result[start:end]
        vocab_list = json.loads(vocab_json)
        
        # Filter and validate entries
        valid_entries = [entry for entry in vocab_list if validate_vocab_entry(entry)]
        
        # Remove duplicates while preserving order
        seen = set()
        unique_entries = []
        for entry in valid_entries:
            key = entry["word"]
            if key not in seen:
                seen.add(key)
                unique_entries.append(entry)
        
        return unique_entries
        
    except (json.JSONDecodeError, KeyError, ValueError) as e:
        raise Exception(f"Failed to parse vocabulary: {str(e)}")

if __name__ == "__main__":
    # Test the function with a simple example
    test_text = "ビール3本と弁当はいくらですか"
    try:
        vocab = extract_vocabulary(test_text)
        print(json.dumps(vocab, ensure_ascii=False, indent=2))
    except Exception as e:
        print(f"Error: {e}")
