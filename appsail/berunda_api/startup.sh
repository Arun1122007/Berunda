#!/bin/bash
# Berunda API - AppSail startup script
set -e

PORT="${X_ZOHO_CATALYST_LISTEN_PORT:-8000}"
echo "Starting Berunda API on port $PORT"

exec uvicorn src.main:app --host 0.0.0.0 --port "$PORT" --workers 1
