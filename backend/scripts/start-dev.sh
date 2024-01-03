#!/usr/bin/env bash

set -e

DEFAULT_MODULE_NAME=app.main

MODULE_NAME=${MODULE_NAME:-$DEFAULT_MODULE_NAME}
VARIABLE_NAME=${VARIABLE_NAME:-app}
export APP_MODULE=${APP_MODULE:-"$MODULE_NAME:$VARIABLE_NAME"}

HOST=${HOST:-0.0.0.0}
PORT=${PORT:-8000}
WORKERS=${WORKERS:-2}

echo "Run migrations"

alembic upgrade head


# Start Uvicorn with live reload
exec uvicorn --reload --proxy-headers --host $HOST --port $PORT --workers $WORKERS --loop uvloop "$APP_MODULE"