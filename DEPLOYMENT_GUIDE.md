# Step-by-Step Deployment Guide

Complete guide to deploy the MLOps Cats vs Dogs classifier from local development to production using Docker and GitHub Actions CI/CD.

---

## 📋 Table of Contents

1. [Prerequisites](#step-1-prerequisites)
2. [Local Environment Setup](#step-2-local-environment-setup)
3. [Download and Prepare Dataset](#step-3-download-and-prepare-dataset)
4. [Train Model Locally](#step-4-train-model-locally)
5. [Test Locally](#step-5-test-locally)
6. [Docker Hub Setup](#step-6-docker-hub-setup)
7. [GitHub Repository Setup](#step-7-github-repository-setup)
8. [Configure GitHub Secrets](#step-8-configure-github-secrets)
9. [Push and Deploy](#step-9-push-and-deploy)
10. [Monitor Deployment](#step-10-monitor-deployment)
11. [Verify Deployment](#step-11-verify-deployment)
12. [Troubleshooting](#troubleshooting)

---

## Step 1: Prerequisites

### 1.1 Check Required Software

Verify you have all required software installed:

```powershell
# Check Python version (should be 3.9 or higher)
python --version

# Check Git
git --version

# Check Docker
docker --version

# Check Docker Compose
docker-compose --version
```

### 1.2 Install Missing Software

If any software is missing:

**Python 3.9+**
- Download from: https://www.python.org/downloads/
- During installation, check "Add Python to PATH"

**Git**
- Download from: https://git-scm.com/downloads
- Use default installation options

**Docker Desktop**
- Download from: https://www.docker.com/products/docker-desktop
- Start Docker Desktop after installation
- Ensure it's running (check system tray icon)

### 1.3 Accounts Setup

Create accounts if you don't have them:

- **GitHub Account**: https://github.com/signup
- **Docker Hub Account**: https://hub.docker.com/signup
- **Kaggle Account**: https://www.kaggle.com/account/login (for dataset)

---

## Step 2: Local Environment Setup

### 2.1 Navigate to Project Directory

```powershell
cd "C:\Users\kdrz653\OneDrive - AZCollaboration\Desktop\MLOPS\mlops-cats-dogs"
```

### 2.2 Create Virtual Environment

```powershell
# Create virtual environment
python -m venv venv

# Activate virtual environment (Windows)
.\venv\Scripts\activate

# You should see (venv) in your prompt
```

### 2.3 Install Dependencies

```powershell
# Upgrade pip
python -m pip install --upgrade pip

# Install production dependencies
pip install -r requirements.txt

# Install development dependencies
pip install -r requirements-dev.txt
```

**Expected Output:**
```
Successfully installed torch-2.0.0 fastapi-0.104.0 mlflow-2.8.0 ...
```

### 2.4 Verify Installation

```powershell
# Check PyTorch installation
python -c "import torch; print(f'PyTorch: {torch.__version__}')"

# Check FastAPI installation
python -c "import fastapi; print(f'FastAPI: {fastapi.__version__}')"

# Check MLflow installation
python -c "import mlflow; print(f'MLflow: {mlflow.__version__}')"
```

---

## Step 3: Download and Prepare Dataset

### 3.1 Download Dataset from Kaggle

1. Go to: https://www.kaggle.com/c/dogs-vs-cats/data
2. Click "Download All"
3. Extract the zip file
4. You'll get `train.zip` and `test1.zip`

### 3.2 Organize Dataset

```powershell
# Create data directories
New-Item -ItemType Directory -Force -Path "data\raw\train"
New-Item -ItemType Directory -Force -Path "data\raw\test"

# Extract images to data/raw/train/
# You should have files like: dog.0.jpg, cat.0.jpg, etc.
```

### 3.3 Run Preprocessing

```powershell
# Run preprocessing script
python src\data\preprocess.py
```

**Expected Output:**
```
Processing images...
Processed 25000 images
Train: 20000 images (80%)
Validation: 2500 images (10%)
Test: 2500 images (10%)
Preprocessing complete!
```

**Result:**
- `data/processed/train/` - Training images
- `data/processed/val/` - Validation images
- `data/processed/test/` - Test images

---

## Step 4: Train Model Locally

### 4.1 Start MLflow Tracking Server (Optional)

Open a **new terminal** window:

```powershell
# Activate environment
.\venv\Scripts\activate

# Start MLflow UI
mlflow ui --port 5000
```

Keep this terminal open. Access MLflow at: http://localhost:5000

### 4.2 Train the Model

Back in your main terminal:

```powershell
# Train with default parameters
python src\models\train.py --epochs 20 --batch_size 32

# Or customize training
python src\models\train.py --epochs 30 --batch_size 64 --learning_rate 0.0001
```

**Expected Output:**
```
Epoch 1/20
Train Loss: 0.5234, Train Acc: 0.7456
Val Loss: 0.4123, Val Acc: 0.8234
...
Training complete!
Best model saved to: models/best_model.pt
```

**Training Time:**
- CPU: ~2-3 hours
- GPU: ~15-30 minutes

### 4.3 Verify Model Files

```powershell
# Check model files exist
Get-ChildItem models\

# Should show:
# best_model.pt
# final_model.pt
# metrics.json
```

---

## Step 5: Test Locally

### 5.1 Run Unit Tests

```powershell
# Run all tests
pytest tests\ -v

# Run with coverage report
pytest tests\ -v --cov=src --cov-report=term-missing

# Run specific test file
pytest tests\test_preprocess.py -v
pytest tests\test_inference.py -v
```

**Expected Output:**
```
tests/test_preprocess.py::TestPreprocessing::test_load_and_preprocess_image_shape PASSED
tests/test_preprocess.py::TestPreprocessing::test_load_and_preprocess_image_normalization PASSED
...
===================== 20 passed in 5.23s =====================
```

### 5.2 Test FastAPI Service Locally

**Terminal 1: Start the API**
```powershell
# Activate environment
.\venv\Scripts\activate

# Start FastAPI server
uvicorn src.inference.app:app --host 0.0.0.0 --port 8000 --reload
```

**Expected Output:**
```
INFO:     Started server process
INFO:     Uvicorn running on http://0.0.0.0:8000
```

**Terminal 2: Test Endpoints**
```powershell
# Test health endpoint
curl http://localhost:8000/health

# Expected: {"status": "healthy", "model_loaded": true}

# Test root endpoint
curl http://localhost:8000/

# Test with browser
# Open: http://localhost:8000/docs (Swagger UI)
```

### 5.3 Test Prediction with Image

```powershell
# Test prediction (replace with actual image path)
curl -X POST "http://localhost:8000/predict" `
  -H "accept: application/json" `
  -H "Content-Type: multipart/form-data" `
  -F "file=@data\processed\test\cat.0.jpg"
```

**Expected Response:**
```json
{
  "prediction": "cat",
  "confidence": 0.9523,
  "probabilities": {
    "cat": 0.9523,
    "dog": 0.0477
  }
}
```

### 5.4 Stop Local Server

Press `Ctrl+C` in Terminal 1 to stop the server.

---

## Step 6: Docker Hub Setup

### 6.1 Create Docker Hub Repository

1. Go to: https://hub.docker.com/
2. Sign in to your account
3. Click **Create Repository**
4. Fill in details:
   - **Name**: `cats-dogs-classifier`
   - **Visibility**: Public
   - **Description**: "MLOps Cats vs Dogs Binary Classifier"
5. Click **Create**

### 6.2 Create Access Token

1. Click your username → **Account Settings**
2. Go to **Security** tab
3. Click **New Access Token**
4. Settings:
   - **Description**: `github-actions-mlops`
   - **Access permissions**: Read, Write, Delete
5. Click **Generate**
6. **IMPORTANT**: Copy the token immediately (you won't see it again!)

Example token: `dckr_pat_1234567890abcdefghijklmnop`

### 6.3 Test Docker Hub Login

```powershell
# Login to Docker Hub
docker login

# Enter username and password (use the access token as password)
```

**Expected Output:**
```
Login Succeeded
```

---

## Step 7: GitHub Repository Setup

### 7.1 Create GitHub Repository

1. Go to: https://github.com/new
2. Fill in details:
   - **Repository name**: `mlops-cats-dogs`
   - **Description**: "End-to-end MLOps pipeline for Cats vs Dogs classification"
   - **Visibility**: Public or Private
3. **DO NOT** initialize with README, .gitignore, or license
4. Click **Create repository**

### 7.2 Initialize Git (if not already done)

```powershell
# Check if git is initialized
git status

# If not initialized, run:
git init
git branch -M main
```

### 7.3 Add Remote Repository

```powershell
# Add GitHub remote (replace with your username)
git remote add origin https://github.com/YOUR-USERNAME/mlops-cats-dogs.git

# Verify remote
git remote -v
```

---

## Step 8: Configure GitHub Secrets

### 8.1 Navigate to Repository Settings

1. Go to your GitHub repository
2. Click **Settings** (top right)
3. In left sidebar: **Secrets and variables** → **Actions**
4. Click **New repository secret**

### 8.2 Add Docker Hub Username

1. Click **New repository secret**
2. Fill in:
   - **Name**: `DOCKER_USERNAME`
   - **Secret**: Your Docker Hub username (e.g., `johndoe`)
3. Click **Add secret**

### 8.3 Add Docker Hub Password

1. Click **New repository secret** again
2. Fill in:
   - **Name**: `DOCKER_PASSWORD`
   - **Secret**: Paste your Docker Hub access token from Step 6.2
3. Click **Add secret**

### 8.4 Verify Secrets

You should see both secrets listed:
```
DOCKER_USERNAME
DOCKER_PASSWORD
```

**Note:** Values are hidden for security.

---

## Step 9: Push and Deploy

### 9.1 Prepare Repository

```powershell
# Check git status
git status

# Add all files
git add .

# Check what will be committed
git status
```

### 9.2 Create .gitignore (if needed)

Ensure these are in `.gitignore`:
```
venv/
__pycache__/
*.pyc
data/raw/
data/processed/
models/*.pt
mlruns/
logs/
.env
*.log
```

### 9.3 Commit Changes

```powershell
# Commit with descriptive message
git commit -m "Initial commit: MLOps pipeline with CI/CD"

# Verify commit
git log --oneline
```

### 9.4 Push to GitHub

```powershell
# Push to main branch
git push -u origin main
```

**Expected Output:**
```
Enumerating objects: 45, done.
Counting objects: 100% (45/45), done.
...
To https://github.com/YOUR-USERNAME/mlops-cats-dogs.git
 * [new branch]      main -> main
```

---

## Step 10: Monitor Deployment

### 10.1 Watch CI Pipeline

1. Go to your GitHub repository
2. Click **Actions** tab (top navigation)
3. You'll see **CI Pipeline** workflow running

**CI Pipeline Stages:**
- ✓ Setup environment
- ✓ Install dependencies
- ✓ Run linting (flake8)
- ✓ Run tests (pytest)
- ✓ Build Docker image
- ✓ Test Docker image
- ✓ Push to Docker Hub

**Expected Duration:** 3-5 minutes

### 10.2 View CI Logs

1. Click on the running workflow
2. Click on **test-and-build** job
3. Expand each step to see logs

**Common stages to monitor:**
```
Run unit tests
  - pytest tests/ -v --cov=src
  
Build Docker image
  - docker build -t ...
  
Push Docker image
  - docker push ...
```

### 10.3 Watch CD Pipeline (After CI Success)

After CI completes successfully on `main` branch:

1. **CD Pipeline** will automatically start
2. Go to **Actions** tab
3. Click on **CD Pipeline** workflow

**CD Pipeline Stages:**
- ✓ Pull latest image
- ✓ Deploy with Docker Compose
- ✓ Run smoke tests
- ✓ Verify health endpoint
- ✓ Test prediction endpoint

**Expected Duration:** 1-2 minutes

### 10.4 Check Docker Hub

1. Go to: https://hub.docker.com/
2. Navigate to your repository: `YOUR-USERNAME/cats-dogs-classifier`
3. Check **Tags** tab
4. You should see: `latest`, commit SHA tags

---

## Step 11: Verify Deployment

### 11.1 Local Docker Deployment

Test the deployed Docker image locally:

```powershell
# Pull the image from Docker Hub
docker pull YOUR-DOCKERHUB-USERNAME/cats-dogs-classifier:latest

# Run container
docker run -d -p 8000:8000 --name cats-dogs-test YOUR-DOCKERHUB-USERNAME/cats-dogs-classifier:latest

# Wait a few seconds for startup
Start-Sleep -Seconds 10

# Test health endpoint
curl http://localhost:8000/health

# Test prediction
curl -X POST "http://localhost:8000/predict" `
  -F "file=@data\processed\test\cat.0.jpg"

# View logs
docker logs cats-dogs-test

# Stop and remove
docker stop cats-dogs-test
docker rm cats-dogs-test
```

### 11.2 Docker Compose Deployment

```powershell
# Navigate to deployment directory
cd deployment

# Start all services
docker-compose up -d

# Check service status
docker-compose ps

# View logs
docker-compose logs -f cats-dogs-classifier

# Test endpoints
curl http://localhost:8000/health
curl http://localhost:8000/

# Access services:
# - API: http://localhost:8000
# - API Docs: http://localhost:8000/docs
# - MLflow: http://localhost:5001
# - Prometheus: http://localhost:9090
# - Grafana: http://localhost:3000 (admin/admin)
```

### 11.3 Run Smoke Tests

```powershell
# Navigate back to root
cd ..

# Run smoke test script
bash scripts\smoke_test.sh http://localhost:8000

# Or use Git Bash if bash not available
# Or run tests manually with curl
```

**Expected Output:**
```
==================================
Running Smoke Tests
==================================
Test 1: Health Check
✓ Health check passed (HTTP 200)

Test 2: Root Endpoint
✓ Root endpoint accessible (HTTP 200)

Test 3: Prediction Test
✓ Prediction successful (HTTP 200)

==================================
Tests Passed: 3/3
Tests Failed: 0/3
==================================
```

### 11.4 Verify Application Logs

```powershell
# View recent logs
docker-compose -f deployment\docker-compose.yml logs --tail=50 cats-dogs-classifier

# Follow logs in real-time
docker-compose -f deployment\docker-compose.yml logs -f cats-dogs-classifier
```

**Look for:**
```
INFO: Started server process
INFO: Uvicorn running on http://0.0.0.0:8000
INFO: Model loaded successfully
```

### 11.5 Check Metrics

```powershell
# Get Prometheus metrics
curl http://localhost:8000/metrics
```

**Expected Output:**
```
# HELP prediction_requests_total Total prediction requests
# TYPE prediction_requests_total counter
prediction_requests_total{class="cat"} 15
prediction_requests_total{class="dog"} 8
...
```

---

## Step 12: Post-Deployment Tasks

### 12.1 MLflow Tracking

Access MLflow UI to view training experiments:

```powershell
# If using docker-compose, MLflow is already running
# Access at: http://localhost:5001

# Or start separately:
mlflow ui --port 5001
```

View:
- All training runs
- Parameters (epochs, batch_size, learning_rate)
- Metrics (accuracy, loss, F1-score)
- Artifacts (model files, confusion matrix)

### 12.2 Monitoring Setup

**Prometheus** (http://localhost:9090):
1. Query: `rate(http_requests_total[5m])`
2. View request rates and latencies

**Grafana** (http://localhost:3000):
1. Login: admin/admin
2. Add Prometheus data source: http://prometheus:9090
3. Create dashboards for monitoring

### 12.3 Create Test Dataset

```powershell
# Copy some test images for easy testing
New-Item -ItemType Directory -Force -Path "test_images"
Copy-Item "data\processed\test\cat.*.jpg" -Destination "test_images\" -Force
Copy-Item "data\processed\test\dog.*.jpg" -Destination "test_images\" -Force
```

### 12.4 Performance Testing

```powershell
# Test multiple predictions
Get-ChildItem test_images\*.jpg | ForEach-Object {
    Write-Host "Testing: $($_.Name)"
    curl -X POST "http://localhost:8000/predict" -F "file=@$($_.FullName)"
}
```

---

## Troubleshooting

### Issue 1: CI Pipeline Fails at "Push to Docker Hub"

**Error:** `denied: requested access to the resource is denied`

**Solution:**
1. Verify GitHub secrets are set correctly
2. Check Docker Hub username is exact (case-sensitive)
3. Regenerate Docker Hub access token
4. Update `DOCKER_PASSWORD` secret in GitHub

### Issue 2: Tests Fail Locally

**Error:** `ModuleNotFoundError: No module named 'src'`

**Solution:**
```powershell
# Add project root to PYTHONPATH
$env:PYTHONPATH = (Get-Location).Path
pytest tests\ -v
```

### Issue 3: Model File Not Found

**Error:** `FileNotFoundError: models/best_model.pt not found`

**Solution:**
```powershell
# Ensure model is trained
python src\models\train.py --epochs 5

# Or use a pretrained model
# Download and place in models/ directory
```

### Issue 4: Docker Build Fails

**Error:** `ERROR [internal] load metadata for docker.io/library/python:3.9-slim`

**Solution:**
```powershell
# Check Docker is running
docker ps

# If not, start Docker Desktop

# Clean Docker cache
docker system prune -a

# Retry build
docker build -t cats-dogs-classifier:latest .
```

### Issue 5: Port 8000 Already in Use

**Error:** `Error: bind: address already in use`

**Solution:**
```powershell
# Find process using port 8000
netstat -ano | findstr :8000

# Kill the process (replace PID)
taskkill /PID <PID> /F

# Or use different port
docker run -p 8080:8000 cats-dogs-classifier:latest
```

### Issue 6: GitHub Actions Stuck

**Error:** Workflow doesn't start or is pending

**Solution:**
1. Check GitHub Actions are enabled: Settings → Actions → General
2. Ensure GitHub Actions have permissions: Settings → Actions → General → Workflow permissions
3. Check GitHub status: https://www.githubstatus.com/

### Issue 7: Docker Compose Fails

**Error:** `ERROR: Service 'cats-dogs-classifier' failed to build`

**Solution:**
```powershell
# Check Docker Compose version
docker-compose --version

# Navigate to deployment directory
cd deployment

# Build explicitly
docker-compose build --no-cache

# Try starting again
docker-compose up -d
```

### Issue 8: Insufficient Memory

**Error:** `RuntimeError: CUDA out of memory` or system slowdown

**Solution:**
```powershell
# Reduce batch size
python src\models\train.py --batch_size 16

# Or train on CPU only
python src\models\train.py --device cpu

# Increase Docker memory limit
# Docker Desktop → Settings → Resources → Memory
```

---

## Quick Reference Commands

### Daily Development Workflow

```powershell
# 1. Activate environment
.\venv\Scripts\activate

# 2. Run tests
pytest tests\ -v

# 3. Start API locally
uvicorn src.inference.app:app --reload

# 4. Test endpoints
curl http://localhost:8000/health

# 5. Commit and push
git add .
git commit -m "Your changes"
git push origin main
```

### Docker Commands

```powershell
# Build image
docker build -t cats-dogs-classifier:latest .

# Run container
docker run -d -p 8000:8000 --name ml-api cats-dogs-classifier:latest

# View logs
docker logs ml-api

# Stop container
docker stop ml-api

# Remove container
docker rm ml-api

# Clean up
docker system prune -a
```

### Docker Compose Commands

```powershell
# Start services
docker-compose -f deployment\docker-compose.yml up -d

# View status
docker-compose -f deployment\docker-compose.yml ps

# View logs
docker-compose -f deployment\docker-compose.yml logs -f

# Stop services
docker-compose -f deployment\docker-compose.yml down

# Restart specific service
docker-compose -f deployment\docker-compose.yml restart cats-dogs-classifier
```

---

## Success Checklist

Before considering deployment complete, verify:

- [ ] All unit tests pass locally
- [ ] Docker image builds successfully
- [ ] Local Docker container runs and responds
- [ ] GitHub secrets configured correctly
- [ ] CI pipeline passes (green checkmark on commit)
- [ ] Docker image pushed to Docker Hub
- [ ] CD pipeline deploys successfully
- [ ] Smoke tests pass
- [ ] Health endpoint returns 200
- [ ] Prediction endpoint works with test images
- [ ] MLflow tracking accessible
- [ ] Logs are being written
- [ ] Metrics endpoint returns data

---

## Next Steps

After successful deployment:

1. **Monitor Performance**: Check logs and metrics regularly
2. **Collect Feedback**: Test with real images
3. **Iterate**: Retrain model with new data
4. **Scale**: Increase replicas if needed
5. **Secure**: Add authentication for production
6. **Optimize**: Profile and improve inference speed
7. **Document**: Add custom changes and learnings

---

## Support Resources

- **Project Documentation**: [README.md](README.md)
- **Requirements Checklist**: [ASSIGNMENT_CHECKLIST.md](ASSIGNMENT_CHECKLIST.md)
- **Quick Setup**: [SETUP_GUIDE.md](SETUP_GUIDE.md)
- **GitHub Setup**: [GITHUB_SETUP.md](GITHUB_SETUP.md)
- **FastAPI Docs**: http://localhost:8000/docs
- **MLflow UI**: http://localhost:5001

---

**Deployment Status**: ✅ Ready to deploy!

Last Updated: February 10, 2026
