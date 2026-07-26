import os
import sys

port = os.environ.get("X_ZOHO_CATALYST_LISTEN_PORT") or os.environ.get("PORT") or "9000"
print(f"[AppSail] Starting Berunda FastAPI on port {port}...", flush=True)

# Replace current process with uvicorn listening on 0.0.0.0:port
os.execvp(
    sys.executable,
    [
        sys.executable,
        "-m",
        "uvicorn",
        "src.main:app",
        "--host",
        "0.0.0.0",
        "--port",
        str(port),
    ],
)
