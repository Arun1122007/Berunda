import os
import sys
import uvicorn
from src.main import app

if __name__ == "__main__":
    catalyst_port = os.environ.get("X_ZOHO_CATALYST_LISTEN_PORT")
    env_port = os.environ.get("PORT")
    
    # Prioritize X_ZOHO_CATALYST_LISTEN_PORT from Catalyst AppSail runtime container
    port_str = catalyst_port if catalyst_port else (env_port if env_port else "9000")
    try:
        port = int(port_str)
        if port < 1024:
            port = 9000
    except Exception:
        port = 9000

    print(f"[Berunda AppSail] Binding to 0.0.0.0:{port}", flush=True)
    uvicorn.run(app, host="0.0.0.0", port=port)
