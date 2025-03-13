import json
import os
import logging
from typing import Dict, List, Optional, Any
import requests
from tools.extract_vocab import extract_vocabulary

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AgentError(Exception):
    """Custom error for agent-specific issues."""
    pass

class TopicExplorerAgent:
    def __init__(self, max_turns: int = 10):
        self.max_turns = max_turns
        self.turn_count = 0
        self.tools = {
            "extract_vocabulary": extract_vocabulary
        }
        self.load_prompt()
    
    def load_prompt(self) -> None:
        """Load the main agent prompt."""
        prompt_path = os.path.join(os.path.dirname(__file__), 
                                 'prompts', 'agent.txt')
        with open(prompt_path, 'r', encoding='utf-8') as f:
            self.base_prompt = f.read()

    def call_llm(self, prompt: str) -> Dict:
        """Call Ollama with the given prompt and parse JSON response."""
        response = requests.post('http://localhost:11434/api/generate',
                               json={
                                   'model': 'qwen2.5:3b',
                                   'prompt': prompt,
                                   'stream': False,
                                   'temperature': 0.1
                               })
        if response.status_code != 200:
            raise AgentError(f"Ollama API error: {response.text}")
            
        try:
            llm_response = response.json()['response']
            # Find the JSON object in the response
            start = llm_response.find('{')
            end = llm_response.rfind('}') + 1
            if start == -1 or end == 0:
                raise AgentError("No JSON object found in response")
            
            response_json = json.loads(llm_response[start:end])
            logger.info(f"Parsed LLM response: {json.dumps(response_json, indent=2, ensure_ascii=False)}")
            return response_json
        except json.JSONDecodeError as e:
            raise AgentError(f"Failed to parse LLM response as JSON: {str(e)}\nResponse: {llm_response}")

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

    def run(self, japanese_text: str) -> Dict:
        """Run the ReAct loop."""
        self.turn_count = 0
        conversation = [
            self.base_prompt,
            f'Input: Process this Japanese text: "{japanese_text}"'
        ]

        while self.turn_count < self.max_turns:
            self.turn_count += 1
            logger.info(f"Turn {self.turn_count}")

            try:
                # Get and validate LLM response
                response = self.call_llm('\n'.join(conversation))
                self.validate_response(response)
                
                # Check for final answer
                if "final_answer" in response:
                    return response["final_answer"]

                # Execute tool if action is present
                action = response["action"]
                tool_result = self.execute_tool(action)
                
                if "error" in tool_result:
                    error_msg = f"Tool execution failed: {tool_result['error']}"
                    logger.error(error_msg)
                    conversation.append(f"Error: {error_msg}")
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
    # Test the agent
    agent = TopicExplorerAgent()
    result = agent.run("ビール3本と弁当はいくらですか")
    print(json.dumps(result, ensure_ascii=False, indent=2))
