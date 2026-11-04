# Streamlit App Runner (PowerShell version)

Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "   YOLO Streamlit Object Detection App" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# Check if venv exists
if (-not (Test-Path "venv")) {
    Write-Host "ERROR: Virtual environment not found!" -ForegroundColor Red
    Write-Host "Please run setup first or ensure venv folder exists." -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1

# Check if Streamlit is installed
try {
    python -c "import streamlit" 2>$null
    $streamlit_installed = $?
} catch {
    $streamlit_installed = $false
}

if (-not $streamlit_installed) {
    Write-Host ""
    Write-Host "Installing Streamlit and dependencies..." -ForegroundColor Yellow
    pip install -q -r requirements.txt
}

Write-Host ""
Write-Host "Launching Streamlit app..." -ForegroundColor Green
Write-Host "The app will open in your browser automatically." -ForegroundColor Green
Write-Host ""
Write-Host "Press Ctrl+C to stop the app." -ForegroundColor Yellow
Write-Host ""

# Run Streamlit app
streamlit run streamlit_app.py
