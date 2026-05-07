Set-Location $PSScriptRoot
Write-Host "Starting the Sentinel Apex API bridge and engine..."
$env:REACT_APP_API_URL = "http://127.0.0.1:5000"
$env:REACT_APP_NICEHASH_API_KEY = "insert_your_real_key_here"
python -m pip install -r requirements.txt
python .\my_mcp_server_dcccfdc5.py