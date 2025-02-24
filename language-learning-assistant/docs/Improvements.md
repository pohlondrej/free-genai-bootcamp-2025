# Improvements
## 1: Japanese Language Quality Improvements
### Description:
Implement additional validation and quality controls for Japanese language output.
- Add validation for kanji/kana mix appropriate for beginners
- Implement JLPT level checking
- Verify vocabulary usage in generated content
- Add grammar pattern validation
- Enhance question generation with difficulty controls

### Acceptance Criteria:
- Japanese text follows appropriate difficulty level
- Vocabulary words actually appear in monologues
- Questions are properly formulated
- Grammar patterns match target level

### Technical Notes:
- Consider using existing Japanese language processing libraries
- May require additional language models or APIs
- Should not significantly impact response time
- Can be implemented incrementally

## 2: Scene Image Generation
### Description:
Add image generation to create visual context for each learning scenario.
- Integrate with an image generation model (e.g., DALL-E, Stable Diffusion)
- Generate scene image when creating new session
- Display image during vocabulary stage
- Cache generated images for reuse

### Acceptance Criteria:
- Image is generated for each unique scenario
- Generation happens during session creation
- Images are cached and reused for similar scenarios
- Loading states handle image generation time

### Technical Notes:
- Consider using OpenAI DALL-E or local Stable Diffusion
- Should handle failed image generation gracefully
- Should implement image caching similar to audio caching

## 3: Multi-Language Support
### Description:
Add support for multiple source and target languages in the learning sessions.
- Add language selection UI
- Make prompts language-agnostic
- Support multiple TTS models for different languages
- Handle different writing systems appropriately
- Implement language-specific validators
- Add language tags to vector database entries

### Acceptance Criteria:
- Users can select source and target languages
- LLM generates appropriate content for selected languages
- TTS works for all supported languages
- RAG finds relevant examples in correct languages
- Error handling for unsupported language pairs

### Technical Notes:
- May need different LLM models for certain languages
- Consider using language-specific embeddings
- TTS model selection based on language
- Should consider right-to-left scripts
- Need to validate language-specific character sets
- Consider using ISO language codes

## 4: WaniKani Integration
### Description:
Integrate with WaniKani API to personalize content based on user's known kanji and vocabulary.
- Add WaniKani API key configuration
- Fetch and cache user's known items
- Filter LLM output to match user level
- Include progress-appropriate kanji
- Respect user's current learning level
- Update content as user progresses

### Acceptance Criteria:
- Content uses only known kanji/vocabulary
- Vocabulary matches WaniKani level
- Content updates with WaniKani progress
- Graceful fallback if API is unavailable

### Technical Notes:
- Use official WaniKani V2 API
- Cache API responses to respect rate limits
- Store user's known items in local DB
- Add kanji/vocabulary filters to LLM prompts
- Should refresh cache periodically
