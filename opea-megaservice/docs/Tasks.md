# Action Plan

## Tasks

### 1. Project Setup and Exploration [COMPLETED] 

- [x] Document project structure and components
- [x] Identify models used (Meta-Llama-3-8B-Instruct and TII Falcon2-11B)
- [x] Map out key components and their interactions
- [x] Document findings in `Learnings.md`
- [x] Evaluate vLLM compatibility
  - Confirmed vLLM is the default LLM backend
  - Must build from source for CPU deployment
  - Base image: Ubuntu 22.04

### 2. vLLM CPU Adaptation [COMPLETED] 

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

### 3. Documentation [COMPLETED]

- [x] Document setup process (in README.md)
- [x] Create troubleshooting guide (in Learnings.md)
- [x] Add performance notes (in README.md)
- [x] Write deployment instructions (in README.md)

### 4. Next Steps [TODO]

- [ ] Fix UI routing issues:
  - Investigate /v1/chatqna 404 error
  - Check NGINX configuration
  - Verify backend service paths
- [ ] Investigate retriever service:
  - Test document retrieval functionality
  - Verify Redis vector DB integration
  - Check embedding service connection
- [ ] Performance optimization:
  - Monitor memory usage with reduced VLLM_SHM_SIZE
  - Test different batch sizes
  - Document optimal configuration

## Current State Summary

### Key Components Identified:
1. Layered Architecture:
   - First Layer: Base services (Redis)
   - Second Layer: Core services (Embedding, Reranking)
   - Third Layer: Backend services (ChatQnA, vLLM)
   - Fourth Layer: UI services (Frontend, NGINX)
2. Docker Configuration: Layer-specific compose files
3. Environment Files: Layer-specific configurations
4. vLLM: CPU-optimized build from source

### Architecture Understanding:
1. Mega Service Pattern with multiple microservices:
   - Embedding Service
   - Retriever Service
   - Rerank Service
   - vLLM Service (CPU-optimized)
   - ChatQnA Backend
   - UI and NGINX

### Key Findings:
1. vLLM successfully running with CPU optimizations
2. All services containerized and running
3. UI needs routing fixes
4. Retriever functionality needs verification
5. Memory requirements can be reduced (16GB tested)
