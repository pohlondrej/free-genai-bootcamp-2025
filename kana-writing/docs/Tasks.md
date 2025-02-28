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
- [x] Implement drawing canvas
- [x] Add clear canvas functionality
- [x] Display current word to draw
- [x] Implement submit button
- [x] Show match/no match feedback (initially with mock responses)
- [x] Add "next word" button
- [x] Test cross-browser compatibility
- [x] Verify canvas resolution is sufficient for OCR
- [x] Add loading states for API calls
- [x] Basic error handling for API failures

## Task 3: Drawing Recognition Service
**Description:**  
After basic frontend-backend flow is working, implement the OCR service using MangaOCR to process submitted drawings.

**Acceptance Criteria:**
- [x] Set up MangaOCR integration
- [x] Implement POST /submit endpoint with real OCR
- [x] Handle base64 image processing
- [x] Implement text matching logic
- [x] Proper error handling for invalid images
- [x] Test with various image qualities
- [x] Response time under 2 seconds
- [x] Add fallback mechanism for OCR failures
