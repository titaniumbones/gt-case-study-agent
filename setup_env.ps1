# Setup script for creating and configuring a virtual environment using uv in PowerShell

# Check if .venv directory exists
if (-not (Test-Path -Path ".venv")) {
    Write-Host "Creating virtual environment with uv..." -ForegroundColor Yellow
    uv venv .venv
} else {
    Write-Host "Virtual environment already exists." -ForegroundColor Yellow
}

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
.\.venv\Scripts\Activate.ps1

# Install dependencies with uv
Write-Host "Installing dependencies with uv..." -ForegroundColor Yellow
uv pip install -r requirements.txt

# Install the package in development mode
Write-Host "Installing package in development mode..." -ForegroundColor Yellow
uv pip install -e .

# Display success message
Write-Host "Setup complete! Virtual environment is ready." -ForegroundColor Green
Write-Host "To activate the environment, run:" -ForegroundColor Green
Write-Host ".\.venv\Scripts\Activate.ps1"