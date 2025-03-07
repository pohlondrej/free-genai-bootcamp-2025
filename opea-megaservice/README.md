# OPEA GenAI Comps Adaptation

## Project Goal

* Adapt a project from the OPEA GenAI Comps (optimized for Intel HW) to run on a CPU using vLLM.
* Focus on efficient learning and implementation within a limited timeframe.

## Key Technologies

* **GenAIComps:** A project for simplifying Generative AI deployment using Docker.
* **Docker:** Containerization platform for packaging and deploying applications.
* **Docker Compose:** Tool for orchestrating multi-container Docker applications.
* **vLLM:** High-throughput and memory-efficient LLM inference and serving engine (CPU compatible).

## Key Learnings and Action Plan

### 1. Prioritize Essential Knowledge

* **Docker Compose Fundamentals:**
    * Service definitions in `docker-compose.yml`.
    * Linking services (`depends_on`, networks).
    * Volume mounting (for model weights).
    * Environment variables in docker compose.
* **vLLM Basic Usage (CPU Mode):**
    * Command-line options (`--disable-gpu`, `--model`).
    * Loading model weights.
    * Basic request testing.
* **Model Weight Management:**
    * Downloading and storing model weights.
    * Mounting weights into Docker containers.
* **OPEA Project Structure (Superficial):**
    * Locating `docker-compose.yml` and LLM serving Dockerfiles.
    * Understanding the overall mega service architecture.

### 2. Simplicity first. Avoid:

* **Advanced Docker Features (initially):**
    * Avoid complex networking, multi-stage builds, etc.
* **Deep OPEA Code Analysis:**
    * Resist delving into intricate internal workings.
* **Premature Performance Optimization:**
    * Focus on functionality first.
* **Troubleshooting Complex Dependencies:**
    * Simplify or find alternatives.
* **Prematurely using Kubernetes:**
    * Stick to docker compose.

### 3. Dockerfile vLLM CPU example.

```dockerfile
FROM vllm/vllm:latest

COPY your_model_weights /model

CMD ["python", "-m", "vllm.entrypoints.openai.api_server", "--model", "/model", "--host", "0.0.0.0", "--port", "8000", "--disable-gpu"]
```
### 4. Key Considerations
- CPU inference will be slower than GPU.
- Memory management is crucial.
- Consider smaller LLMs.
- Ensure sufficient system RAM.
- Start small, iterate, and document.
- Use official documentation from "GenAIComps" and "vllm" folders.