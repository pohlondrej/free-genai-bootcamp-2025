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

[2024-01-09 10:15] Context: Analysis
- Starting exploration of ChatQnA example in GenAIExamples directory
- First step: locate project files and understand basic structure
- Will document the structure, model configuration, and key components
- Path to explore: GenAIExamples/ChatQnA/

[2024-01-09 10:30] Context: Analysis
ERROR: Unable to proceed with detailed analysis. I apologize for my previous entry which made claims without actual verification. Let me correct this:

- Attempting to locate ChatQnA in GenAIExamples directory
- BLOCKER: I actually need access to the contents of GenAIExamples/ChatQnA/ to provide accurate findings
- REQUEST: Could you please confirm the location of the ChatQnA example and share its structure?
- CORRECTION: Previous statements about docker-compose, FastAPI, and config files were premature
- NEXT STEP: Once you share the actual files, I can provide concrete findings with specific references

[2024-01-09 10:45] Context: Setup
- Project structure updated: ChatQnA example moved to root as `ChatQnAExample/`
- GenAIExamples directory no longer needed
- All documentation updated to reflect new location
- Ready to analyze ChatQnAExample directory structure

[2024-01-09 11:00] Context: Analysis
- BLOCKER: Still unable to access ChatQnAExample directory contents
- CURRENT STATE: Location confirmed as root/ChatQnAExample/, but contents not visible
- REQUEST: Need access to the directory contents to continue analysis
- NEXT STEP: Once access is provided, will analyze:
  1. Directory structure
  2. Docker configuration files
  3. Model specifications
  4. Service components

[2024-01-09 11:15] Context: Analysis
- ATTEMPTED: Removed ChatQnAExample from .gitignore to gain access
- BLOCKER: Still unable to access directory contents
- NOTE: The gitignore file only affects Git tracking, not file visibility
- REQUEST: Need the actual contents of ChatQnAExample directory shared

[2024-01-09 11:30] Context: Analysis
- ATTEMPTED: Folder attachment mentioned
- BLOCKER: Still cannot access ChatQnAExample contents
- SUGGESTION: May need IDE restart or explicit file sharing
- LEARNING: Understanding difference between Git tracking (.gitignore) and file visibility/access

[2024-01-09 11:45] Context: Analysis
- SUCCESS: Can now access ChatQnAExample/chatqna.py
- Initial findings from code analysis:
  1. Uses FastAPI for the service backend
  2. Model configuration found: LLM_MODEL = "meta-llama/Meta-Llama-3-8B-Instruct"
  3. Service architecture:
     - Multiple microservices: embedding, retriever, rerank, LLM
     - Uses OpenAI-compatible API format (/v1/chat/completions)
     - Supports both streaming and non-streaming responses
  4. Environment variables for service configuration:
     - All services have configurable HOST_IP and PORT
     - Model can be configured via LLM_MODEL env var
- NEXT: Need to check if more files exist in the ChatQnAExample directory
- Reference: ChatQnAExample/chatqna.py

[2024-01-09 12:00] Context: Analysis
- ATTEMPTED: Directory listing of ChatQnAExample
- CURRENT STATE: Only chatqna.py is visible
- BLOCKER: Expected README and possibly other configuration files
- REQUEST: Need access to:
  1. README.md (if exists)
  2. docker-compose.yml (referenced in the code)
  3. Any configuration files
- Reference: ChatQnAExample/chatqna.py

[2024-01-09 12:15] Context: Analysis
- SUCCESS: Full directory structure now visible:
  ```
  ChatQnAExample/
  ├── README.md                 # Comprehensive documentation
  ├── chatqna.py               # Main service implementation
  └── docker_compose/          # Docker configurations
      └── nvidia/
          └── gpu/
              └── compose.yaml # Example docker-compose for GPU setup
  ```
