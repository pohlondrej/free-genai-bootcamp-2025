SESSION_TOPIC_PROMPT = """Generate a simple conversational topic for a Japanese language lesson.

Recently used topics (DO NOT USE THESE):
{recent_topics}

Pick ONE random combination from these options:

Locations:
- School (classroom, library, cafeteria)
- Shopping (convenience store, department store, bookstore)
- Transport (train station, bus stop, airport)
- Entertainment (movie theater, park, museum)
- Daily life (home, apartment, neighborhood)
- Work (office, meeting, interview)
- Nature (forest, beach, garden)
- Food (restaurant, café, market)
- Health (hospital, gym, doctor)
- Science (lab, classroom, library)
- Outdoor (park, trail, mountain)

Activities:
- Asking/giving directions
- Buying something
- Meeting someone
- Making plans
- Learning/studying
- Helping someone
- Playing/reading/watching/listening

Time:
- Morning
- Afternoon
- Evening
- Weekend
- Holiday season
- Night
- Day
- Year

IMPORTANT:
- Choose a topic that is DIFFERENT from the recent topics listed above
- Make it specific and interesting

Return ONLY valid JSON matching this format (but create your own unique scenario):
{{"topic": "at the bookstore", "context": "A student is looking for a Japanese textbook", "difficulty": "beginner"}}"""

VOCABULARY_PROMPT = """Generate 4 thematically related Japanese vocabulary words for a lesson about '{topic}'.
The words should be:
- Common, everyday words
- Related to the topic
- Suitable for beginners
- A mix of nouns and useful expressions

Previous successful examples (DO NOT COPY, USE ONLY AS INSPIRATION):
{examples}

IMPORTANT:
- The japanese vocabulary words should not use furigana.
- Create completely new words different from the examples
- Words should be relevant to '{topic}' and must be from allowed words: {allowed_words}
- Words must use allowed kanji: {allowed_kanji}, replace other kanji with hiragana.
- Use natural Japanese writing (kanji where appropriate and where allowed)
- Choose words that work well together in a conversation
- Do not use special formatting (e.g. bold, italics)
- The preview should be in English and should contain no Japanese words.

Return ONLY valid JSON matching this format (but use your own unique words):
{{"words": [
    {{"jp_text": "example1", "en_text": "meaning1"}},
    {{"jp_text": "example2", "en_text": "meaning2"}},
    {{"jp_text": "example3", "en_text": "meaning3"}},
    {{"jp_text": "example4", "en_text": "meaning4"}}
], "preview": "Write a short but engaging preview for the topic."}}"""

MONOLOGUE_PROMPT = """Create a short Japanese monologue about '{topic}' using some of these words: {vocab_list}.
The monologue should be:
- It should prioritize words from {allowed_words}.
- Natural and realistic
- It must be a monologue, NOT a dialogue
- Simple enough for beginners
- Short, maximum 3 sentences
- Include at least 2 vocabulary words
- Have a clear yes/no question about its content
- Do not use special formatting (e.g. bold, italics)

Return ONLY valid JSON matching this format (but create your own monologue):
{{"scene": "Describe where/when this happens", "jp_text": "Write natural Japanese dialog", "en_context": "Explain what's happening", "question": "Ask a yes/no question in English", "correct_answer": true}}"""

RECALL_PROMPT = """Given this first monologue: {jp_text}
Create a continuation of the monologue (1-2 sentences) that follows naturally from the first monologue.
Then create a vocabulary quiz about words used in your continuation.

IMPORTANT:
- Do not use special formatting (e.g. bold, italics)
- Do not use furigana or romaji in the japanese text
- Prioritize using words from {allowed_words}.
- Only use kanji from {allowed_kanji}, replace other kanji with hiragana.

Return ONLY valid JSON matching this format:
{{"continuation": {{
    "scene": "Describe the next moment in the story",
    "jp_text": "Write the continuation in natural Japanese",
    "en_context": "Explain what happens next"
}},
"quiz": {{
    "words": ["word1", "word2", "unrelated"],
    "incorrect_word": "unrelated",
    "hint": "Which two words appeared in the continuation?"
}}}}"""

INTRO_TEMPLATE = "Welcome! {context} {preview}"
OUTRO_TEMPLATE = "Great job! You learned about {topic} and practiced {vocab_count} words!"
