# Implementation Tasks

## Task 1: Backend Word Service
**Description:**  
Implement the basic FastAPI backend service with word dictionary and random word generation.

**Acceptance Criteria:**
- [x] Create kana word dictionary with at least 20 basic words
- [x] Implement FastAPI endpoint GET /word/random
- [x] Response includes both kana and romaji
- [x] Words are properly randomized
- [x] Error handling for service unavailability
- [x] Basic unit tests for word generation

## Task 2: Streamlit Frontend
**Description:**  
Create the user interface with drawing capabilities and API integration. Initially implement with mock OCR responses to test the flow.

**Acceptance Criteria:**
- [ ] Implement drawing canvas
- [ ] Add clear canvas functionality
- [ ] Display current word to draw
- [ ] Implement submit button
- [ ] Show match/no match feedback (initially with mock responses)
- [ ] Add "next word" button
- [ ] Test cross-browser compatibility
- [ ] Verify canvas resolution is sufficient for OCR
- [ ] Add loading states for API calls
- [ ] Basic error handling for API failures

## Task 3: Drawing Recognition Service
**Description:**  
After basic frontend-backend flow is working, implement the OCR service using MangaOCR to process submitted drawings.

**Acceptance Criteria:**
- [ ] Set up MangaOCR integration
- [ ] Implement POST /submit endpoint with real OCR
- [ ] Handle base64 image processing
- [ ] Implement text matching logic
- [ ] Proper error handling for invalid images
- [ ] Test with various image qualities
- [ ] Response time under 2 seconds
- [ ] Add fallback mechanism for OCR failures