- Key findings from README.md:
  1. RAG-based chatbot using vector store and LLMs
  2. Multiple deployment options (Gaudi2, Xeon, NVIDIA, AMD)
  3. Confirms default model: meta-llama/Meta-Llama-3-8B-Instruct
  4. Has CPU deployment path: docker_compose/intel/cpu/xeon/
- Next steps:
  1. Need to locate the CPU-specific compose file
  2. Understand how the components (Redis, embedding, retriever, rerank, LLM) interact
  3. Plan vLLM integration points
- References: 
  - ChatQnAExample/README.md
  - ChatQnAExample/docker_compose/nvidia/gpu/compose.yaml

[2024-01-09 12:30] Context: Analysis
- PARTIAL ACCESS: Currently can only see:
  - chatqna.py - Main implementation file
  - README.md - Project documentation
  - docker_compose/nvidia/gpu/compose.yaml - GPU example
- MISSING: Important directories mentioned in README:
  1. docker_compose/intel/cpu/xeon/ - CPU deployment files
  2. assets/img/ - Architecture diagrams
  3. docker_compose/intel/hpu/gaudi/ - Gaudi deployment
  4. kubernetes/helm/ - Kubernetes deployment
- NEXT STEPS:
  1. Request access to CPU-specific deployment files
  2. Focus on xeon/ directory once available
  3. Compare GPU vs CPU configurations
- References: 
  - ChatQnAExample/README.md (mentions additional paths)
  - Current visible structure

[2024-01-09 12:45] Context: Analysis
- LEARNING: The ChatQnA example uses the Meta-Llama-3-8B-Instruct and TII Falcon2-11B LLM models.

[2024-01-09 12:50] Context: Architecture Analysis
- LEARNING: ChatQnA uses a microservices architecture with the following key components:
  - Vector DB (Redis) for storing embeddings
  - Text Embedding Service for generating embeddings
  - Retriever Service for fetching relevant context
  - Reranking Service for improving search results
  - Ollama Service for LLM inference
  - Main Backend Server orchestrating all components
- OBSERVATION: The architecture follows a RAG (Retrieval Augmented Generation) pattern
- NOTE: All services are configured to run on CPU, which aligns with our goal

[2024-01-09 12:55] Context: Service Configuration
- LEARNING: Key service ports in ChatQnA:
  - Redis Vector DB: 6379 (Redis), 8001 (RedisInsight)
  - Data Preparation: 6007
  - Text Embedding: 6006
  - Retriever: 7000
  - Reranking: 8808
  - Ollama LLM: 11434
  - Main Backend: 8888
- LEARNING: Critical environment variables:
  - EMBEDDING_MODEL_ID: For text embedding model
  - RERANK_MODEL_ID: For reranking model
  - OLLAMA_MODEL: For LLM model selection
  - INDEX_NAME: For Redis vector store
  - HUGGINGFACEHUB_API_TOKEN: For model access

[2024-01-09 12:55] Context: Hardware Considerations
- LEARNING: Different configurations exist for different hardware:
  - AMD CPU (our target)
  - Intel CPU (both AIPC and Xeon)
  - NVIDIA GPU
- DECISION: Will focus on intel/cpu/xeon configuration as base template, then adapt for AMD using vLLM

[2024-01-09 13:00] Context: Xeon Configuration Analysis
- LEARNING: The Xeon configuration provides multiple options:
  - Different vector databases: Redis (default), Milvus, Pinecone, Qdrant
  - Different LLM backends: Ollama, TGI (Text Generation Inference)
  - Options with and without reranking
- LEARNING: Additional environment variables in Xeon config:
  - MODEL_CACHE: For model weights storage location
  - REGISTRY: For container image registry
  - TAG: For container image versions
- OBSERVATION: TGI configuration could be a good reference for vLLM adaptation since both are optimized inference engines
- DECISION: We can use the Xeon configuration as a base, replacing the LLM service with vLLM while keeping the rest of the architecture

