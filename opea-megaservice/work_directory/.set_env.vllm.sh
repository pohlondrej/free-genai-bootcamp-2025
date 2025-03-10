# This file contains environment variables for vLLM service

# Required: HuggingFace token for model access
if [ -z "${HUGGINGFACEHUB_API_TOKEN}" ]; then
    echo "Error: HUGGINGFACEHUB_API_TOKEN is not set. Please set HUGGINGFACEHUB_API_TOKEN."
    exit 1
fi

# Docker registry configuration
export REGISTRY=${REGISTRY:-"opea"}
export TAG=${TAG:-"latest"}

# Host IP for service communication
export host_ip=$(hostname -I | awk '{print $1}')
if [ -z "${host_ip}" ]; then
    echo "Error: Could not determine host_ip."
    exit 1
fi

# Model configuration
export LLM_MODEL_ID="Qwen/Qwen2.5-0.5B-Instruct"  # Using 0.5B model for testing
export MODEL_CACHE=${MODEL_CACHE:-"./data"}

# vLLM memory optimization (reduced from 128GB default)
export VLLM_SHM_SIZE=16g  # Half of available 32GB RAM
export VLLM_CPU_OMP_THREADS_BIND=1  # Enable CPU thread binding
