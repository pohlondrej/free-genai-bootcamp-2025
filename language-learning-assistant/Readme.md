# Language Learning Assistant
## Business Goal
A language learning application that leverages AI to enhance Japanese listening comprehension skills. It uses AI-powered question generation and speech synthesis based on RAG and LLM output to provide adaptive quizzes.
## Technical Uncertainties
- How can I craft effective LLM prompts to *consistently* generate high-quality, relevant, and appropriately challenging questions?
- What is the best approach for deploying the application's backend (LLM, vector database, TTS) in a cloud or locally?
- How can I ensure the LLM generates plausible but incorrect answers for multiple-choice questions?
- Which TTS model provides the best quality and natural-sounding Japanese speech?
- What strategies can I use to minimize the latency between user interaction, question generation, TTS, and feedback?
## Technical Restrictions
- Must use LiteLLM for model management.
- Must use Streamlit for frontend.
- Must use Chroma for vector storage.
- Should use SQLite for non-vector data.
- Must use a Japanese and English TTS engines.
- Should store user quiz history (scores, answers).
    - Users should be able to clear the quiz history.
- Should be deployable locally (using Docker).
- Should follow separation of concerns.
## Session Format
### 1. Introduction Phase
- English TTS: Announcer welcomes user and sets context
- English TTS: Pre-lesson vocabulary preview
- **Quiz 1**: Vocabulary matching
  - Format: Match 4 Japanese audio clips to English words
  - Goal: Prepare user for upcoming monologue

### 2. Main Monologue Phase
- English TTS: Topic introduction and speaker context
- Japanese TTS: First segment (2-3 sentences)
- **Quiz 2**: Comprehension check
  - Format: Yes/No question about content
  - Goal: Verify understanding of main points

### 3. Extension Phase
- Japanese TTS: Second segment (1-2 sentences)
- **Quiz 3**: Vocabulary recall
  - Format: Select 2 words from 3 options that appeared in monologue
  - Goal: Test active listening and vocabulary retention

### 4. Wrap-up Phase
- English TTS: Brief summary and farewell
- Display session score and progress

### Expected Duration
- Total session time: ~2-3 minutes
- Each quiz: 10-30 seconds

## Development Setup

### Environment Variables
Required environment variables:
```bash
export LLM_API_KEY="your-api-key-here"
```

Optional environment variables:
```bash
export LLM_MODEL="gpt-3.5-turbo"
export LLM_TEMPERATURE="0.7"
export LLM_MAX_RETRIES="3"
export LLM_TIMEOUT="30"