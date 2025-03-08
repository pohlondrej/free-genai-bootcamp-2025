# Learnings
## Key Knowledge Gaps
### Docker Compose Fundamentals
Instead of diving deep into advanced Docker features, concentrate on mastering Docker Compose. This is the key to orchestrating the megaservice.
#### Goals
- Understand how to define services in docker-compose.yml.
- Learn how to link services together using depends_on and networks.
- Become comfortable with mounting volumes to share data between containers (essential for model weights).
- Learn how to set environment variables inside of the docker-compose.yml file.

#### Why
This will allow me to quickly modify the OPEA project's service definitions and adapt them to the CPU-based setup.

### vLLM Basic Usage
Focus on getting vLLM running in CPU mode within a Docker container.
#### Goals
- Understand the basic command-line options for vLLM, particularly --disable-gpu and --model.
- Learn how to load the desired model weights into the vLLM container.
- Test that the vLLM container is working by sending it basic requests.
#### Why
This is the core component that will replace the GPU-optimized LLM serving in the OPEA project.

### Model Weight Management
Ensure a reliable way to access and manage the model weights for vLLM.
#### Goals
- Understand how to download and store model weights.
- Learn how to mount model weights into the vLLM Docker container using volumes.
- Test that the model weights are being loaded correctly by vLLM.
#### Why
Without the correct model weights, vLLM will be useless.

### OPEA Project Structure (Superficial)
Don't try to understand every detail of the OPEA project.
#### Goals
- Focus on identifying the docker-compose.yml file and the Dockerfiles for the LLM serving containers.
- Try to understand the overall architecture of the mega service, but don't get bogged down in the details.

#### Why
Provide the context to make the necessary modifications without wasting time on irrelevant details.

## Things to Avoid

*   **Advanced Docker Features (initially):**
    *   Avoid complex networking, multi-stage builds, etc.
*   **Deep OPEA Code Analysis:**
    *   Resist delving into intricate internal workings.
*   **Premature Performance Optimization:**
    *   Focus on functionality first.
*   **Troubleshooting Complex Dependencies:**
    *   Simplify or find alternatives.
*   **Prematurely using Kubernetes:**
    *   Stick to docker compose.

## Lessons Learned

### Entry Template
[YYYY-MM-DD HH:MM] Context: [Setup/Analysis/Implementation/Issue]
- What was attempted
- What was learned
- Any blockers or solutions found
- References to relevant files or documentation

### First Entry
[2024-01-09 10:00] Context: Setup
- Established project structure and documentation guidelines
- Confirmed read-only status of reference directories
- Set up learning documentation format
- Ready to begin ChatQnA analysis

### Entries

#### [2024-01-09 10:15] Context: Analysis
- Initial exploration of ChatQnA example in `GenAIExamples` directory.

#### [2024-01-09 10:30] Context: Analysis
- Corrected initial analysis; required access to ChatQnA directory.
- Request: Access to `GenAIExamples/ChatQnA/` directory contents.

#### [2024-01-09 10:45] Context: Setup
- ChatQnA example moved to `ChatQnAExample/` in root.
- `GenAIExamples` directory removed.

#### [2024-01-09 11:00 - 11:30] Context: Analysis
- Repeated blocker: Unable to access `ChatQnAExample/` directory contents.
- Request: Access to directory contents.

#### [2024-01-09 11:45] Context: Analysis
- Success: Access to `ChatQnAExample/chatqna.py`.
- Findings:
  - FastAPI backend.
  - LLM: `LLM_MODEL = "meta-llama/Meta-Llama-3-8B-Instruct"`.
  - Microservices architecture (embedding, retriever, rerank, LLM).
  - OpenAI-compatible API (`/v1/chat/completions`).
  - Configurable environment variables: `HOST_IP`, `PORT`, `LLM_MODEL`.

#### [2024-01-09 12:00] Context: Analysis
- Blocked: Expected `README.md` and `docker-compose.yml` not visible.
- Request: Access to `README.md`, `docker-compose.yml`, and other configuration files.

#### [2024-01-09 12:15] Context: Analysis
- Success: Full directory structure visible.
- Key findings from `README.md`:
  - RAG-based chatbot.
  - Multiple deployment options (Gaudi2, Xeon, NVIDIA, AMD).
  - Default model: `meta-llama/Meta-Llama-3-8B-Instruct`.
  - CPU deployment path: `docker_compose/intel/cpu/xeon/`.
- Next steps:
  - Locate CPU-specific compose file.
  - Understand component interactions.
  - Plan vLLM integration points.

#### [2024-01-09 12:30] Context: Analysis
- Partial access: Missing CPU-specific deployment files, architecture diagrams, and other deployment files.
- Next steps: Access CPU files, focus on Xeon configuration, compare GPU vs CPU.

