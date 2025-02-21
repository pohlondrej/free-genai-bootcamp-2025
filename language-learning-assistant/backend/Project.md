# Project Definitions
## Data Structures
### Session API
```json
{
    "session_id": "uuid",
    "en_intro_audio": "cache_key",
    "en_outro_audio": "cache_key",
    "vocabulary_stage": {
        "stage_id": "uuid",
        "entries": [
            {
                "jp_audio": "cache_key",
                "en_text": "English Text"
            },
            {
                "jp_audio": "cache_key",
                "en_text": "English Text"
            },
            {
                "jp_audio": "cache_key",
                "en_text": "English Text"
            },
            {
                "jp_audio": "cache_key",
                "en_text": "English Text"
            }
        ]
    },
    "comprehension_stage": {
        "stage_id": "uuid",
        "jp_audio": "cache_key",
        "correct_answer": true
    },
    "recall_stage": {
        "stage_id": "uuid",
        "jp_audio": "cache_key",
        "options": ["日本", "はい", "こんにちは"],
        "incorrect_option": "こんにちは"
    }
}
```

## Tasks
### 1: Implement Core Quiz Logic
#### Description:
Develop the core backend logic for presenting quiz questions, handling user answers, calculating scores, and tracking quiz progress. This includes initializing the quiz, displaying questions and answer choices, accepting user input, checking answers against the correct answer, and updating the score.
#### Acceptance Criteria:
- Users can complete a multi-phase quiz session
- Scores are calculated correctly
- Quiz history is retrievable and clearable
#### Technical Notes:
- Ignore audio for now. If needed, use a short example sound as a placeholder.
- This is backend only. It should include API for the frontend, but no frontend implementation.

### 2: Integrate LLM for Question/Answer Generation
#### Description:
Integrate the chosen LLM (via LiteLLM) to generate Japanese listening comprehension questions and corresponding answer choices. Start with a basic prompt to generate simple questions.
- Implement prompt engineering for question generation
- Set up RAG with Chroma for context-aware questions
- Generate plausible incorrect answers
#### Acceptance Criteria:
The application can successfully query the LLM and receive generated question and answer data.
- LLM generates contextually appropriate questions
- Questions follow the specified difficulty level
- Generated incorrect answers are plausible but clearly wrong

### 3: Integrate TTS for Audio Playback
#### Description:
Integrate a TTS engine to generate audio for the Japanese questions and answer choices.
- Set up Japanese TTS engine with natural voice
- Set up English TTS for instructions and feedback
- Implement audio caching mechanism
#### Acceptance Criteria:
The application can generate and play audio for the questions and answers.
- Audio generation works for both languages
- Speech output is clear and natural-sounding
- Audio caching reduces latency
- Playback controls work reliably