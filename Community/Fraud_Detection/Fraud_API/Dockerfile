# Use official lightweight Python image with security updates
FROM python:3.11.8-slim-bullseye

# Set work directory
WORKDIR /app

# Ensure OS packages are up to date
RUN apt-get update && apt-get upgrade -y && \
    apt-get install -y --no-install-recommends gcc build-essential && \
    rm -rf /var/lib/apt/lists/*

# Copy dependencies first for caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Run FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