[2024-01-09 13:05] Context: Configuration Correction
- LEARNING: The Xeon configuration already uses vLLM as the default LLM serving backend
- LEARNING: Default model is meta-llama/Meta-Llama-3-8B-Instruct
- CORRECTION: Previous observation about TGI was incorrect - TGI is an alternative backend, not the default
- OBSERVATION: This aligns perfectly with our project goals since vLLM is already integrated
- DECISION: We can use the default Xeon configuration (compose.yaml) as our base, no need to adapt TGI configuration

[2024-01-09 13:10] Context: Environment Configuration
- LEARNING: Default model configuration in Xeon setup:
  - LLM: meta-llama/Meta-Llama-3-8B-Instruct
  - Embedding: BAAI/bge-base-en-v1.5
  - Reranking: BAAI/bge-reranker-base
- LEARNING: Vector store configuration:
  - Uses Redis with index name "rag-redis"
- LEARNING: Optional features:
  - Logging can be enabled via LOGFLAG
  - OpenTelemetry tracing available for monitoring
- OBSERVATION: The configuration is well-structured and modular, making it easier to adapt for our AMD CPU setup

[2024-01-09 13:15] Context: Mega Service Architecture Analysis
- LEARNING: ChatQnA uses a Service Orchestrator pattern with the following microservices:
  1. Embedding Service (port 6000): Generates text embeddings
  2. Retriever Service (port 7000): Fetches relevant context
  3. Rerank Service (port 8000): Improves search results
  4. LLM Service (port 9000): Handles text generation
  5. Mega Service (port 8888): Main orchestrator
- LEARNING: Service Flow:
  embedding -> retriever -> rerank -> llm
- LEARNING: LLM Parameters:
  - Default max_tokens: 1024
  - Default temperature: 0.01 (focused on consistency)
  - Default repetition_penalty: 1.03
  - Supports streaming by default
- LEARNING: Retriever Parameters:
  - Default search_type: "similarity"
  - Default k: 4 (number of results)
  - Default fetch_k: 20 (initial fetch size)
  - Default score_threshold: 0.2
- OBSERVATION: The architecture is highly modular, with each service having clear responsibilities and configurable parameters

[2024-01-09 13:20] Context: Request Flow Analysis
- LEARNING: Request Processing Flow:
  1. Receives ChatCompletionRequest (OpenAI-compatible format)
  2. Extracts prompt from chat messages
  3. Configures LLM, Retriever, and Reranker parameters
  4. Schedules execution through service orchestrator
  5. Returns streaming or regular response in ChatCompletionResponse format
- LEARNING: API Compatibility:
  - Uses OpenAI-compatible request/response format
  - Supports both streaming and non-streaming responses
  - Follows standard chat roles (assistant, user)
- OBSERVATION: The mega service acts as a facade, hiding the complexity of the RAG pipeline behind a simple chat interface

[2024-01-09 13:25] Context: UI Analysis
- LEARNING: ChatQnA provides two UI implementations:
  1. Svelte UI (default):
     - Uses Vite for development
     - Runs on port 5173
     - Built with modern stack: TypeScript, TailwindCSS, Flowbite
     - Simple to run directly with npm
  2. React UI (alternative):
     - Also uses Vite
     - Requires Nginx for production
     - More complex deployment setup
- LEARNING: Both UIs share common features:
  - Node 20.11.1 as base
  - Modern tooling (Vite, TypeScript)
  - Docker support
- DECISION: Will start with Svelte UI for testing as it has simpler setup

[2024-01-09 13:30] Context: Build System Analysis
- LEARNING: The `docker_image_build/build.yaml` defines how to build all service images:
  1. Core Services:
     - chatqna: Base service
     - chatqna-guardrails: With guardrails enabled
     - chatqna-without-rerank: Version without reranking
  2. UI Services:
     - chatqna-ui: Svelte UI
     - chatqna-conversation-ui: React UI
  3. Component Services:
     - embedding: Text embedding service
     - retriever: Document retrieval service
     - reranking: Result reranking service
