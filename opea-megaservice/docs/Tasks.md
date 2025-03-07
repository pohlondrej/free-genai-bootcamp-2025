# Action Plan

## Tasks

### 1. Project Setup and Exploration [COMPLETED] 

- [x] Document project structure and components
- [x] Identify models used (Meta-Llama-3-8B-Instruct and TII Falcon2-11B)
- [x] Map out key components and their interactions
- [x] Document findings in `Learnings.md`
- [x] Evaluate vLLM compatibility
  - Confirmed vLLM is the default LLM backend
  - Found CPU-specific Dockerfile
  - Documented memory requirements
  - Identified optimization possibilities

### 2. vLLM CPU Adaptation [IN PROGRESS] 

- [x] Analyze base configuration
  - Default shared memory: 128GB
  - Uses OPEA's CPU-optimized image
  - Found health check endpoints
  - Documented environment variables
- [x] Research optimization options
  - Identified quantization possibilities
  - Found CPU-specific settings
  - Located command line options
  - Noted memory tuning parameters
- [ ] Document deployment requirements
  - Minimum memory requirements
  - CPU-specific optimizations
  - Quantization support
  - Performance implications
- [ ] Test deployment
  - Start with basic services
  - Try reduced memory
  - Monitor performance
  - Document findings

### 3. Documentation [NOT STARTED]

- [ ] Document setup process
- [ ] Create troubleshooting guide
- [ ] Add performance notes
- [ ] Write deployment instructions

## Current State Summary

### Key Components Identified:
1. Entry Point: `chatqna.py`
2. Docker Configuration: `intel/cpu/xeon/compose.yaml`
3. Frontend: `ui` directory
4. Build Instructions: `docker_image_build/build.yaml`

### Architecture Understanding:
1. Mega Service Pattern with multiple microservices:
   - Embedding Service (port 6000)
   - Retriever Service (port 7000)
   - Rerank Service (port 8000)
   - LLM Service (port 9000)
   - Main Orchestrator (port 8888)

### Key Findings:
1. vLLM is already the default LLM backend
2. Uses Meta-Llama-3-8B-Instruct model by default
3. OpenAI-compatible API interface
4. Well-structured modular architecture
