# Dockerfile
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y curl build-essential && rm -rf /var/lib/apt/lists/*

# Install Poetry
ENV POETRY_VERSION=1.5.1
RUN curl -sSL https://install.python-poetry.org | python3 -

# Set PATH so that poetry is available
ENV PATH="/root/.local/bin:$PATH"

# Create a working directory in the container
WORKDIR /app

# Copy only pyproject.toml and poetry.lock first for dependency installation
COPY pyproject.toml poetry.lock .env /app/

# Install Python dependencies with Poetry (no dev dependencies in production)
RUN poetry install --no-dev --no-root

# Now copy the Django application files
COPY . /app/

# Install the local project (which might contain your Django app code)
RUN poetry install --no-dev

# Collect static files during image build
RUN poetry run python manage.py collectstatic --noinput

# Expose port 8000 for Gunicorn
EXPOSE 8000

# Run Gunicorn when the container starts
CMD ["poetry", "run", "gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
