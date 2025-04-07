import json
import os
import logging
from typing import List, Dict
from common.llms import LLMProvider

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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

async def extract_vocabulary(text: str, llm_provider: LLMProvider) -> List[Dict[str, str]]:
    """Extract vocabulary from Japanese text using LLM provider.
    
    Args:
        text: Japanese text to extract vocabulary from
        llm_provider: LLM provider to use for extraction
        
    Returns:
        List of vocabulary entries, each containing:
        - word: Japanese word
        - reading: Reading in hiragana
        - romaji: Romanized reading
        - meaning: English meaning
    """
    # Load and prepare prompt
    prompt_template = load_prompt()
    full_prompt = f"{prompt_template}\n\n{text}"
    
    try:
        # Get response from LLM
        raw_response = await llm_provider.call(full_prompt)
        
        # Extract JSON array from response if needed
        if isinstance(raw_response, str):
            # Find the JSON array in the response
            start = raw_response.find('[')
            end = raw_response.rfind(']') + 1
            if start == -1 or end == 0:
                raise ValueError("No JSON array found in response")
            vocab_json = raw_response[start:end]
            vocab_list = json.loads(vocab_json)
        else:
            vocab_list = raw_response
            
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
        
    except Exception as e:
        logger.error(f"Failed to extract vocabulary: {e}")
        return []

if __name__ == "__main__":
    # Test the function with a simple example
    test_text = "ビール3本と弁当はいくらですか"
    try:
        from common.llms import LLMFactory
        import asyncio
        
        async def test():
            llm = LLMFactory.create()
            vocab = await extract_vocabulary(test_text, llm)
            print(json.dumps(vocab, ensure_ascii=False, indent=2))
            
        asyncio.run(test())
    except Exception as e:
        print(f"Error: {e}")
