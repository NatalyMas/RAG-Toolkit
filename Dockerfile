ARG DOCKER_PROXY
FROM $DOCKER_PROXY/python:3.12.11-slim

ARG PIP_INDEX_PROXY_URL

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .

RUN python -m pip install --no-cache-dir --upgrade pip \
    && python -m pip install --no-cache-dir -r requirements.txt \
    --default-timeout=1000 \
    --index-url "${PIP_INDEX_PROXY_URL}"

COPY src ./src

CMD ["uvicorn", "src.app.main:app", "--host", "0.0.0.0", "--port", "8080"]
