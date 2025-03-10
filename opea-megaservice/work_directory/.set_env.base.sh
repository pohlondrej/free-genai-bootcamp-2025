# This file contains environment variables for base layer services

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

# vLLM memory optimization
export VLLM_SHM_SIZE=16g
export VLLM_CPU_OMP_THREADS_BIND=1  # Enable CPU thread binding

# Base services configuration
export EMBEDDING_MODEL_ID="BAAI/bge-small-en-v1.5" 
export INDEX_NAME="rag-redis"  # Redis index name
