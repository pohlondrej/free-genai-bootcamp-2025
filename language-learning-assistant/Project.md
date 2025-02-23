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
        "question": "LLM-generated question in English",
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
#### Technical Notes:
- Ignore session history for now. Keep everything in memory, no persistance required.
- Ignore audio for now. If needed, use a short example sound as a placeholder.
- This is backend only. It should include API for the frontend, but no frontend implementation.

### 2: Basic LLM Integration
#### Description:
Set up basic LiteLLM integration with a simple prompt workflow.
- Install and configure LiteLLM
- Create basic prompt templates
- Implement basic error handling and retry logic
- Add configuration for model selection and parameters
#### Acceptance Criteria:
- Can successfully connect to LLM API
- Can generate basic Japanese questions
- Response format matches Session API structure

### 3: Question Generation Logic
#### Description:
Implement core question generation logic with proper prompt engineering.
- Design prompt templates for each quiz phase
- Implement temperature/sampling controls
- Add output validation
- Create fallback content for API failures
#### Acceptance Criteria:
- Questions are appropriate for each stage
- Output is consistently formatted
- Japanese language output is correct

### 4: RAG Integration
#### Description:
Implement Retrieval-Augmented Generation with Chroma.
- Set up Chroma database
- Create embedding pipeline
- Implement retrieval logic
- Connect retrieval results to prompt generation
#### Acceptance Criteria:
- Can store and retrieve relevant context
- Questions are contextually appropriate
- Search results are relevant

### 5: Answer Generation
#### Description:
Implement generation of plausible incorrect answers.
- Design prompts for distractor generation
- Implement validation of incorrect answers
- Add difficulty scaling
- Ensure answers are clearly wrong but plausible
#### Acceptance Criteria:
- Generates appropriate number of options
- Incorrect answers are plausible but clearly wrong
- Answers are appropriate for difficulty level

### 6: Integrate TTS for Audio Playback
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

### 7: Create Frontend
#### Description:
Implement a basic Streamlit frontend for the language learning application.

- Build core quiz interface:
  - Display current question/task
  - Show answer options
  - Accept user input
  - Display correct/incorrect feedback
- Implement audio features:
  - Basic audio player
  - Replay button
- Add minimal visual feedback:
  - Loading indicators
  - Error messages
  - Stage progress (1/3, 2/3, 3/3)

#### Acceptance Criteria:
- Users can complete a full quiz session
- Audio plays correctly
- Interface shows current stage clearly
- Loading and errors are visible
- Correct/incorrect feedback works

#### Technical Notes:
- Must use Streamlit as required
- Keep interface minimal and functional
- Focus on core quiz flow
- Handle basic error cases
- Should be implemented 

## Improvements
### 1: Japanese Language Quality Improvements
#### Description:
Implement additional validation and quality controls for Japanese language output.
- Add validation for kanji/kana mix appropriate for beginners
- Implement JLPT level checking
- Verify vocabulary usage in generated content
- Add grammar pattern validation
- Enhance question generation with difficulty controls

#### Acceptance Criteria:
- Japanese text follows appropriate difficulty level
- Vocabulary words actually appear in monologues
- Questions are properly formulated
- Grammar patterns match target level

#### Technical Notes:
- Consider using existing Japanese language processing libraries
- May require additional language models or APIs
- Should not significantly impact response time
- Can be implemented incrementally