# =========================
# Builder stage
# =========================
FROM python:3.9-slim AS builder

WORKDIR /app

# Install build dependencies including libraries needed for Pillow
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libjpeg-dev \
    zlib1g-dev \
    libpng-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt requirements-dev.txt ./

# Install runtime dependencies to a separate folder
RUN python -m pip install --upgrade pip wheel \
    && pip install --prefix=/install --no-cache-dir -r requirements.txt

# =========================
# Runtime stage
# =========================
FROM python:3.9-slim

WORKDIR /app

# Install runtime dependencies for image processing and health checks
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    libjpeg-dev \
    zlib1g-dev \
    libpng-dev \
