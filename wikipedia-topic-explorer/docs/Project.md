# Technical Specification

## Project Structure
wikipedia-topic-explorer/
├── tools/                    # ReAct framework tools
│   ├── search_wikipedia.py   # Wikipedia article search and fetch
│   ├── summarize_text.py     # Text simplification
│   ├── translate_text.py     # Japanese translation
│   ├── extract_vocab.py      # Vocabulary extraction
│   └── search_images.py      # DuckDuckGo image search
├── prompts/                  # LLM prompt templates
│   ├── simplify.txt         # Text simplification prompt
│   ├── translate.txt        # Japanese translation prompt
│   └── vocabulary.txt       # Vocabulary extraction prompt
├── agent.py                 # Main ReAct agent implementation
├── api.py                   # FastAPI application
└── frontend.py             # Streamlit interface

## Architecture

### Backend (Python/FastAPI)
- FastAPI for API endpoints
- Ollama integration with llama2 3b (GPU-accelerated)
- Wikipedia API for content
- DuckDuckGo API for images

### Frontend (Streamlit)
- Simple web interface
- Direct integration with FastAPI backend

## ReAct Framework Implementation

### Tools
- `search_wikipedia`: Fetch and parse Wikipedia articles
- `summarize_text`: Simplify English to 9-year-old level
- `translate_text`: Convert to N5-level Japanese
- `extract_vocab`: Generate vocabulary and kanji lists
- `search_images`: Find relevant topic images

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
- Model: llama2 3b
- Tasks:
  - Text simplification
  - Japanese translation (N5 level)
  - Vocabulary extraction
  - Kanji identification

### External Services
- Wikipedia API: Article fetching
- DuckDuckGo API: Image search

## API Endpoints

### `/api/v1/topic`
- POST: New topic submission
- Returns: Job ID

### `/api/v1/status/<job_id>`
- GET: Processing status

### `/api/v1/result/<job_id>`
- GET: Final results

## Development Steps
1. Set up Ollama with GPU support
2. Implement FastAPI backend
3. Create Streamlit frontend
4. Integrate external APIs
5. Connect components