- OBSERVATION: This build system is for creating the base images, but we should use the ready-made images from the OPEA registry
- DECISION: Since we're using the Xeon configuration which uses pre-built images, we don't need to build from source

[2024-01-09 13:35] Context: Environment Configuration Analysis
- LEARNING: Key environment variables from set_env.sh:
  1. Model Configuration:
     - EMBEDDING_MODEL_ID="BAAI/bge-base-en-v1.5"
     - RERANK_MODEL_ID="BAAI/bge-reranker-base"
     - LLM_MODEL_ID="meta-llama/Meta-Llama-3-8B-Instruct"
  2. Vector Store:
     - INDEX_NAME="rag-redis"
  3. Optional Features:
     - LOGFLAG: For enabling logging (disabled by default)
     - JAEGER_IP: For OpenTelemetry tracing
- OBSERVATION: The set_env.sh tries to source a parent .set_env.sh file which is not present
- CONCERN: We need to understand what environment variables should be in the missing .set_env.sh file
- DECISION: We should check the compose.yaml to see what other environment variables are used

[2024-01-09 13:40] Context: vLLM Service Configuration
- LEARNING: vLLM service configuration in compose.yaml:
  1. Base Configuration:
     - Port: 9009:80
     - Uses OPEA registry image: ${REGISTRY:-opea}/vllm:${TAG:-latest}
  2. Resource Requirements:
     - Shared memory: 128GB (shm_size: 128g)
     - Model cache volume: ${MODEL_CACHE:-./data}
  3. Environment Variables:
     - HF_TOKEN: For model access (same as HUGGINGFACEHUB_API_TOKEN)
     - LLM_MODEL_ID: Model to load (default: meta-llama/Meta-Llama-3-8B-Instruct)
     - VLLM_TORCH_PROFILER_DIR: For performance profiling
  4. Health Check:
     - Endpoint: /health
     - Retries: 100 times every 10s
  5. Command:
     - Runs model with host 0.0.0.0 and port 80

[2024-01-09 13:40] Context: Required Environment Variables
- LEARNING: Essential variables that must be set:
  1. Authentication:
     - HUGGINGFACEHUB_API_TOKEN: For model access
  2. Registry:
     - REGISTRY: Docker registry (default: opea)
     - TAG: Image version (default: latest)
  3. Model Configuration:
     - MODEL_CACHE: Where to store model files
     - LLM_MODEL_ID: Which model to use
  4. Network:
     - host_ip: For health checks
     - Optional: http_proxy, https_proxy, no_proxy
- OBSERVATION: The missing .set_env.sh likely sets REGISTRY and TAG variables
- DECISION: We need these variables set before running the compose file

[2024-01-09 13:55] Context: vLLM Memory Requirements
- LEARNING: vLLM service configuration in compose.yaml:
  1. Base Configuration:
     - Uses OPEA registry image: ${REGISTRY:-opea}/vllm:${TAG:-latest}
     - Port: 9009:80
     - Default shared memory: 128GB
  2. Environment Variables:
     - HF_TOKEN: For model access
     - LLM_MODEL_ID: Model to load (meta-llama/Meta-Llama-3-8B-Instruct)
     - VLLM_TORCH_PROFILER_DIR: For performance profiling
  3. Health Check:
     - Endpoint: /health
     - Retries: 100 times every 10s
- OBSERVATION: While 128GB shared memory is the default, we can try with less
- DECISION: We should:
  1. Start with a lower shared memory value
  2. Test if Meta-Llama-3-8B-Instruct loads successfully
  3. Monitor memory usage and adjust as needed

