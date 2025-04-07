import json
import os
import logging
from typing import Dict, Any
from tools.extract_vocab import extract_vocabulary
from tools.translate import translate_to_japanese
from tools.search_wikipedia import search_wikipedia
from tools.summarize_text import summarize_text
from google import genai
from common.llms import call_ollama, call_gemini, AgentError

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set up Google Gemini
client = None

class TopicExplorerAgent:
    def __init__(self, max_turns: int = 20):
        self.max_turns = max_turns
        self.turn_count = 0
        self.tools = {
            "search_wikipedia": search_wikipedia,
            "summarize_text": summarize_text,
            "translate_to_japanese": translate_to_japanese,
            "extract_vocabulary": extract_vocabulary
        }
        self.load_prompts()
    
    def load_prompts(self) -> None:
        """Load all prompt templates."""
        prompts_dir = os.path.join(os.path.dirname(__file__), 'prompts')
        
        # Load base prompt
        with open(os.path.join(prompts_dir, 'agent.txt'), 'r', encoding='utf-8') as f:
            self.base_prompt = f.read()
            
        # Load validation error prompt
        with open(os.path.join(prompts_dir, 'validation_error.txt'), 'r', encoding='utf-8') as f:
            self.validation_error_prompt = f.read()
            
        # Load tool error prompt
        with open(os.path.join(prompts_dir, 'tool_error.txt'), 'r', encoding='utf-8') as f:
            self.tool_error_prompt = f.read()

    def extract_json_from_response(self, text: str) -> Dict:
        """Extract the last valid JSON object from text."""
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
            raise AgentError("No JSON object found in response")
            
        # Try to parse each potential JSON, starting from the last one
        for json_str in reversed(potential_jsons):
            try:
                return json.loads(json_str)
            except json.JSONDecodeError:
                continue
                
        raise AgentError(f"Failed to parse any JSON from response: {text}")

    def validate_response(self, response: Dict) -> None:
        """Validate the structure of the LLM response."""
        if not isinstance(response, dict):
            raise AgentError(f"Response must be a dictionary, got {type(response)}")
            
        if "observation" not in response or "thought" not in response:
            raise AgentError("Response missing required fields: observation and thought")
            
        if "action" not in response and "final_answer" not in response:
            raise AgentError("Response must contain either action or final_answer")
            
        if "action" in response:
            action = response["action"]
            if not isinstance(action, dict):
                raise AgentError("Action must be a dictionary")
            if "name" not in action or "input" not in action:
                raise AgentError("Action missing required fields: name and input")
            if action["name"] not in self.tools:
                raise AgentError(f"Unknown tool: {action['name']}")

    def execute_tool(self, action: Dict) -> Dict[str, Any]:
        """Execute the specified tool with given input."""
        try:
            tool_name = action["name"]
            tool_input = action["input"]
            
            if tool_name not in self.tools:
                return {"error": f"Unknown tool: {tool_name}"}
            
            result = self.tools[tool_name](tool_input)
            return {"result": result}
        except Exception as e:
            return {"error": str(e)}

    def run(self, input_text: str, gemini_api_key: str) -> Dict:
        """Run the ReAct loop with input text."""
        if gemini_api_key:
            global client
            if client is None:
                client = genai.Client(api_key=gemini_api_key)

        self.turn_count = 0
        conversation = [
            self.base_prompt,
            f'Input: {input_text}'
        ]

        while self.turn_count < self.max_turns:
            self.turn_count += 1
            logger.info(f"Turn {self.turn_count}")

            try:
                # Get and validate LLM response
                response = None
                if gemini_api_key:
                    logger.info("Using Gemini API key for agent responses.")
                    response = call_gemini('\n'.join(conversation))
                else:
                    response = call_ollama('\n'.join(conversation))
                try:
                    self.validate_response(response)
                except AgentError as validation_error:
                    # Give the agent another chance to fix its response
                    logger.info(f"Response validation failed: {validation_error}. Asking agent to fix it.")
                    conversation.append(self.validation_error_prompt.format(error=str(validation_error)))
                    continue
                
                # Check for final answer
                if "final_answer" in response:
                    return response["final_answer"]

                # Execute tool if action is present
                action = response["action"]
                tool_result = self.execute_tool(action)
                
                if "error" in tool_result:
                    error_msg = f"Tool execution failed: {tool_result['error']}"
                    logger.error(error_msg)
                    conversation.append(self.tool_error_prompt.format(error=error_msg))
                else:
                    result_str = json.dumps(tool_result["result"], ensure_ascii=False)
                    conversation.append(f"Tool output: {result_str}")
                    
            except AgentError as e:
                logger.error(f"Agent error: {str(e)}")
                return {"error": str(e)}
            except Exception as e:
                logger.error(f"Unexpected error: {str(e)}")
                return {"error": f"Unexpected error: {str(e)}"}

        return {"error": f"Exceeded maximum turns ({self.max_turns})"}

if __name__ == "__main__":
    # Test the agent with English text
    agent = TopicExplorerAgent()
    result = agent.run("I would like to eat sushi and drink green tea.")
    print(json.dumps(result, ensure_ascii=False, indent=2))
