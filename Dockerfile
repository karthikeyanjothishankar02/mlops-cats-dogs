# ========================================
# Multi-stage Dockerfile for Cats vs Dogs Classifier
# ========================================
# Stage 1: Build stage - install dependencies
# Stage 2: Runtime stage - minimal image for production
# ========================================

# ========================================
# Stage 1: Builder
# ========================================
FROM python:3.9-slim as builder

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /build

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies to a specific target
RUN pip install --target=/build/deps -r requirements.txt

# ========================================
# Stage 2: Runtime
# ========================================
FROM python:3.9-slim as runtime

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app:/app/deps \
    API_HOST=0.0.0.0 \
    API_PORT=8000 \
    GDRIVE_FOLDER_ID=1knSkL_LDsuWTXAIcv6UfdxhuXMUXbC65

# Set working directory
WORKDIR /app

# Install runtime dependencies only
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Copy dependencies from builder
COPY --from=builder /build/deps /app/deps

# Copy application code
COPY src/ /app/src/
COPY scripts/download_model.py /app/scripts/download_model.py
COPY models/ /app/models/

# Download model from Google Drive if not present
RUN python -c "import sys; sys.path.insert(0, '/app'); from scripts.download_model import ensure_model_exists; ensure_model_exists()" || echo "Model will be downloaded at runtime"

# Create non-root user for security
RUN useradd --create-home --shell /bin/bash appuser \
    && chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run the application
CMD ["python", "-m", "uvicorn", "src.inference.app:app", "--host", "0.0.0.0", "--port", "8000"]



