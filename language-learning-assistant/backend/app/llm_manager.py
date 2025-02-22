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
                    timeout=settings.LLM_TIMEOUT,
                    frequency_penalty=settings.LLM_FREQUENCY_PENALTY
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
            
            # Generate first monologue
            try:
                vocab_list = ", ".join(w["jp_text"] for w in vocab_data["words"])
            except (KeyError, TypeError):
                print("Malformed vocabulary data")
                return None
                
            monologue_data = self._call_llm(
                MONOLOGUE_PROMPT.format(
                    topic=topic_data["topic"],
                    vocab_list=vocab_list
                )
            )
            if not monologue_data or "jp_text" not in monologue_data:
                print("Failed to generate first monologue")
                return None
            print(f"Generated first monologue: {monologue_data}")
            
            # Generate continuation and recall quiz
            recall_data = self._call_llm(
                RECALL_PROMPT.format(jp_text=monologue_data["jp_text"])
            )
            if not recall_data or "continuation" not in recall_data or "quiz" not in recall_data:
                print("Failed to generate continuation and recall quiz")
                return None
            print(f"Generated continuation and recall: {recall_data}")
            
            # Validate continuation and quiz
            continuation = recall_data["continuation"]
            quiz = recall_data["quiz"]
            
            if not all(key in continuation for key in ["scene", "jp_text", "en_context"]):
                print("Missing required continuation fields")
                return None
                
            if not all(key in quiz for key in ["words", "incorrect_word", "hint"]):
                print("Missing required quiz fields")
                return None
                
            if len(quiz["words"]) != 3 or quiz["incorrect_word"] not in quiz["words"]:
                print("Invalid quiz format")
                return None

            # Validate all required fields exist before returning
            data_sections = {
                "topic": topic_data,
                "vocabulary": vocab_data,
                "monologue": monologue_data,
                "continuation": continuation,
                "quiz": quiz
            }
            required_fields = {
                "topic": ["topic", "context"],
                "vocabulary": ["words", "preview"],
                "monologue": ["jp_text", "correct_answer"],
                "continuation": ["jp_text", "scene", "en_context"],
                "quiz": ["words", "incorrect_word", "hint"]
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
                "monologue": monologue_data,
                "recall": {
                    "continuation": continuation,
                    "quiz": quiz
                },
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
