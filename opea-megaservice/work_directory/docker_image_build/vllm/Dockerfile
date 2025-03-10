# Dockerfile for custom AMD CPU vLLM service

FROM ubuntu:24.04

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3-pip \
    python3-dev \
    build-essential \
    git \
    curl \
    gcc-12 \
    g++-12 \
    libnuma-dev \
    && rm -rf /var/lib/apt/lists/*

RUN update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-12 10 --slave /usr/bin/g++ g++ /usr/bin/g++-12

# Set working directory
WORKDIR /app

# Install CPU-specific PyTorch dependencies
RUN pip install --break-system-packages --no-cache-dir torch==2.3.1+cpu torchvision==0.18.1+cpu -f https://download.pytorch.org/whl/torch_stable.html

# Clone and build vLLM from source
RUN git clone https://github.com/vllm-project/vllm.git

# Install build dependencies
RUN pip install --break-system-packages "cmake>=3.26" wheel packaging ninja "setuptools-scm>=8" numpy
RUN cd vllm && pip install --break-system-packages -v -r requirements/cpu.txt --extra-index-url https://download.pytorch.org/whl/cpu

# Build vLLM
RUN cd vllm && VLLM_TARGET_DEVICE=cpu python3 setup.py install

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Add healthcheck
HEALTHCHECK --interval=30s --timeout=30s --start-period=300s --retries=3 \
    CMD curl -f http://localhost:80/health || exit 1

# Set entrypoint
ENTRYPOINT ["python3", "-m", "vllm.entrypoints.openai.api_server"]
