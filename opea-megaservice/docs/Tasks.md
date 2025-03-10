# Tasks

## 1. Project Setup and Exploration [COMPLETED] 

- [x] Document project structure and components
- [x] Identify models used (Meta-Llama-3-8B-Instruct and TII Falcon2-11B)
- [x] Map out key components and their interactions
- [x] Document findings in `Learnings.md`
- [x] Evaluate vLLM compatibility
  - Confirmed vLLM is the default LLM backend
  - Must build from source for CPU deployment
  - Base image: Ubuntu 22.04

## 2. vLLM CPU Adaptation [COMPLETED] 

- [x] Analyze base configuration
  - Default shared memory: 128GB
  - Uses OPEA's CPU-optimized image
  - Documented environment variables
- [x] Research optimization options
  - Identified CPU-specific dependencies
  - Found PyTorch CPU packages
  - Located build requirements
- [x] Document deployment requirements
  - torch==2.3.1+cpu from PyTorch repo
  - torchvision==0.18.1+cpu from PyTorch repo
  - Memory configurable via VLLM_SHM_SIZE
- [x] Test deployment
  - Successfully started all layers
  - Configured reduced memory (16GB)
  - Services running but need UI fixes
  - Documented findings in Learnings.md

## 3. Documentation [COMPLETED]

- [x] Document setup process (in README.md)
- [x] Create troubleshooting guide (in Learnings.md)
- [x] Add performance notes (in README.md)
- [x] Write deployment instructions (in README.md)

## 4. Next Steps [IN PROGRESS]

- [x] Fix UI routing issues:
  - Fixed /v1/chatqna 404 error by using localhost URLs
  - Resolved CORS issues by making same-origin requests
  - UI now successfully communicates with backend
- [x] Investigate retriever service:
  - Confirmed document retrieval functionality
  - Verified Redis vector DB integration
  - Embedding service working (768-dim vectors)
  - Reranking configured (fetch_k=20)
- [ ] Performance optimization:
  - Monitor memory usage with reduced VLLM_SHM_SIZE
  - Test different batch sizes
  - Document optimal configuration
