FROM python:3.10-slim

ARG APP_DIR
ARG MODULES_DIR

WORKDIR /app

COPY $APP_DIR/requirements.txt .
RUN pip install -r requirements.txt

COPY $MODULES_DIR/ .
COPY $APP_DIR/app/ .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]