import os
import requests
from dotenv import load_dotenv

class GatewayManager:
    """Manages Cloudflare DNS routing for the Sentinel Apex infrastructure."""
    
    def __init__(self):
        load_dotenv()
        self.token = os.getenv("CLOUDFLARE_TOKEN")
        self.zone_id = os.getenv("CLOUDFLARE_ZONE_ID")
        
        if not self.token or not self.zone_id:
            raise ValueError("CRITICAL: Missing Cloudflare credentials in .env")

        self.base_url = f"https://api.cloudflare.com/client/v4/zones/{self.zone_id}/dns_records"
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

    def ensure_tunnel_route(self, subdomain, tunnel_target, proxied=True):
        """Checks if the route exists; creates or updates it if necessary."""
        print(f"🔍 Auditing route for: {subdomain}")
        
        response = requests.get(
            self.base_url,
            headers=self.headers,
            params={"name": subdomain, "type": "CNAME"}
        )
        response.raise_for_status()
        records = response.json().get("result", [])

        if records:
            record = records[0]
            if record["content"] == tunnel_target:
                print(f"✅ Route verified: {subdomain} -> {tunnel_target}")
                return True
            else:
                print(f"🔄 Re-routing {subdomain} to {tunnel_target}...")
                payload = {
                    "type": "CNAME",
                    "name": subdomain,
                    "content": tunnel_target,
                    "ttl": 1,
                    "proxied": proxied
                }
                requests.put(f"{self.base_url}/{record['id']}", headers=self.headers, json=payload).raise_for_status()
                return True
        else:
            print(f"✨ Forging new route: {subdomain} -> {tunnel_target}")
            payload = {
                "type": "CNAME",
                "name": subdomain,
                "content": tunnel_target,
                "ttl": 1,
                "proxied": proxied
            }
            res = requests.post(self.base_url, headers=self.headers, json=payload)
            res.raise_for_status()
            return res.json().get("success", False)
