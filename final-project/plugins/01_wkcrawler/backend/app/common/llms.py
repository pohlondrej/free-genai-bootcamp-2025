import requests
from typing import Dict
import logging

class AgentError(Exception):
    """Custom error for agent-specific issues."""
    pass

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def call_gemini(prompt: str) -> Dict:
    """Call Gemini with the given prompt and parse JSON response."""
    logger.info(f"Calling Gemini API")
    response = None
    try:
        response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=prompt,
            config={
                'response_mime_type': 'application/json',
            }
        )
        llm_response = response.text
        logger.debug(f"Raw LLM response:\n{llm_response}")
        
        response_json = extract_json_from_response(llm_response)
        logger.info(f"Parsed Gemini response: {json.dumps(response_json, indent=2, ensure_ascii=False)}")
        return response_json
    except Exception as e:
        raise AgentError(f"Failed to parse Gemini response: {str(e)}\nResponse: {response}")

def call_ollama(prompt: str) -> Dict:
    """Call Ollama with the given prompt and parse JSON response."""
    logger.info(f"Calling Ollama API")
    response = None
    try:
        response = requests.post('http://localhost:11434/api/generate',
                               json={
                                   'model': 'qwen2.5:7b',
                                   'prompt': prompt,
                                   'stream': False,
                                   'temperature': 0.1  # Low temperature for consistent output
                               })
        
        if response.status_code != 200:
            raise Exception(f"Ollama API error: {response.text}")
            
        llm_response = response.json()['response']
        logger.debug(f"Raw LLM response:\n{llm_response}")
        
        response_json = extract_json_from_response(llm_response)
        logger.info(f"Parsed LLM response: {json.dumps(response_json, indent=2, ensure_ascii=False)}")
        return response_json
    except Exception as e:
        raise AgentError(f"Failed to parse LLM response: {str(e)}\nResponse: {llm_response}")