import logging
 
import os
from threading import Thread

from api_bridge import app
from sentinel_apex_core import engine_pulse
from sentinel_startup import initialize_sentinel

logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")


def run_engine():
    logging.info("[MY-MCP] Sentinel Apex Core engine thread starting.")
    engine_pulse()


def main():
    initialize_sentinel()

    host = os.getenv("API_HOST", "0.0.0.0")
    port = int(os.getenv("API_PORT", "5000"))

    logging.info("--------------------------------------------------")
    logging.info("[MY-MCP] Starting gogetum-minmine development server")
    logging.info(f"[MY-MCP] API bridge available at http://{host}:{port}/api/data")
    logging.info("--------------------------------------------------")

    engine_thread = Thread(target=run_engine, daemon=True, name="SentinelApexEngine")
    engine_thread.start()

    app.run(host=host, port=port, debug=False, use_reloader=False)


if __name__ == "__main__":
    main()
