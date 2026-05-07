Set-Location $PSScriptRoot
if (-not (Test-Path .\docker-compose.bitcoin-regtest.yml)) {
    Write-Error "Missing docker-compose.bitcoin-regtest.yml in $PWD"
    exit 1
}
$dockerComposeCmd = Get-Command docker-compose -ErrorAction SilentlyContinue
$dockerCmd = Get-Command docker -ErrorAction SilentlyContinue

if ($dockerComposeCmd) {
    Write-Host "Starting Bitcoin regtest cluster with docker-compose..."
    & $dockerComposeCmd.Source -f .\docker-compose.bitcoin-regtest.yml up -d
} elseif ($dockerCmd) {
    Write-Host "Starting Bitcoin regtest cluster with docker compose..."
    & $dockerCmd.Source compose -f .\docker-compose.bitcoin-regtest.yml up -d
} else {
    Write-Error "Docker CLI not found. Install Docker Desktop or Docker Engine and ensure docker or docker-compose is on PATH."
    exit 1
}

if ($LASTEXITCODE -ne 0) {
    Write-Error "Failed to start Bitcoin regtest cluster."
    exit $LASTEXITCODE
}

Write-Host "Bitcoin regtest cluster started. Use docker compose -f .\docker-compose.bitcoin-regtest.yml ps to inspect."