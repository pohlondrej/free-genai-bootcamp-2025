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

# Model configuration
export LLM_MODEL_ID="meta-llama/Meta-Llama-3-8B-Instruct"  # Primary model choice
export MODEL_CACHE=${MODEL_CACHE:-"./data"}

# vLLM memory optimization (reduced from 128GB default)
# Starting with 32GB (2x minimum 16GB requirement) for testing
export VLLM_SHM_SIZE=32g
export VLLM_CPU_OMP_THREADS_BIND=1  # Enable CPU thread binding for better performance
export VLLM_QUANTIZATION="fp8"  # Enable FP8 quantization to reduce memory by 2x

# Optional: proxy settings if needed
#export http_proxy=""
#export https_proxy=""
#export no_proxy=""
