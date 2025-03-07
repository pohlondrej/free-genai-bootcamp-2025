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
