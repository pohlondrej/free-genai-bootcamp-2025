# Setup general container environment
FROM python:3.10-slim AS base

RUN apt-get update && apt-get upgrade -y && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

ENV HOME=/home/user
ENV APP_HOME=$HOME/app

RUN useradd -m -s /bin/bash user && \
    mkdir -p $APP_HOME && \
    chown -R user $APP_HOME

WORKDIR $APP_HOME

# Install Python dependencies
FROM base AS python-base

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip setuptools && \
    pip install --no-cache-dir -r requirements.txt

ENV PYTHONPATH=$PYTHONPATH:$APP_HOME

USER user

# Download model files
ARG HF_MODEL_NAME
ENV HF_MODEL_NAME=${HF_MODEL_NAME}

RUN python -c "from transformers import AutoTokenizer, AutoModel; AutoTokenizer.from_pretrained('${HF_MODEL_NAME}'); AutoModel.from_pretrained('${HF_MODEL_NAME}')"

# Run the Python script
FROM python-base

COPY faqgen.py .

ENTRYPOINT ["python", "faqgen.py"]