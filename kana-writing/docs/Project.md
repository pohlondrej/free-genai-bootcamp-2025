# Project Description

This prototype implements a Japanese kana writing practice application using Python. The system consists of a FastAPI backend that serves random kana words and processes user-drawn characters using MangaOCR for recognition. The frontend, built with Streamlit, provides a simple drawing interface where users can practice writing kana characters and receive feedback on their accuracy.

The application follows a minimalist approach with no persistent storage, focusing on the core functionality of word generation, character drawing, and OCR-based verification.

## Technical Uncertainties
- MangaOCR accuracy with hand-drawn input vs. printed text
- Canvas drawing quality and resolution requirements for accurate OCR
- Handling different writing styles and stroke orders

## Technical Requirements

### Backend (Python)
- FastAPI for REST API
- MangaOCR integration for character recognition
- Kana word dictionary
- API endpoints:
  - GET /word/random - Get random word
  - POST /submit - Submit drawing for evaluation

### Frontend (Python)
- Streamlit for UI
- HTML5 Canvas for drawing
- Components:
  - Word display
  - Drawing canvas
  - Clear canvas button
  - Submit button
  - Right/Wrong feedback display
  - Next word button

### Data Requirements
- Kana-only word dictionary (loaded in memory)
- Drawing submission format: PNG/JPEG

## Technical Architecture
```
Frontend (Streamlit) <-> Backend (FastAPI) <-> MangaOCR
```

## API Specification

### GET /word/random
Get a random word for practice.

Response:
```json
{
    "word": {
        "kana": "ひらがな",
        "romaji": "hiragana"
    }
}
```

### POST /submit
Submit a drawing for evaluation.

Request:
```json
{
    "image": "base64_encoded_image_data",
    "expected_word": "ひらがな"
}
```

Response:
```json
{
    "match": true,
    "detected_text": "ひらがな"
}
```

### Error Response Format
```json
{
    "error": "error_code",
    "message": "Human readable error message"
}
```

## Risks
1. OCR accuracy might be insufficient for hand-drawn input
2. Canvas drawing quality might affect recognition
3. Limited word dictionary might affect user engagement

## Success Metrics
- OCR basic recognition rate (match/no match)
- System response time < 2 seconds
