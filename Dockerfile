FROM python:3.12-slim-bullseye

WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    libhdf5-dev \
    pkg-config && \
    rm -rf /var/lib/apt/lists/*

# Copy the pyproject.toml and poetry.lock files to the container
COPY pyproject.toml poetry.lock* /app/

# Install Poetry and dependencies in a single RUN step to reduce layers
RUN pip install --no-cache-dir poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev --no-interaction --no-ansi

# Copy the rest of the application code
COPY . /app

# Make port available to the world outside this container
EXPOSE 8123

# Run the application
CMD ["uvicorn", "server.main:app", "--host", "0.0.0.0", "--port", "8123"]
