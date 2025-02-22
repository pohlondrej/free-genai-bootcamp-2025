SESSION_TOPIC_PROMPT = """Generate a simple conversational topic for a Japanese language lesson.
Pick ONE random combination from these options:

Locations:
- School (classroom, library, cafeteria)
- Shopping (convenience store, department store, bookstore)
- Transport (train station, bus stop, airport)
- Entertainment (movie theater, park, museum)
- Daily life (home, apartment, neighborhood)

Activities:
- Asking/giving directions
- Buying something
- Meeting someone
- Making plans
- Learning/studying
- Helping someone

Time:
- Morning
- Afternoon
- Evening
- Weekend
- Holiday season

Make it specific and interesting, but keep it at beginner level.

Return ONLY valid JSON matching this format (but create your own unique scenario):
{{"topic": "at the bookstore", "context": "A student is looking for a Japanese textbook", "difficulty": "beginner"}}"""

VOCABULARY_PROMPT = """Generate 4 thematically related Japanese vocabulary words for a lesson about '{topic}'.
The words should be:
- Common, everyday words
- Related to the topic
- Suitable for beginners
- A mix of nouns and useful expressions

The japanese vocabulary words should not use furigana.

Return ONLY valid JSON matching this format (but use words related to your topic):
{{"words": [
    {{"jp_text": "example1", "en_text": "meaning1"}},
    {{"jp_text": "example2", "en_text": "meaning2"}},
    {{"jp_text": "example3", "en_text": "meaning3"}},
    {{"jp_text": "example4", "en_text": "meaning4"}}
], "preview": "Write an engaging preview for your chosen words."}}"""

MONOLOGUE_PROMPT = """Create a short Japanese monologue about '{topic}' using some of these words: {vocab_list}.
The monologue should be:
- Natural and realistic
- Simple enough for beginners
- Include at least 2 vocabulary words
- Have a clear yes/no question about its content

Return ONLY valid JSON matching this format (but create your own monologue):
{{"scene": "Describe where/when this happens", "jp_text": "Write natural Japanese dialog", "en_context": "Explain what's happening", "question": "Ask a yes/no question in Japanese", "correct_answer": true}}"""

RECALL_PROMPT = """Given this monologue: {jp_text}
Create a vocabulary recall quiz where:
1. Pick 2 words that appeared in the monologue
2. Add 1 unrelated but plausible Japanese word
3. The unrelated word should match the topic's context but NOT be in the monologue

Return ONLY valid JSON matching this format (using your chosen words):
{{"words": ["word1", "word2", "unrelated"], "incorrect_word": "unrelated", "hint": "Write a hint about which words to pick"}}"""

INTRO_TEMPLATE = "Welcome! {context} {preview}"
OUTRO_TEMPLATE = "Great job! You learned about {topic} and practiced {vocab_count} new words!"
