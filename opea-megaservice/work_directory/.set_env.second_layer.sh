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

# Model cache location
export MODEL_CACHE=${MODEL_CACHE:-"./data"}

# Base services configuration
export EMBEDDING_MODEL_ID="BAAI/bge-small-en-v1.5"  # Small, efficient embedding model
export INDEX_NAME="opea-vector-store"  # Redis index name

# Second layer configuration
export RERANK_MODEL_ID="BAAI/bge-reranker-base"  # Small, efficient reranking model
export LOGFLAG="INFO"  # Retriever logging level
export RETRIEVER_COMPONENT_NAME="OPEA_RETRIEVER_REDIS"  # Retriever component identifier
