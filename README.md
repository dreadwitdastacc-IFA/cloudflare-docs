# Gogetum Minmine PROJ

This project contains the Gogetum Minmine development server, a Flask API bridge, a Sentinel Apex engine simulator, Cloudflare route support, and a Bitcoin regtest cluster helper.

## Prerequisites

- Python 3.13+
- Docker / Docker Compose
- Node.js if you want to run the `sentinel-apex.cjs` Node script
- PowerShell for the helper scripts

## Setup

1. Install Python dependencies:

```powershell
Set-Location G:\gogetum-minmine_PROD
python -m pip install -r requirements.txt
```

1. Update `.env` with your values:

```env
REACT_APP_NICEHASH_API_KEY="insert_your_real_key_here"
REACT_APP_API_URL="http://127.0.0.1:5000"
CLOUDFLARE_TOKEN="your_cloudflare_api_token"
CLOUDFLARE_ZONE_ID="your_cloudflare_zone_id"
CF_TUNNEL_TARGET="your-tunnel-uuid.cfargotunnel.com"
```

2. Start the Bitcoin regtest cluster:

```powershell
.\start-regtest.ps1
```

> Note: This repository uses a Dockerized Bitcoin Core regtest cluster and the `bitcoind` CLI inside the container. It does not require `bitcoind_qt.exe` or the GUI wallet binary for regtest operation.

1. Start the API + engine server:

```powershell
.\start-server.ps1
```

1. Optionally run the Node sentinel script:

```powershell
node .\sentinel-apex.cjs
```

## API Endpoints

- `GET /api/health`
- `GET /api/data`
- `GET /api/state`
- `GET /api/bitcoin/regtest/status`
- `POST /api/bitcoin/regtest/start`
- `POST /api/bitcoin/regtest/stop`

## Termux / Android SSH setup

1. Install OpenSSH in Termux:

```bash
pkg install openssh
passwd
sshd
```

1. Find your phone IP:

```bash
ip addr show wlan0
```

1. From your PC connect with SSH:

```powershell
ssh username@PHONE_IP
```

This lets you access your phone terminal remotely while working on the project.

## Notes

- The Python files were syntax-checked using `python -m py_compile`.
- `api_bridge.py` now exposes Bitcoin regtest control endpoints.
- `docker-compose.bitcoin-regtest.yml` creates a 3-node regtest cluster.
- `amf.py` provides a small application messaging framework for future extension.
