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