#### [2024-01-09 12:45] Context: Analysis
- Models used: `Meta-Llama-3-8B-Instruct` and `TII Falcon2-11B`.

#### [2024-01-09 12:50] Context: Architecture Analysis
- Microservices architecture:
  - Vector DB (Redis): Port 6379 (Redis), 8001 (RedisInsight).
  - Data Preparation: Port 6007.
  - Text Embedding: Port 6006.
  - Retriever: Port 7000.
  - Reranking: Port 8808.
  - Ollama LLM: Port 11434.
  - Main Backend: Port 8888.
- RAG pattern.
- All services CPU-configured.

#### [2024-01-09 12:55] Context: Service Configuration
- Key environment variables:
  - `EMBEDDING_MODEL_ID`: Text embedding model.
  - `RERANK_MODEL_ID`: Reranking model.
  - `OLLAMA_MODEL`: LLM model selection.
  - `INDEX_NAME`: Redis vector store.
  - `HUGGINGFACEHUB_API_TOKEN`: Model access.

#### [2024-01-09 12:55] Context: Hardware Considerations
- Focus on `intel/cpu/xeon` as base, adapt for AMD using vLLM.

#### [2024-01-09 13:00] Context: Xeon Configuration Analysis
- Xeon configuration uses Redis, Milvus, Pinecone, Qdrant, Ollama, TGI, and vLLM.
- TGI as reference for vLLM adaptation.
- Additional environment variables:
  - `MODEL_CACHE`: Model weights storage.
  - `REGISTRY`: Container image registry.
  - `TAG`: Container image versions.

#### [2024-01-09 13:05] Context: Configuration Correction
- Xeon default uses vLLM, not TGI. Aligns with project goals.

#### [2024-01-09 13:10] Context: Environment Configuration
- Default models:
  - `LLM_MODEL_ID`: `meta-llama/Meta-Llama-3-8B-Instruct`.
  - `EMBEDDING_MODEL_ID`: `BAAI/bge-base-en-v1.5`.
  - `RERANK_MODEL_ID`: `BAAI/bge-reranker-base`.
- Redis vector store: `INDEX_NAME = "rag-redis"`.
- Optional features: `LOGFLAG` (logging), OpenTelemetry tracing.

#### [2024-01-09 13:15] Context: Mega Service Architecture Analysis
- Service Orchestrator pattern:
  - Embedding Service: Port 6000.
  - Retriever Service: Port 7000.
  - Rerank Service: Port 8000.
  - LLM Service: Port 9000.
  - Mega Service: Port 8888.
- Service Flow: embedding -> retriever -> rerank -> llm
- LLM parameters: `max_tokens`, `temperature`, `repetition_penalty`.
- Retriever parameters: `search_type`, `k`, `fetch_k`, `score_threshold`.

#### [2024-01-09 13:20] Context: Request Flow Analysis
- OpenAI-compatible request/response.
- Streaming and non-streaming support.
- Mega service as RAG pipeline facade.

#### [2024-01-09 13:25] Context: UI Analysis
- Svelte UI (default): Port 5173.
- React UI (alternative).
- Svelte UI simpler for testing.

#### [2024-01-09 13:30] Context: Build System Analysis
- `docker_image_build/build.yaml` for building service images.
- Use pre-built OPEA registry images.

#### [2024-01-09 13:35] Context: Environment Configuration Analysis
- Key environment variables from `set_env.sh`:
  - `EMBEDDING_MODEL_ID`, `RERANK_MODEL_ID`, `LLM_MODEL_ID`, `INDEX_NAME`, `LOGFLAG`, `JAEGER_IP`.
- Missing parent `.set_env.sh` variables need investigation.

#### [2024-01-09 13:40] Context: vLLM Service Configuration
- vLLM service configuration:
  - Port: 9009:80.
  - OPEA registry image: `<span class="math-inline">\{REGISTRY\:\-opea\}/vllm\:</span>{TAG:-latest}`.
  - Resource requirements: `shm_size: 128g`, `MODEL_CACHE`.
  - Environment variables: `HF_TOKEN`, `LLM_MODEL_ID`, `VLLM_TORCH_PROFILER_DIR`.
  - Health check: `/health`.

#### [2024-01-09 13:40] Context: Required Environment Variables
- Essential variables: `HUGGINGFACEHUB_API_TOKEN`, `REGISTRY`, `TAG`, `MODEL_CACHE`, `LLM_MODEL_ID`, `host_ip`, `http_proxy`, `https_proxy`, `no_proxy`.

#### [2024-01-09 13:55] Context: vLLM Memory Analysis
- vLLM memory requirements: 128GB default, but 16GB might be enough.

#### [2024-01-09 14:00] Context: vLLM CPU Optimization
- vLLM CPU optimization options and OPEA's CPU implementation.
