import json
from typing import Any, Dict, Optional
from time import sleep
from litellm import completion, ModelResponse
from .config import settings
from .prompts import *

class LLMError(Exception):
    """Base class for LLM-related errors"""
    pass

class LLMManager:
    def __init__(self):
        self.model = settings.LLM_MODEL
        self.backoff_factor = 2
        
    def _call_llm_with_retry(self, prompt: str) -> ModelResponse:
        """Call LLM with exponential backoff retry"""
        attempts = 0
        last_error = None
        
        while attempts < settings.LLM_MAX_RETRIES:
            try:
                return completion(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": "You are a helpful Japanese language teaching assistant. Always respond with valid JSON."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=settings.LLM_TEMPERATURE,
                    api_key=settings.LLM_API_KEY,
                    timeout=settings.LLM_TIMEOUT
                )
            except Exception as e:
                last_error = e
                attempts += 1
                if attempts < settings.LLM_MAX_RETRIES:
                    sleep_time = self.backoff_factor ** attempts
                    print(f"Attempt {attempts} failed. Retrying in {sleep_time}s...")
                    sleep(sleep_time)
                
        raise LLMError(f"Failed after {attempts} attempts. Last error: {last_error}")
        
    def _call_llm(self, prompt: str) -> Optional[Dict[str, Any]]:
        try:
            print(f"\nSending prompt to LLM: {prompt[:100]}...(truncated)")
            response = self._call_llm_with_retry(prompt)
            
            if not response or not response.choices:
                print("No response received from LLM")
                return None
                
            content = response.choices[0].message.content.strip()
            print(f"\nReceived response from LLM: {content}")
            
            # Remove any markdown formatting if present
            if content.startswith("```json"):
                content = content.split("```json")[1]
            if content.endswith("```"):
                content = content.split("```")[0]
            
            content = content.strip()
            print(f"\nAttempting to parse as JSON: {content}")
            
            return json.loads(content)
        except Exception as e:
            print(f"\nLLM API Error: {str(e)}")
            if 'response' in locals():
                print(f"Raw response: {response}")
            return None

    def generate_session_content(self) -> Optional[Dict[str, Any]]:
        """Generate a complete, coherent learning session"""
        try:
            # Generate topic and context
            topic_data = self._call_llm(SESSION_TOPIC_PROMPT)
            if not topic_data or "topic" not in topic_data:
                print("Failed to generate topic")
                return None
            print(f"Generated topic: {topic_data}")
                
            # Generate vocabulary with context
            vocab_data = self._call_llm(
                VOCABULARY_PROMPT.format(topic=topic_data["topic"])
            )
            if not vocab_data or "words" not in vocab_data:
                print("Failed to generate vocabulary")
                return None
            print(f"Generated vocabulary: {vocab_data}")
            
            # Generate conversation using words that exist
            try:
                vocab_list = ", ".join(w["jp_text"] for w in vocab_data["words"])
            except (KeyError, TypeError):
                print("Malformed vocabulary data")
                return None
                
            conv_data = self._call_llm(
                CONVERSATION_PROMPT.format(
                    topic=topic_data["topic"],
                    vocab_list=vocab_list
                )
            )
            if not conv_data or "jp_text" not in conv_data:
                print("Failed to generate conversation")
                return None
            print(f"Generated conversation: {conv_data}")
            
            # Generate recall quiz based on conversation
            recall_data = self._call_llm(
                RECALL_PROMPT.format(jp_text=conv_data["jp_text"])
            )
            if not recall_data or "words" not in recall_data:
                print("Failed to generate recall quiz")
                return None
            print(f"Generated recall: {recall_data}")
            
            # Validate recall response
            if recall_data:
                words = recall_data.get("words", [])
                incorrect = recall_data.get("incorrect_word")
                if len(words) != 3 or not incorrect or incorrect not in words:
                    print("Invalid recall format - regenerating")
                    recall_data = None
                    for _ in range(settings.LLM_MAX_RETRIES):
                        recall_data = self._call_llm(
                            RECALL_PROMPT.format(jp_text=conv_data["jp_text"])
                        )
                        if (recall_data and len(recall_data.get("words", [])) == 3 
                            and recall_data.get("incorrect_word") in recall_data["words"]):
                            break
                        recall_data = None
                
            if not recall_data or "words" not in recall_data or len(recall_data["words"]) != 3:
                print("Failed to generate valid recall quiz")
                return None
            
            # Validate all required fields exist before returning
            data_sections = {
                "topic": topic_data,
                "vocabulary": vocab_data,
                "conversation": conv_data,
                "recall": recall_data
            }
            required_fields = {
                "topic": ["topic", "context"],
                "vocabulary": ["words", "preview"],
                "conversation": ["jp_text", "correct_answer"],
                "recall": ["words", "incorrect_word"]
            }
            
            for section, fields in required_fields.items():
                data = data_sections[section]  # Use the dictionary instead of locals()
                if not data or not all(field in data for field in fields):
                    print(f"Missing required fields in {section}")
                    print(f"Expected: {fields}")
                    print(f"Got: {list(data.keys()) if data else None}")
                    return None
            
            return {
                "topic": topic_data,
                "vocabulary": vocab_data,
                "conversation": conv_data,
                "recall": recall_data,
                "intro_text": INTRO_TEMPLATE.format(
                    context=topic_data["context"],
                    preview=vocab_data.get("preview", "Let's practice!")
                ),
                "outro_text": OUTRO_TEMPLATE.format(
                    topic=topic_data["topic"],
                    vocab_count=len(vocab_data["words"])
                )
            }
            
        except Exception as e:
            print(f"Session generation error: {str(e)}")
            import traceback
            print(f"Traceback: {traceback.format_exc()}")
            return None
