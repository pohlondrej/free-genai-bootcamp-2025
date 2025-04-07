import os
import logging
from typing import Dict
from common.llms import LLMProvider

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def summarize_text(text: str, llm_provider: LLMProvider) -> Dict[str, str]:
    """Simplify English text to be more understandable.
    
    Args:
        text: Complex English text to simplify
        llm_provider: LLM provider to use for simplification
        
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
        # Get response from LLM
        raw_response = await llm_provider.call(full_prompt)
        
        # Extract JSON from response if needed
        if isinstance(raw_response, str):
            response = eval(raw_response)
        else:
            response = raw_response
            
        # Validate response
        if not isinstance(response, dict) or 'simplified' not in response:
            raise ValueError("Expected response with 'simplified' field")
            
        # Ensure simplified text is not empty
        simplified = response['simplified'].strip()
        if not simplified:
            raise ValueError("Simplified text is empty")
            
        return {
            'original': text,
            'simplified': simplified
        }
    except Exception as e:
        logger.error(f"Failed to simplify text: {e}")
        raise

if __name__ == "__main__":
    # Test the function
    test_text = """Elephants are the largest living land animals. Three living species are currently recognised: 
    the African bush elephant (Loxodonta africana), the African forest elephant (L. cyclotis), and the Asian 
    elephant (Elephas maximus). They are the only surviving members of the family Elephantidae and the order Proboscidea."""
    
    try:
        from common.llms import LLMFactory
        import asyncio
        
        async def test():
            llm = LLMFactory.create()
            result = await summarize_text(test_text, llm)
            print("Original:", result["original"])
            print("\nSimplified:", result["simplified"])
            
        asyncio.run(test())
    except Exception as e:
        print(f"Error: {e}")
