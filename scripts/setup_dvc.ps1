# ============================================
# DVC Setup Script for Google Drive Remote (Windows)
# ============================================
# This script helps configure DVC with Google Drive as remote storage
# Models are stored in Google Drive with public sharing ("Anyone with the link")
# Usage: .\scripts\setup_dvc.ps1

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "DVC Setup with Google Drive (Public Sharing)" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# Check if DVC is installed
$dvcInstalled = Get-Command dvc -ErrorAction SilentlyContinue
if (-not $dvcInstalled) {
    Write-Host "DVC is not installed. Installing..." -ForegroundColor Yellow
    pip install dvc dvc-gdrive
}

Write-Host "DVC version:" (dvc version | Select-Object -First 1)
Write-Host ""

# Initialize DVC if not already initialized
if (-not (Test-Path ".dvc")) {
    Write-Host "Initializing DVC..."
    dvc init
}

Write-Host "Current DVC remotes:"
dvc remote list
Write-Host ""

# Instructions for setting up Google Drive
Write-Host "============================================" -ForegroundColor Green
Write-Host "Setup Instructions (Public Sharing Method)" -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Green
Write-Host ""
Write-Host "STEP 1: Create Google Drive Folder" -ForegroundColor Yellow
Write-Host "   - Go to https://drive.google.com"
Write-Host "   - Create a new folder (e.g., 'mlops-cats-dogs-models')"
Write-Host ""
Write-Host "STEP 2: Enable Public Sharing" -ForegroundColor Yellow
Write-Host "   - Right-click the folder -> Share"
Write-Host "   - Click 'General access' -> Change to 'Anyone with the link'"
Write-Host "   - Set role to 'Viewer'"
Write-Host "   - Click 'Done'"
Write-Host ""
Write-Host "STEP 3: Get Folder ID" -ForegroundColor Yellow
Write-Host "   - Copy the folder ID from URL"
Write-Host "     Example: https://drive.google.com/drive/folders/1ABC...XYZ"
Write-Host "     The folder ID is: 1ABC...XYZ"
Write-Host ""
Write-Host "STEP 4: Configure DVC" -ForegroundColor Yellow
Write-Host "   Run: dvc remote modify gdrive url gdrive://YOUR_FOLDER_ID"
Write-Host ""
Write-Host "STEP 5: Upload Models" -ForegroundColor Yellow
Write-Host "   - Train your model locally"
Write-Host "   - Upload best_model.pt to the Google Drive folder"
Write-Host "   - Or use 'dvc push' (requires one-time OAuth login)"
Write-Host ""

Write-Host "============================================" -ForegroundColor Green
Write-Host "How It Works" -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Green
Write-Host ""
Write-Host "FOR PUSHING (uploading models):" -ForegroundColor Cyan
Write-Host "   - First time: dvc push (opens browser for Google login)"
Write-Host "   - Or manually upload files to Google Drive folder"
Write-Host ""
Write-Host "FOR PULLING (CI/CD & team members):" -ForegroundColor Cyan
Write-Host "   - No authentication needed!"
Write-Host "   - dvc pull works automatically with public folders"
Write-Host ""

# Prompt for folder ID
$FOLDER_ID = Read-Host "Enter your Google Drive folder ID (or press Enter to skip)"

if ($FOLDER_ID) {
    Write-Host "Configuring DVC remote with folder ID: $FOLDER_ID" -ForegroundColor Green
    dvc remote modify gdrive url "gdrive://$FOLDER_ID"
    Write-Host "Remote configured successfully!" -ForegroundColor Green
    Write-Host ""
    dvc remote list
}

Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "Common DVC Commands" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "dvc add models/best_model.pt    # Track a file"
Write-Host "dvc push                         # Upload to Google Drive"
Write-Host "dvc pull                         # Download from Google Drive"
Write-Host "dvc status                       # Check status"
Write-Host "============================================"
Write-Host ""
Write-Host "GitHub Secrets Required (for CI/CD):" -ForegroundColor Yellow
Write-Host "  - DOCKER_USERNAME: Docker Hub username"
Write-Host "  - DOCKER_PASSWORD: Docker Hub password/token"
Write-Host ""
Write-Host "No Google Drive credentials needed for CI/CD!" -ForegroundColor Green
Write-Host "(Public folder access works without authentication)"
Write-Host "============================================"



