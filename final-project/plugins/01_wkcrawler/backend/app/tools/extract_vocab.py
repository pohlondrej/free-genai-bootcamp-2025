import json
import os
import logging
from typing import List, Dict
from common.llms import LLMProvider

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def load_prompt() -> str:
    """Load the vocabulary extraction prompt template."""
    prompt_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 
                              'prompts', 'vocabulary.txt')
    with open(prompt_path, 'r', encoding='utf-8') as f:
        return f.read()

def validate_vocab_entry(entry: Dict) -> bool:
    """Validate a vocabulary entry."""
    logger.debug(f"Validating entry: {entry}")
    try:
        # All fields must be present and non-empty
        required_fields = ["word", "reading", "romaji", "meaning"]
        if not all(field in entry and entry[field] for field in required_fields):
            logger.debug(f"Missing or empty fields in entry: {entry}")
            return False
            
        # Don't include particles unless they're part of a compound
        if entry["word"] in ["は", "が", "の", "に", "を", "で", "へ"]:
            logger.debug(f"Skipping particle: {entry['word']}")
            return False
            
        # Don't include entries with spaces or invalid characters
        if any(c in entry["reading"] for c in [" ", "_", "-"]):
            logger.debug(f"Skipping invalid reading: {entry['reading']}")
            return False
        if any(c in entry["romaji"] for c in [" ", "_"]):
            logger.debug(f"Skipping invalid romaji: {entry['romaji']}")
            return False
            
        return True
    except (KeyError, TypeError) as e:
        logger.debug(f"Validation error for entry: {e}")
        return False

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
        logger.debug(f"Raw LLM response: {raw_response}")
        
        # Extract vocab list from response
        if isinstance(raw_response, dict):
            vocab_list = raw_response.get("vocabulary", [])
        else:
            logger.warning(f"Unexpected response type: {type(raw_response)}")
            vocab_list = []
            
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
        
        logger.debug(f"Found {len(unique_entries)} valid vocabulary entries")
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
