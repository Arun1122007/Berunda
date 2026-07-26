import os
import sys
import uvicorn
from src.main import app

app = app

if __name__ == "__main__":
    port_env = (
        os.environ.get("X_ZOHO_CATALYST_LISTEN_PORT")
        or os.environ.get("PORT")
        or "9000"
    )
    try:
        port = int(port_env)
        if port < 1024:
            port = 9000
    except Exception:
        port = 9000

    print(f"[Berunda AppSail] Listening on 0.0.0.0:{port}", flush=True)
    uvicorn.run(app, host="0.0.0.0", port=port)
