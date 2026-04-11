# Project Helix - Dockerfile
# Multi-stage build for minimal image size

# ============================================================================
# Stage 1: Base image
# ============================================================================
FROM python:3.10-slim AS base

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    HELIX_VERSION=1.0.0-beta.3

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# ============================================================================
# Stage 2: Builder - Install dependencies
# ============================================================================
FROM base AS builder

# Create virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install Python dependencies
COPY pyproject.toml ./
RUN pip install --no-cache-dir -e .

# ============================================================================
# Stage 3: Production image
# ============================================================================
FROM base AS production

# Create non-root user for security
RUN groupadd --gid 1000 helix && \
    useradd --uid 1000 --gid helix --shell /bin/bash --create-home helix

# Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy application code
COPY --chown=helix:helix . .

# Switch to non-root user
USER helix

# Expose default port (can be overridden)
ENV HELIX_PORT=8000
EXPOSE $HELIX_PORT

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:$HELIX_PORT/health || exit 1

# Default command
CMD ["helix", "serve", "--host", "0.0.0.0", "--port", "8000"]

# ============================================================================
# Development image (for local development)
# ============================================================================
FROM base AS development

# Create virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install development dependencies
COPY pyproject.toml ./
RUN pip install --no-cache-dir -e . && \
    pip install --no-cache-dir pytest pytest-asyncio pytest-cov mypy

# Create development user
RUN groupadd --gid 1000 helix && \
    useradd --uid 1000 --gid helix --shell /bin/bash --create-home helix

# Copy application code
COPY --chown=helix:helix . .

# Set work directory
WORKDIR /app
USER helix

# Default command for development
CMD ["/bin/bash"]
