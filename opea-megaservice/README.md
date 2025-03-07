# OPEA GenAI Comps Adaptation

## Project Goal

* Adapt the "ChatQnA" project from OPEA GenAI Examples to run on CPU using vLLM
* Document the learning process and understanding of mega services architecture
* Successfully run the adapted service or document valuable learnings trying to do so

## Key Technologies

* **GenAIComps & Examples:** Reference projects containing the original OPEA implementation (Read-only source code)
* **Docker:** Containerization platform for packaging and deploying applications
* **Docker Compose:** Tool for orchestrating multi-container Docker applications
* **vLLM:** High-throughput and memory-efficient LLM inference engine (CPU compatible)

## Project Layout

*   `GenAIComps/`: Contains the original OPEA GenAI Comps project. (Read-only)
*   `GenAIExamples/`: Contains OPEA GenAI examples. (Read-only)
*   `vllm/`: Contains the vLLM library. (Read-only)
*   `docs/`: Contains project documentation.
    *   `docs/Learnings.md`: Records all learnings and observations.
    *   `docs/Rules.md`: Contains project rules and constraints.
    *   `docs/Tasks.md`: Contains the project's action plan.
*   `docker-compose.yml`: Defines the multi-container Docker application.
*   `.gitignore`: Specifies intentionally untracked files that Git should ignore.

## Setup

1.  Ensure Docker and Docker Compose are installed.
2.  Refer to `docs/Tasks.md` for the project's action plan.
3.  Record all learnings in `docs/Learnings.md`.
4.  Adhere to the rules specified in `docs/Rules.md`.

### Dockerfile vLLM CPU example.

```dockerfile
FROM vllm/vllm:latest

COPY your_model_weights /model

CMD ["python", "-m", "vllm.entrypoints.openai.api_server", "--model", "/model", "--host", "0.0.0.0", "--port", "8000", "--disable-gpu"]
```

### Key Considerations
- CPU inference will be slower than GPU.
- Memory management is crucial.
- Consider smaller LLMs.
- Ensure sufficient system RAM.
- Start small, iterate, and document.
- Use official documentation from "GenAIComps" and "vllm" folders.