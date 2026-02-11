# =========================
# Builder stage
# =========================
FROM python:3.9-slim AS builder

WORKDIR /app

# Install build dependencies for Python packages like Pillow
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libjpeg-dev \
    zlib1g-dev \
    libpng-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt ./

# Install Python dependencies to a separate folder
RUN python -m pip install --upgrade pip wheel \
    && pip install --prefix=/install --no-cache-dir -r requirements.txt

# =========================
# Runtime stage
# =========================
FROM python:3.9-slim

WORKDIR /app

# Install runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    libjpeg-dev \
    zlib1g-dev \
    libpng-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy installed Python packages from builder
COPY --from=builder /install /usr/local

# Set Python path to include the app directory
ENV PYTHONPATH=/app

# Copy application code
COPY src/ /app/src/
COPY models/ /app/models/

# Verify model files exist
RUN ls -la /app/models/ && \
    echo "Model files copied successfully"

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Start the FastAPI app
CMD ["uvicorn", "src.inference.app:app", "--host", "0.0.0.0", "--port", "8000"]


