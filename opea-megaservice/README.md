# OPEA Mega Service

An adapted version of the OPEA ChatQnA service optimized for CPU deployment using vLLM.

## Project Goals
* Document the learning process and understanding of mega services architecture
* Successfully run the adapted service or document valuable learnings trying to do so

## Project Layout

*   `GenAIComps/`: Original OPEA GenAI Comps project (Read-only)
*   `ChatQnAExample/`: Original ChatQnA example implementation (Read-only)
*   `vllm/`: vLLM source code for CPU-optimized build (Read-only)
*   `work_directory/`: Active development directory
    - `.set_env.*.sh`: Environment files for different layers
    - `docker_compose/intel/cpu/xeon/`: Docker Compose files for each layer
*   `docs/`: Project documentation
    - [Tasks.md](docs/Tasks.md): Project action plan and progress
    - [Learnings.md](docs/Learnings.md): Documented learnings and insights
    - [Rules.md](docs/Rules.md): Project guidelines and constraints

## Key Technologies

* **GenAIComps & Examples:** Reference projects containing the original OPEA implementation (Read-only source code)
* **Docker:** Containerization platform for packaging and deploying applications
* **Docker Compose:** Tool for orchestrating multi-container Docker applications
* **vLLM:** High-throughput and memory-efficient LLM inference engine (CPU compatible)

### vLLM CPU Requirements
- Must build from source following official guide; working Dockerfile is in docker_image_build/vllm/Dockerfile
- Base image: Ubuntu 22.04
- Dependencies:
  - torch==2.3.1+cpu from PyTorch repo
  - torchvision==0.18.1+cpu from PyTorch repo
  - python3-dev and build-essential
- Memory configuration:
  - 16GB RAM (down from 128GB default)
- Tested models:
  - Qwen/Qwen2.5-0.5B-Instruct; should be changed to Meta-Llama-3-8B-Instruct in production
  - BAAI/bge-base-en-v1.5 (for embedding)
  - BAAI/bge-reranker-base (for reranking)

### Architecture
The service uses a layered architecture pattern:

1. `*base*` (core services, no dependencies)
   - Redis
   - Embedding service
   - vLLM service (CPU-optimized)

2. `*second_layer*` (data services, depends on base)
   - Reranking service (depends on embedding service)
   - Dataprep service (depends on embedding service and Redis)
   - Retriever service (depends on Redis)

3. `*third_layer*` (backend service, depends on first and second layers)
   - ChatQnA backend server

4. `*fourth_layer*` (ui services, depends on backend service)
   - Frontend UI server
   - NGINX for routing and proxying

Each layer has its own:
- Environment file (.set_env.*.sh)
- Docker Compose configuration

### Current Status and Next Steps

1. UI Integration [COMPLETED]:
   - Fixed routing issues by using localhost URLs
   - UI successfully communicates with backend
   - All requests routed through NGINX

2. Retriever Service [COMPLETED]:
   - Document retrieval needs testing
   - Redis vector DB integration needs verification
   - Embedding service connection check needed