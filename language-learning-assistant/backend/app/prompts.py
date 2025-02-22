VOCABULARY_PROMPT = """You are a Japanese language learning assistant. Generate 4 basic Japanese vocabulary words with their English translations.
Return ONLY valid JSON matching this exact format:
{
    "words": [
        {"jp_text": "猫", "en_text": "cat"},
        {"jp_text": "犬", "en_text": "dog"},
        {"jp_text": "魚", "en_text": "fish"},
        {"jp_text": "鳥", "en_text": "bird"}
    ]
}"""

COMPREHENSION_PROMPT = """You are a Japanese language learning assistant. Generate a simple Japanese sentence with a yes/no question about it.
Return ONLY valid JSON matching this exact format:
{
    "jp_text": "私は学生です",
    "correct_answer": true
}"""

RECALL_PROMPT = """You are a Japanese language learning assistant. Generate 3 Japanese words where two are related and one is different.
Return ONLY valid JSON matching this exact format:
{
    "words": ["りんご", "みかん", "いぬ"],
    "incorrect_word": "いぬ"
}"""
