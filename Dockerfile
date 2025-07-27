# Use Python 3.9 as base image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p logs/traces \
    && mkdir -p data/cache \
    && mkdir -p data/metrics

# Set up environment
ENV PYTHONPATH=/app \
    REDIS_HOST=redis \
    REDIS_PORT=6379 \
    MONGO_HOST=mongodb \
    MONGO_PORT=27017

# Expose ports
EXPOSE 8000 8001 8002

# Create non-root user
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Start the application
CMD ["uvicorn", "Core.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"] 