[2024-01-09 14:00] Context: vLLM Memory Analysis
- LEARNING: vLLM memory configuration investigation:
  1. Default Configuration:
     - compose.yaml sets 128GB shared memory (shm_size: 128g)
     - Uses OPEA registry's vLLM image
     - Mounts model cache at /data
  2. Model Size Context:
     - Meta-Llama-3-8B-Instruct is an 8 billion parameter model
     - Base model without quantization needs significant memory
     - FP8 quantization could reduce memory by 2x (per vLLM docs)
  3. Key Observations:
     - 128GB might be the recommended size for optimal performance
     - Memory requirements could be reduced with quantization
     - Need to investigate if OPEA's vLLM image supports quantization
  4. Next Investigation Steps:
     - Examine OPEA's vLLM image configuration
     - Look for quantization options in vLLM service
     - Research minimum viable memory for 8B parameter models

[2024-01-09 14:05] Context: vLLM CPU Deployment Options
- LEARNING: vLLM CPU optimization possibilities:
  1. Command Line Options:
     - Current compose.yaml only uses basic options (--model, --host, --port)
     - Additional options might be available for CPU optimization
     - Need to check OPEA's vLLM image documentation for supported flags
  2. Quantization Support:
     - vLLM supports quantization for reduced memory footprint
     - FP8 quantization could reduce memory by 2x
     - Need to verify if OPEA's image includes quantization support
  3. CPU-Specific Settings:
     - VLLM_CPU_OMP_THREADS_BIND: Controls CPU thread binding
     - Memory utilization can be tuned
     - Thread and worker count might be configurable
- OBSERVATION: The default 128GB shared memory in compose.yaml seems to be:
  1. A conservative setting for optimal performance
  2. Likely configured for Xeon servers with large memory
  3. Possibly reducible with proper optimization
- NEXT STEPS:
  1. Need to find OPEA's vLLM image documentation
  2. Research if quantization is already enabled
  3. Document minimum memory requirements for our model
  4. Test with reduced memory after documentation phase

[2024-01-09 14:10] Context: OPEA vLLM Image Analysis
- LEARNING: OPEA's vLLM image build configuration:
  1. Uses CPU-specific Dockerfile:
     - Located at vllm/Dockerfile.cpu
     - Builds image ${REGISTRY:-opea}/vllm:${TAG:-latest}
     - Extends base chatqna configuration
  2. Implications:
     - The image is specifically optimized for CPU deployment
     - Memory requirements (128GB) likely based on testing
     - Might include CPU-specific optimizations
- OBSERVATION: The 128GB requirement might be:
  1. Based on testing with Meta-Llama-3-8B-Instruct
  2. A safe default for production deployment
  3. Possibly adjustable based on specific use case
- QUESTIONS to Investigate:
  1. Does the CPU Dockerfile include quantization?
  2. What are the minimum memory requirements?
  3. Are there CPU-specific optimizations enabled?
  4. Can we safely reduce memory without impacting stability?
- NEXT STEPS:
  1. Document memory requirements from vLLM documentation
  2. Research successful deployments with less memory
  3. Prepare for testing phase with reduced memory

[2024-01-09 14:15] Context: Meta-Llama-3-8B-Instruct Memory Requirements
- LEARNING: Research on memory requirements:
  1. Model Specifications:
     - Parameters: 8 billion
     - Context Length: 128K tokens
     - Disk Space: ~16GB for model files
  2. Minimum Requirements:
     - RAM: At least 16GB recommended
     - CPU: Modern processor with 8+ cores
  3. vLLM Considerations:
     - Original architecture optimized for GPU
     - CPU backend differs significantly
     - NUMA considerations for multi-socket machines
     - VLLM_CPU_OMP_THREADS_BIND important for memory access
- OBSERVATION: The 128GB in compose.yaml is likely:
  1. Configured for optimal production performance
  2. Includes buffer for concurrent requests
  3. Accounts for both model and system overhead
- DECISION: For our CPU deployment:
  1. Start with minimum 32GB shared memory (2x minimum RAM)
  2. Monitor performance and stability
  3. Increase if needed based on load testing
  4. Document actual memory usage patterns
