#!/usr/bin/env bash

# Copyright (C) 2024 Intel Corporation
# SPDX-License-Identifier: Apache-2.0

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

# Proxy settings
export no_proxy=huggingface.co,localhost,127.0.0.1

# Model configuration
export LLM_MODEL_ID="Qwen/Qwen2.5-0.5B-Instruct"  # Using 0.5B model for testing
export MODEL_CACHE=${MODEL_CACHE:-"./data"}

# vLLM memory optimization
export VLLM_SHM_SIZE=16g
export VLLM_CPU_OMP_THREADS_BIND=1  # Enable CPU thread binding

# Base services configuration
export EMBEDDING_MODEL_ID="BAAI/bge-base-en-v1.5"  # Small, efficient embedding model
export INDEX_NAME="opea-vector-store"  # Redis index name

# Second layer configuration
export RERANK_MODEL_ID="BAAI/bge-reranker-base"  # Small, efficient reranking model
export LOGFLAG="INFO"  # Retriever logging level
export RETRIEVER_COMPONENT_NAME="OPEA_RETRIEVER_REDIS"  # Retriever component identifier

# Third layer configuration - ChatQNA Backend
export EMBEDDING_SERVER_PORT=80
export RERANK_SERVER_PORT=80
export LLM_SERVER_PORT=80
