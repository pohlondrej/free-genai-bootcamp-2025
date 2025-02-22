SESSION_TOPIC_PROMPT = """Generate a simple conversational topic for a Japanese language lesson. Return ONLY valid JSON matching this format: {{"topic": "at the cafe", "context": "A student orders coffee and a sandwich for lunch", "difficulty": "beginner"}}"""

VOCABULARY_PROMPT = """Generate 4 thematically related Japanese vocabulary words for a lesson about '{topic}'. Return ONLY valid JSON matching this format: {{"words": [{{"jp_text": "コーヒー", "en_text": "coffee"}}, {{"jp_text": "サンドイッチ", "en_text": "sandwich"}}, {{"jp_text": "注文する", "en_text": "to order"}}, {{"jp_text": "お願いします", "en_text": "please"}}], "preview": "Let's learn some useful words you might need when ordering at a cafe."}}"""

CONVERSATION_PROMPT = """Create a short Japanese conversation about '{topic}' using these words: {vocab_list}. Return ONLY valid JSON matching this format: {{"scene": "At a small cafe during lunch time", "jp_text": "すみません。コーヒーとサンドイッチをお願いします。", "en_context": "A customer is placing their order", "question": "お客さんは何を注文しましたか？", "correct_answer": true}}"""

RECALL_PROMPT = """Given this conversation: {jp_text}
Generate a vocabulary quiz with EXACTLY 3 Japanese words, where:
- Two words MUST be from the conversation
- One word MUST be unrelated but plausible
- The unrelated word MUST be marked as incorrect_word
Return ONLY valid JSON matching this exact format with EXACTLY 3 words:
{{"words": ["コーヒー", "サンドイッチ", "赤ちゃん"], "incorrect_word": "赤ちゃん", "hint": "Which two words were in the customer's order?"}}

IMPORTANT:
- The words array MUST contain exactly 3 items
- Two words MUST appear in the conversation
- One word MUST be unrelated but plausible
- The incorrect_word MUST be one of the three words"""

INTRO_TEMPLATE = "Welcome! {context} {preview}"
OUTRO_TEMPLATE = "Great job! You learned about {topic} and practiced {vocab_count} new words!"
