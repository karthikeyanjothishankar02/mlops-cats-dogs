# ========================================
# Multi-stage Dockerfile for Cats vs Dogs Classifier
# ========================================

# ========================================
# Stage 1: Builder
# ========================================
FROM python:3.9-slim-bookworm AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /build

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --upgrade pip \
    && pip install --target=/build/deps -r requirements.txt

# ========================================
# Stage 2: Runtime
# ========================================
FROM python:3.9-slim-bookworm AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app:/app/deps \
    API_HOST=0.0.0.0 \
    API_PORT=8000 \
    GDRIVE_FOLDER_ID=1knSkL_LDsuWTXAIcv6UfdxhuXMUXbC65

WORKDIR /app

# Install runtime dependencies only
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Copy dependencies
COPY --from=builder /build/deps /app/deps

# Copy app
COPY src/ /app/src/
COPY scripts/download_model.py /app/scripts/download_model.py
COPY models/ /app/models/

# ⚠️ Better: DO NOT download model at build time
# Downloading at build makes image non-reproducible.
# Remove this block for proper production MLOps:
# RUN python -c "..."

# Create non-root user
RUN useradd --create-home --shell /bin/bash appuser \
    && chown -R appuser:appuser /app

USER appuser

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

CMD ["python", "-m", "uvicorn", "src.inference.app:app", "--host", "0.0.0.0", "--port", "8000"]
