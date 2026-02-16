#!/usr/bin/env bash
# ============================================
# DVC Setup Script for Google Drive Remote
# ============================================
# This script helps configure DVC with Google Drive as remote storage
# Models are stored in Google Drive with public sharing ("Anyone with the link")
# Usage: ./scripts/setup_dvc.sh

set -e

echo "============================================"
echo "DVC Setup with Google Drive (Public Sharing)"
echo "============================================"
echo ""

# Check if DVC is installed
if ! command -v dvc &> /dev/null; then
    echo "DVC is not installed. Installing..."
    pip install dvc dvc-gdrive
fi

echo "DVC version: $(dvc version | head -1)"
echo ""

# Initialize DVC if not already initialized
if [ ! -d ".dvc" ]; then
    echo "Initializing DVC..."
    dvc init
fi

echo "Current DVC remotes:"
dvc remote list || echo "No remotes configured"
echo ""

# Instructions for setting up Google Drive
echo "============================================"
echo "Setup Instructions (Public Sharing Method)"
echo "============================================"
echo ""
echo "STEP 1: Create Google Drive Folder"
echo "   - Go to https://drive.google.com"
echo "   - Create a new folder (e.g., 'mlops-cats-dogs-models')"
echo ""
echo "STEP 2: Enable Public Sharing"
echo "   - Right-click the folder -> Share"
echo "   - Click 'General access' -> Change to 'Anyone with the link'"
echo "   - Set role to 'Viewer'"
echo "   - Click 'Done'"
echo ""
echo "STEP 3: Get Folder ID"
echo "   - Copy the folder ID from URL"
echo "     Example: https://drive.google.com/drive/folders/1ABC...XYZ"
echo "     The folder ID is: 1ABC...XYZ"
echo ""
echo "STEP 4: Configure DVC"
echo "   Run: dvc remote modify gdrive url gdrive://YOUR_FOLDER_ID"
echo ""
echo "STEP 5: Upload Models Manually"
echo "   - Train your model locally"
echo "   - Upload best_model.pt to the Google Drive folder"
echo "   - Or use 'dvc push' (requires one-time OAuth login)"
echo ""
echo "============================================"
echo "How It Works"
echo "============================================"
echo ""
echo "FOR PUSHING (uploading models):"
echo "   - First time: dvc push (opens browser for Google login)"
echo "   - Or manually upload files to Google Drive folder"
echo ""
echo "FOR PULLING (CI/CD & team members):"
echo "   - No authentication needed!"
echo "   - dvc pull works automatically with public folders"
echo ""
echo "============================================"
echo ""

# Prompt for folder ID
read -p "Enter your Google Drive folder ID (or press Enter to skip): " FOLDER_ID

if [ -n "$FOLDER_ID" ]; then
    echo "Configuring DVC remote with folder ID: $FOLDER_ID"
    dvc remote modify gdrive url "gdrive://$FOLDER_ID"
    echo "Remote configured successfully!"
    echo ""
    dvc remote list
fi

echo ""
echo "============================================"
echo "Common DVC Commands"
echo "============================================"
echo "dvc add models/best_model.pt    # Track a file"
echo "dvc push                         # Upload to Google Drive"
echo "dvc pull                         # Download from Google Drive"
echo "dvc status                       # Check status"
echo "============================================"
echo ""
echo "GitHub Secrets Required (for CI/CD):"
echo "  - DOCKER_USERNAME: Docker Hub username"
echo "  - DOCKER_PASSWORD: Docker Hub password/token"
echo ""
echo "No Google Drive credentials needed for CI/CD!"
echo "(Public folder access works without authentication)"
echo "============================================"



