# OPEA GenAI Comps Adaptation

## Project Goal

* Adapt a project from the OPEA GenAI Comps (optimized for Intel HW) to run on a CPU using vLLM.
* Focus on efficient learning and implementation within a limited timeframe.

## Key Technologies

* **GenAIComps:** A project for simplifying Generative AI deployment using Docker. (Read-only, located in the `GenAIComps` directory)
* **Docker:** Containerization platform for packaging and deploying applications.
* **Docker Compose:** Tool for orchestrating multi-container Docker applications.
* **vLLM:** High-throughput and memory-efficient LLM inference and serving engine (CPU compatible). (Read-only, located in the `vllm` directory)

## Project Layout

*   `GenAIComps/`: Contains the original OPEA GenAI Comps project. (Read-only)
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