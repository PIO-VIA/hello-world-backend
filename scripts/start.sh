#!/usr/bin/env bash
set -e

# Run migrations
echo "Running migrations..."
alembic upgrade head

# Start application
echo "Starting application..."
exec uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000} --proxy-headers --forwarded-allow-ips='*'
