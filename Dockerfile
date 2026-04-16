# STAGE 1 - BUILD

FROM python:3.14-alpine AS builder

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app

ENV UV_PROJECT_ENVIRONMENT=/app/venv

COPY pyproject.toml uv.lock ./

RUN uv sync --frozen --no-dev --no-install-project && \
    rm -rf /app/venv/lib/python*/site-packages/pip \
    /app/venv/lib/python*/site-packages/pip-*

RUN find /app/venv -name "*.so" -exec strip {} + || true
RUN find /app/venv -type d -name "__pycache__" -exec rm -rf {} + || true
RUN find /app/venv -name "*.pyc" -delete || true

# STAGE 2 - RUNTIME

FROM python:3.14-alpine

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    VIRTUAL_ENV=/app/venv \
    PATH="/app/venv/bin:$PATH" \
    PYTHONPATH="/app"

WORKDIR /app

RUN apk update && \
    apk upgrade && \
    apk add --no-cache zlib libstdc++ && \
    rm -rf /var/cache/apk/* && \
    rm -rf /usr/local/lib/python*/site-packages/pip \
           /usr/local/lib/python*/site-packages/pip-*

RUN adduser -D appuser && \
    chown -R appuser:appuser /app

COPY --from=builder --chown=appuser:appuser /app/venv /app/venv
COPY --chown=appuser:appuser main.py ./
COPY --chown=appuser:appuser templates/ ./templates/

USER appuser

EXPOSE 5000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:5000')" || exit 1

CMD ["/app/venv/bin/python", "main.py"]
