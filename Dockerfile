# =========================
# Builder stage
# =========================
FROM python:3.9-slim AS builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (better caching)
COPY requirements.txt requirements-dev.txt ./

# Upgrade pip & install deps INTO SYSTEM
RUN python -m pip install --upgrade pip wheel \
    && pip install --no-cache-dir --prefer-binary \
       -r requirements.txt \
       -r requirements-dev.txt

# =========================
# Runtime stage
# =========================
FROM python:3.9-slim

WORKDIR /app

# Copy installed Python packages
COPY --from=builder /usr/local/lib/python3.9/site-packages \
                     /usr/local/lib/python3.9/site-packages

COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application code
COPY src/ src/
COPY deployment/ deployment/
COPY models /app/models

# Environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

EXPOSE 8000

CMD ["uvicorn", "src.inference.app:app", "--host", "0.0.0.0", "--port", "8000"]
