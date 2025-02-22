VOCABULARY_PROMPT = """You are a Japanese language learning assistant. Generate 4 random Japanese vocabulary words with their English translations.
Return ONLY valid JSON matching this exact JSON format, but come up with your own random words:
{
    "words": [
        {"jp_text": "猫", "en_text": "cat"},
        {"jp_text": "犬", "en_text": "dog"},
        {"jp_text": "魚", "en_text": "fish"},
        {"jp_text": "鳥", "en_text": "bird"}
    ]
}"""

COMPREHENSION_PROMPT = """You are a Japanese language learning assistant. Generate a random Japanese sentence with a yes/no question about it.
Return ONLY valid JSON matching this exact JSON format, but generate your own random sentence:
{
    "jp_text": "私は学生です",
    "correct_answer": true
}"""

RECALL_PROMPT = """You are a Japanese language learning assistant. Generate 3 random Japanese words where two are related and one is different.
Return ONLY valid JSON matching this exact JSON format, but come up with your own random words:
{
    "words": ["りんご", "みかん", "いぬ"],
    "incorrect_word": "いぬ"
}"""
