# PowerShell script to run Poetry development server and consumer with hot reload
Write-Host "Starting Poetry development server and consumer..." -ForegroundColor Green

try {
    # Define the Python executable path
    $PythonExecutable = ".\.venv\Scripts\python.exe"

    # Check if the Python executable exists
    if (-Not (Test-Path $PythonExecutable)) {
        Write-Host "Python executable not found in the virtual environment. Please ensure the virtual environment is set up correctly." -ForegroundColor Red
        exit 1
    }

    # Add the virtual environment's Scripts folder to the PATH
    $env:PATH = "$(Resolve-Path .\.venv\Scripts);$env:PATH"

    # Start the Poetry development server
    Write-Host "Starting Uvicorn server..." -ForegroundColor Cyan
    $serverJob = Start-Job -ScriptBlock {
        poetry run uvicorn app.main:app --reload
    }

    # Start the consumer
    Write-Host "Starting User Consumer..." -ForegroundColor Cyan
    $consumerJob = Start-Job -ScriptBlock {
        poetry run python contexts/users/interfaces/consumers/user_consumer.py
    }

    # Wait for both jobs to complete
    Write-Host "Both processes are running. Press Ctrl+C to stop." -ForegroundColor Yellow
    Wait-Job -Job $serverJob, $consumerJob

    # Retrieve job results (optional, for debugging)
    Receive-Job -Job $serverJob | Write-Host
    Receive-Job -Job $consumerJob | Write-Host

    Write-Host "Both processes stopped." -ForegroundColor Yellow
} catch {
    Write-Host "Error running Poetry development server or consumer: $_" -ForegroundColor Red
    exit 1
}