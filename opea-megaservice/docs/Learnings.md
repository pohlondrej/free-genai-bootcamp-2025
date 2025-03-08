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

#### [2025-03-08 22:30] Context: Project Structure
##### `.set_env.sh` (root level)
- Core variables: HUGGINGFACEHUB_API_TOKEN, REGISTRY, TAG, host_ip
- Model: meta-llama/Meta-Llama-3-8B-Instruct
- Memory settings: VLLM_SHM_SIZE=32g (reduced from 128GB)
- CPU optimization: VLLM_CPU_OMP_THREADS_BIND=1
- Memory optimization: VLLM_QUANTIZATION="fp8"
##### `requirements.txt`
- Core: fastapi, uvicorn, vllm>=0.2.7
- RAG: redis, langchain, transformers
- Models: BAAI/bge-base-en-v1.5, BAAI/bge-reranker-base
##### Existing files from ChatQnAExample
- chatqna.py: Main service implementation
- chatqna_wrapper.py: Service wrapper
- docker_compose/intel/cpu/xeon/: Base configuration

#### [2025-03-08 22:35] Context: Testing Strategy
- Start with standalone vLLM service
  - Test with 32GB shared memory + FP8 quantization
  - Validate basic inference works

#### [2025-03-08 22:40] Context: vLLM Test Configuration
- Created minimal test configuration in `compose.vllm.yaml`:
- Single service deployment
- Port 9009:80 for API access
- Model cache mounted from host

#### [2025-03-08 22:55] Context: vLLM Initial Test
- Testing vLLM service with:
  - Model: meta-llama/Meta-Llama-3-8B-Instruct
  - Memory: 16GB shared memory
  - Quantization: FP8 for reduced memory usage
  - Max batched tokens: 2048
- ISSUE: `--cpu-memory-utilization` parameter not supported in vLLM API server
  - Removed parameter from compose.vllm.yaml
  - Will rely on default memory management

#### [2025-03-08 23:05] Context: Model Access Requirements
- IMPORTANT: meta-llama/Meta-Llama-3-8B-Instruct requires explicit access approval
  - Need to register at huggingface.co and request access
  - URL: https://huggingface.co/meta-llama/Meta-Llama-3-8B-Instruct
  - Access token alone is not sufficient, need to be on authorized list
  - Error 403 will occur until access is granted
- ALTERNATIVE: TII Falcon2-11B is openly available
  - Model: tiiuae/falcon-11B
  - No special access requirements

#### [2025-03-08 23:15] Context: Model Selection Update
- PROBLEM: Access to meta-llama/Meta-Llama-3-8B-Instruct denied
- DECISION: Switching to Falcon3-7B-Base for initial vLLMtesting
  - Advantages over Falcon2-11B:
    - Smaller size (7B vs 11B parameters)
    - GQA for faster inference
  - Memory benefits:
    - 7B model should work better with 16GB shared memory

#### [2025-03-08 23:25] Context: vLLM Configuration Issues
- ISSUE 1: Token batch size must match model context length
  - Falcon3-7B-Base has 32k context length
  - Initial setting (2048) was too small
  - Fixed by setting max_num_batched_tokens to 32768
  - Learning: Always match max_num_batched_tokens to model's context length

- ISSUE 2: vLLM Docker image may be GPU-focused
  - Error: "Triton not installed... GPU functions not available"
  - Exit code 132 suggests memory-related crash
  - Hypothesis: Default image might be GPU-optimized

#### [2025-03-08 23:45] Context: vLLM CPU Compatibility Resolution
- ROOT CAUSE: vLLM CPU Support Issues
  - Pre-built vLLM in OPEA docker image not compatible with CPU
  - Same issue when running vLLM directly outside Docker
  - Not a model size or timeout issue as initially suspected

- SOLUTION: Build vLLM from Source
  1. Follow official docs: https://docs.vllm.ai/en/latest/getting_started/installation/cpu/
  2. Critical Dependencies:
     - pytorch-cpu
     - torchvision-cpu
  3. Build vLLM from source for CPU compatibility

- IMPLICATIONS:
  1. Need to modify OPEA build process
  2. Cannot use pre-built vLLM packages
  3. Must ensure CPU-specific PyTorch is used

- NEXT STEPS:
  1. Update Docker build to compile vLLM from source
  2. Ensure correct CPU dependencies are included
  3. Test with project's target models (Falcon2-11B or Meta-Llama-3-8B-Instruct)

#### [2025-03-09 00:00] Context: Hardware-Specific Configuration
- HARDWARE SPECS:
  - CPU: 6 cores, 12 threads
  - RAM: 32GB total
  - Allocation:
    - vLLM shared memory: 16GB (half of total RAM)
    - Physical cores: All 6 cores allocated
    - Thread binding: Enabled for better performance

- CRITICAL CHANGES:
  1. Removed FP8 quantization (not supported on CPU)
  2. Thread Configuration:
     - OMP_NUM_THREADS=6 (match physical cores)
     - MKL_NUM_THREADS=6 (match physical cores)

#### [2025-03-09 00:15] Context: vLLM CPU Compatibility
- PROGRESS: Removed quantization helped
  - CPU doesn't support 8-bit FP operations
  - Default bfloat16 might also be problematic

- NEW FINDINGS:
  1. Data Type Issues:
     - Changed to float32 for maximum compatibility
     - Removed bfloat16 to avoid CPU instruction issues
  2. Async Processing:
     - Disabled async output processing
     - Added SDPA CPU fallback
     - Enabled eager mode to avoid JIT complications

#### [2025-03-09 00:40] Context: Model Loading Timeouts
- FINDING: Initial error was due to model loading timeout
  - CPU loading of 7B model takes significant time
  - Default timeouts too short for CPU loading

#### [2025-03-09 00:45] Context: Debugging with Smaller Model
- APPROACH: Test with falcon-rw-1b (1B parameters)
  - Smaller model for faster loading
  - Same architecture as project models
  - Will help validate CPU setup

- CONFIGURATION CLEANUP:
  1. Removed unverified environment variables
  2. Kept essential CPU settings:
     - Thread binding and counts
     - AVX support
     - Async processing disabled
  3. Healthcheck:
     - 5 minute start period (1B model)
     - 30s intervals and timeouts

#### [2025-03-09 00:50] Context: Testing with Minimal Model
- APPROACH: Test with Qwen2.5-0.5B-Instruct
  - Even smaller model (0.5B parameters)
  - Should load much faster than Falcon
  - Will help isolate if issue is model size dependent

#### [2025-03-09 10:30] Context: vLLM CPU Compatibility Resolution
- ROOT CAUSE: vLLM CPU Support Issues
  - Pre-built vLLM in OPEA docker image not compatible with CPU
  - Same issue when running vLLM directly outside Docker
  - Not a model size or timeout issue as initially suspected

- SOLUTION: Build vLLM from Source
  1. Follow official docs: https://docs.vllm.ai/en/latest/getting_started/installation/cpu/
  2. Critical Dependencies:
     - pytorch-cpu
     - torchvision-cpu
  3. Build vLLM from source for CPU compatibility
