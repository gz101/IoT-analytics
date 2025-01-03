#!/bin/bash

# Wait for the database to be ready
while ! nc -z "$POSTGRES_HOST" "$POSTGRES_PORT"; do
  echo "Waiting for the database at $POSTGRES_HOST:$POSTGRES_PORT..."
  sleep 5
done

# Apply database migrations
echo "Running migrate..."
poetry run python manage.py migrate --noinput

# Start the Gunicorn server
echo "Starting Gunicorn (ASGI) server..."
poetry run gunicorn config.asgi:application \
    -k uvicorn.workers.UvicornWorker \
    --bind 0.0.0.0:8000
