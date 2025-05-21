# PowerShell script to run Poetry development server and consumer with hot reload
Write-Host "Starting Poetry development server and consumer..." -ForegroundColor Green

# Activate venv if needed
$venvScripts = Resolve-Path .\.venv\Scripts
if (-Not (Test-Path "$venvScripts\python.exe")) {
    Write-Host "Virtual environment not found. Run 'poetry install' first." -ForegroundColor Red
    exit 1
}
$env:PATH = "$venvScripts;$env:PATH"

Write-Host "Launching Uvicorn server..." -ForegroundColor Cyan
$serverProc = Start-Process `
    -FilePath "poetry" `
    -ArgumentList "run uvicorn app.main:app --reload" `
    -NoNewWindow `
    -PassThru

Write-Host "Launching Inventory consumer..." -ForegroundColor Cyan
$consumerProc = Start-Process `
    -FilePath "poetry" `
    -ArgumentList "run python contexts/inventory/interfaces/consumers/inventory_consumer.py" `
    -NoNewWindow `
    -PassThru

Write-Host "Both processes running. Press Ctrl+C to stop." -ForegroundColor Yellow

# Wait for both to exit (logs remain visible)
$serverProc.WaitForExit()
$consumerProc.WaitForExit()

Write-Host "Processes have exited." -ForegroundColor Yellow