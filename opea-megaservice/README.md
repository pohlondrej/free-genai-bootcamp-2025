# OPEA GenAI Comps Adaptation

## Project Goal

* Adapt the "ChatQnA" project from OPEA GenAI Examples to run on CPU using vLLM
* Document the learning process and understanding of mega services architecture
* Successfully run the adapted service or document valuable learnings trying to do so

## Project Layout

*   `GenAIComps/`: Contains the original OPEA GenAI Comps project. (Read-only)
*   `ChatQnAExample/`: Contains the ChatQnA example to be adapted. (Read-only)
*   `vllm/`: Contains the vLLM library. (Read-only)
*   `docs/`: Contains project documentation.
    *   `docs/Learnings.md`: Records all learnings and observations.
    *   `docs/Rules.md`: Contains project rules and constraints.
    *   `docs/Tasks.md`: Contains the project's action plan.
*   `docker-compose.yml`: Defines the multi-container Docker application.
*   `.gitignore`: Specifies intentionally untracked files that Git should ignore.


## Key Technologies

* **GenAIComps & Examples:** Reference projects containing the original OPEA implementation (Read-only source code)
* **Docker:** Containerization platform for packaging and deploying applications
* **Docker Compose:** Tool for orchestrating multi-container Docker applications
* **vLLM:** High-throughput and memory-efficient LLM inference engine (CPU compatible)

### Key Considerations
- CPU inference will be slower than GPU.
- Memory management is crucial.
- Consider smaller LLMs.
- Ensure sufficient system RAM.
- Start small, iterate, and document.
- Use official documentation from "GenAIComps" and "vllm" folders.