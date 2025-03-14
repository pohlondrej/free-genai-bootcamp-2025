# Technical Specification

## Project Structure
```
wikipedia-topic-explorer/
├── tools/                    # ReAct framework tools
│   ├── search_wikipedia.py   # Wikipedia article search and fetch
│   ├── summarize_text.py     # Text simplification
│   ├── translate.py          # Japanese translation
│   └── extract_vocab.py      # Vocabulary extraction
├── prompts/                  # LLM prompt templates
│   ├── agent.txt             # Main ReAct agent prompt
│   ├── simplify.txt          # Text simplification prompt
│   ├── translate.txt         # Japanese translation prompt
│   └── vocabulary.txt        # Vocabulary extraction prompt
├── agent.py                  # Main ReAct agent implementation
├── api.py                    # FastAPI application
└── frontend.py               # Streamlit interface
```

## Architecture

### Backend (Python/FastAPI)
- FastAPI for API endpoints
- Ollama integration with qwen2.5:7b (GPU-accelerated)
- Wikipedia API for content

### Frontend (Streamlit)
- Simple web interface
- Direct integration with FastAPI backend

## ReAct Framework Implementation

### Tools
- `search_wikipedia`: Fetch and parse Wikipedia articles
- `summarize_text`: Simplify English to 9-year-old level
- `translate`: Convert to N5-level Japanese
- `extract_vocab`: Generate vocabulary and kanji lists

### Agent Workflow
1. Observe: Get user topic input
2. Think: Plan sequence of tool calls
3. Act: Execute tools in optimal order
4. Repeat: Until all content is processed

### Prompt Templates
- Simplification: Guide for text simplification
- Translation: Instructions for N5-level Japanese
- Vocabulary: Rules for term extraction

## Core Components

### LLM Pipeline (Ollama)
- Model: qwen2.5:7b (chosen for Japanese language support)
- Tasks:
  - Text simplification
  - Japanese translation (N5 level)
  - Vocabulary extraction
  - Kanji identification

### External Services
- Wikipedia API: Article fetching

## API Endpoints

### `/api/v1/topic`
- POST: Create translation job
  ```json
  {
    "english_text": "Text to translate"
  }
  ```
- Returns: Job ID

### `/api/v1/topic/<job_id>`
- GET: Get job status and results
  ```json
  {
    "status": "complete",
    "result": {
      "translation": {
        "english": "Original text",
        "japanese": "Japanese translation"
      },
      "vocabulary": [
        {
          "word": "単語",
          "reading": "たんご",
          "romaji": "tango",
          "meaning": "word"
        }
      ]
    }
  }
  ```

## Development Steps
1. Set up Ollama with GPU support
2. Implement FastAPI backend
3. Create Streamlit frontend
4. Connect components
