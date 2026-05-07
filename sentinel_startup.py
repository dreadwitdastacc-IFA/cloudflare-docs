import os
import sys

from cloudflare_gateway import GatewayManager


def initialize_sentinel():
    """Startup sequence for the Vision of Orunmila engine."""
    print("Initiating Sentinel Apex...")

    try:
        gateway = GatewayManager()
        tunnel_target = os.getenv("CF_TUNNEL_TARGET")

        if not tunnel_target:
            print("WARNING: CF_TUNNEL_TARGET not found. Skipping external route mapping.")
        else:
            gateway.ensure_tunnel_route("api.apex.yourdomain.com", tunnel_target)
            gateway.ensure_tunnel_route("node.apex.yourdomain.com", tunnel_target)

    except Exception as e:
        print(f"Startup Error: {e}")
        sys.exit(1)

    print("Gateway secured. Engaging arbitrage detection...")
    # ... rest of your engine logic ...


if __name__ == "__main__":
    initialize_sentinel()
