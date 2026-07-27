#!/bin/sh
set -e
PORT="${X_ZOHO_CATALYST_LISTEN_PORT:-9000}"
echo "[Berunda AppSail] Starting server on port $PORT"
cd "$(dirname "$0")"
export PYTHONPATH="$PWD:$PYTHONPATH"
exec python3 -m uvicorn src.main:app --host 0.0.0.0 --port "$PORT"
