import json
from typing import Dict

def extract_json_from_response(text: str) -> Dict:
    """Extract the last valid JSON object from text.
    
    Args:
        text: Text containing one or more JSON objects
        
    Returns:
        Dict containing the parsed JSON
        
    Raises:
        Exception if no valid JSON is found
    """
    # Find all potential JSON objects in the text
    potential_jsons = []
    stack = []
    start = -1
    
    for i, char in enumerate(text):
        if char == '{':
            if not stack:
                start = i
            stack.append(char)
        elif char == '}':
            if stack:
                stack.pop()
                if not stack and start != -1:
                    potential_jsons.append(text[start:i+1])
                    start = -1
    
    if not potential_jsons:
        raise Exception("No JSON object found in response")
        
    # Try to parse each potential JSON, starting from the last one
    for json_str in reversed(potential_jsons):
        try:
            return json.loads(json_str)
        except json.JSONDecodeError:
            continue
            
    raise Exception(f"Failed to parse any JSON from response: {text}")
