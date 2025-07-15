# Use Python slim-bookworm image for smaller size and security
FROM python:3.11-slim-bookworm

# Set working directory
WORKDIR /app

# Install system dependencies including curl for health checks
# Pin specific versions and minimize installed packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl=7.88.1-10+deb12u5 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install dependencies with security upgrades
RUN pip install --no-cache-dir --upgrade pip setuptools==78.1.1 wheel && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create data directory for database
RUN mkdir -p /data

# Create non-root user for security
RUN adduser --disabled-password --gecos '' appuser && \
    chown -R appuser:appuser /app && \
    chown -R appuser:appuser /data
USER appuser

# Expose port
EXPOSE 5000

# Health check using the proper health endpoint
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

# Run application
CMD ["python", "app.py"]
