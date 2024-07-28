FROM python:3.12-slim

WORKDIR /app

# Copy the pyproject.toml and poetry.lock files to the container
COPY pyproject.toml poetry.lock* /app/

# Install Poetry and dependencies
RUN pip install poetry
RUN poetry config virtualenvs.create false && poetry install --no-dev --no-interactive --no-ansi

# Copy the rest of the application code
COPY . /app

# Make port available to the world outside this container
EXPOSE 8123

# Run the application
CMD ["uvicorn", "server.main:app", "--host", "0.0.0.0", "--port", "8123"]
