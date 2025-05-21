
# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install system dependencies (if any are needed, e.g., for psycopg2)
# RUN apt-get update && apt-get install -y --no-install-recommends some-package && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install poetry==1.7.1

# Copy only pyproject.toml and poetry.lock* first to leverage Docker cache
COPY pyproject.toml poetry.lock* ./

# Configure Poetry to not create virtualenvs within the project directory
RUN poetry config virtualenvs.create false

# Install project dependencies
# --no-interaction ensures no interactive prompts
# --no-ansi prevents potential issues with ANSI color codes in logs
RUN poetry install --no-interaction --no-ansi --no-root --without dev

# Copy the rest of the application code
COPY . /app

# Install the application itself as editable (so imports work)
RUN poetry install --no-interaction --no-ansi --without dev

# Expose port 8000 for the FastAPI app
EXPOSE 8000

# Command to run the application using uvicorn
# Use --host 0.0.0.0 to make it accessible outside the container
CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

