# DeepSonar AI - Docker Image
# Multi-stage build for optimized image size

# ==============================================================================
# Stage 1: Base Python environment
# ==============================================================================
FROM python:3.11-slim as base

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# ==============================================================================
# Stage 2: Dependencies installation
# ==============================================================================
FROM base as dependencies

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# ==============================================================================
# Stage 3: Final application image
# ==============================================================================
FROM dependencies as final

WORKDIR /app

# Copy application code
COPY ai_engine/ ./ai_engine/
COPY backend/ ./backend/
COPY interface/ ./interface/
COPY portal/ ./portal/

# Copy configuration files
COPY .env.example ./.env.example

# Create necessary directories
RUN mkdir -p /app/backend/static/fonts \
    && mkdir -p /app/backend/db

# Set working directory for Chainlit
WORKDIR /app/interface

# Expose ports
# 8001 - Chainlit Interface
# 8000 - Django Backend API
EXPOSE 8001 8000

# Default command (can be overridden by docker-compose)
CMD ["chainlit", "run", "app.py", "--host", "0.0.0.0", "--port", "8001"]
