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
