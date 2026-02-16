# End-to-End Deployment Guide

## MLOps Cats vs Dogs - Complete Local Testing to Deployment Guide

This guide covers the complete workflow from local development to production deployment using Docker Compose and CI/CD pipelines.

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Local Development Setup](#local-development-setup)
3. [Data Preparation](#data-preparation)
4. [Model Training](#model-training)
5. [DVC Setup with Google Drive](#dvc-setup-with-google-drive)
6. [Local Testing](#local-testing)
7. [Docker Containerization](#docker-containerization)
8. [CI/CD Pipeline Setup](#cicd-pipeline-setup)
9. [Production Deployment](#production-deployment)
10. [Monitoring with Prometheus](#monitoring-with-prometheus)
11. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Required Software

| Software | Version | Installation |
|----------|---------|--------------|
| Python | 3.9+ | [python.org](https://www.python.org/downloads/) |
| Docker | 20.10+ | [docker.com](https://www.docker.com/get-started) |
| Docker Compose | 2.0+ | Included with Docker Desktop |
| Git | 2.30+ | [git-scm.com](https://git-scm.com/downloads) |
| DVC | 3.30+ | `pip install dvc dvc-gdrive` |

### Hardware Requirements

- **Minimum**: 8GB RAM, 4 CPU cores, 20GB disk space
- **Recommended**: 16GB RAM, 8 CPU cores, 50GB disk space, NVIDIA GPU (optional)

---

## Local Development Setup

### Step 1: Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/mlops-cats-dogs.git
cd mlops-cats-dogs
```

### Step 2: Create Virtual Environment

**Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate
```

**Linux/macOS:**
```bash
python -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
# Install core dependencies
pip install -r requirements.txt

# Install development dependencies (includes DVC, pytest, etc.)
pip install -r requirements-dev.txt
```

### Step 4: Verify Installation

```bash
# Check Python packages
python -c "import torch; print(f'PyTorch: {torch.__version__}')"
python -c "import fastapi; print(f'FastAPI: {fastapi.__version__}')"

# Check DVC
dvc version
```

---

## Data Preparation

### Step 1: Download Dataset

The dataset uses the Kaggle Dogs vs Cats competition data.

**Option A: Using Kaggle API**
```bash
# Install Kaggle API
pip install kaggle

# Set up credentials (place kaggle.json in ~/.kaggle/)
kaggle competitions download -c dogs-vs-cats -p data/raw
```

**Option B: Manual Download**
1. Visit: https://www.kaggle.com/c/dogs-vs-cats/data
2. Download `train.zip`
3. Extract to `data/raw/train/`

### Step 2: Preprocess Data

```bash
# Run preprocessing script (splits into train/val/test)
python src/data/preprocess.py

# This creates:
# - data/processed/train/cat/ and data/processed/train/dog/
# - data/processed/val/cat/ and data/processed/val/dog/
# - data/processed/test/cat/ and data/processed/test/dog/
```

### Step 3: Verify Data Split

```bash
# Check data structure
python -c "
from pathlib import Path
for split in ['train', 'val', 'test']:
    for cls in ['cat', 'dog']:
        p = Path(f'data/processed/{split}/{cls}')
        count = len(list(p.glob('*.jpg'))) if p.exists() else 0
        print(f'{split}/{cls}: {count} images')
"
```

Expected output (approximate):
```
train/cat: 10000 images
train/dog: 10000 images
val/cat: 1250 images
val/dog: 1250 images
test/cat: 1250 images
test/dog: 1250 images
```

---

## Model Training

### Step 1: Train the Model

```bash
# Basic training (default: 20 epochs)
python src/models/train.py

# Custom training
python src/models/train.py --epochs 50 --batch_size 64 --learning_rate 0.0001
```

### Step 2: Monitor Training with MLflow

```bash
# Start MLflow UI (in separate terminal)
mlflow ui --port 5000

# Open browser: http://localhost:5000
```

### Step 3: Verify Model Output

After training, you should have:
- `models/best_model.pt` - Best validation accuracy model
- `models/final_model.pt` - Final epoch model
- `models/metrics.json` - Training metrics

```bash
# Check model files
ls -lh models/
```

---

## DVC Setup with Google Drive

### Step 1: Create Google Drive Folder

1. Go to [Google Drive](https://drive.google.com)
2. Create a new folder: `mlops-cats-dogs-models`
3. Copy the folder ID from URL: `https://drive.google.com/drive/folders/FOLDER_ID`

### Step 2: Enable Public Sharing (Important!)

1. Right-click the folder → **Share**
2. Click **General access** → Change to **"Anyone with the link"**
3. Set role to **Viewer**
4. Click **Done**

> **Note:** This allows CI/CD pipelines to download models without authentication!

### Step 3: Configure DVC Remote

**Windows:**
```powershell
.\scripts\setup_dvc.ps1
```

**Linux/macOS:**
```bash
chmod +x scripts/setup_dvc.sh
./scripts/setup_dvc.sh
```

**Or manually:**
```bash
# Set the Google Drive folder ID
dvc remote modify gdrive url gdrive://YOUR_FOLDER_ID
```

### Step 4: Track Model Files with DVC

```bash
# Add model files to DVC tracking
dvc add models/best_model.pt
dvc add models/final_model.pt

# Commit the .dvc files to Git
git add models/best_model.pt.dvc models/final_model.pt.dvc models/.gitignore
git commit -m "Track models with DVC"
```

### Step 5: Upload Models to Google Drive

**Option A: Using DVC Push (requires one-time OAuth)**
```bash
# First push will open browser for Google authentication
dvc push

# Verify upload
dvc status
```

**Option B: Manual Upload (no authentication needed)**
1. Train your model locally
2. Go to your Google Drive folder
3. Upload `models/best_model.pt` and `models/final_model.pt` directly
4. The CI/CD will download using `dvc pull`

> **How It Works:**
> - **Pushing models:** Requires Google OAuth (one-time browser login) OR manual upload
> - **Pulling models (CI/CD):** No authentication needed with public folder sharing!

---

## Local Testing

### Step 1: Run Unit Tests

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=src --cov-report=html

# View coverage report
# Open htmlcov/index.html in browser
```

### Step 2: Run Linting

```bash
# Run flake8
flake8 src tests --count --show-source --statistics

# Format code (optional)
black src tests
isort src tests
```

### Step 3: Test Inference Locally

```bash
# Start the API server
uvicorn src.inference.app:app --host 0.0.0.0 --port 8000 --reload
```

**Test with curl:**
```bash
# Health check
curl http://localhost:8000/health

# Root endpoint
curl http://localhost:8000/

# Prediction (replace with actual image)
curl -X POST "http://localhost:8000/predict" \
  -H "accept: application/json" \
  -F "file=@test_image.jpg"
```

**Test with Python:**
```python
import requests
from PIL import Image
import io

# Create test image
img = Image.new('RGB', (224, 224), color='blue')
img_bytes = io.BytesIO()
img.save(img_bytes, format='JPEG')
img_bytes.seek(0)

# Send request
response = requests.post(
    'http://localhost:8000/predict',
    files={'file': ('test.jpg', img_bytes, 'image/jpeg')}
)
print(response.json())
```

---

## Docker Containerization

### Step 1: Build Docker Image

```bash
# Build image
docker build -t cats-dogs-classifier:latest .

# Verify image
docker images | grep cats-dogs
```

### Step 2: Run Container Locally

```bash
# Run container
docker run -d \
  --name cats-dogs-test \
  -p 8000:8000 \
  cats-dogs-classifier:latest

# Check logs
docker logs cats-dogs-test

# Test the API
curl http://localhost:8000/health
```

### Step 3: Stop Test Container

```bash
docker stop cats-dogs-test
docker rm cats-dogs-test
```

---

## CI/CD Pipeline Setup

### GitHub Secrets Required

Add these secrets in your GitHub repository settings:

| Secret Name | Description |
|-------------|-------------|
| `DOCKER_USERNAME` | Docker Hub username |
| `DOCKER_PASSWORD` | Docker Hub password or access token |

> **Note:** No Google Drive credentials needed! The CI/CD pulls models from the public Google Drive folder without authentication.

### CI Pipeline (Automatic on Push)

The CI pipeline ([.github/workflows/ci.yml](.github/workflows/ci.yml)) runs automatically on every push/PR:

1. **Checkout** - Clone repository
2. **Setup Python** - Install Python 3.9
3. **Install Dependencies** - Install requirements
4. **Pull Models** - DVC pull from public Google Drive folder
5. **Lint** - Run flake8
6. **Test** - Run pytest
7. **Build & Push** - Build Docker image & push to Docker Hub (main branch only)
8. **Deploy** - Deploy with Docker Compose (main branch only)

### CD Pipeline (Manual Trigger)

The CD pipeline ([.github/workflows/cd.yml](.github/workflows/cd.yml)) can be triggered manually:

1. Go to Actions > CD - Continuous Deployment
2. Click "Run workflow"
3. Select environment (staging/production)
4. Select image tag

---

## Production Deployment

### Option 1: Docker Compose (Recommended for Single Server)

```bash
# Navigate to project root
cd mlops-cats-dogs

# Set Docker username
export DOCKER_USERNAME=your_dockerhub_username

# Start services
docker compose -f deployment/docker-compose.yml up -d

# Check status
docker compose -f deployment/docker-compose.yml ps

# View logs
docker compose -f deployment/docker-compose.yml logs -f
```

**Services started:**
- `cats-dogs-classifier` - API service on port 8000
- `prometheus` - Metrics collector on port 9090

### Option 2: Local Build & Deploy

If not using Docker Hub:

```bash
# Build locally
docker compose -f deployment/docker-compose.yml build

# Deploy
docker compose -f deployment/docker-compose.yml up -d
```

### Verify Deployment

```bash
# Health check
curl http://localhost:8000/health

# Test prediction
curl -X POST http://localhost:8000/predict \
  -F "file=@test_image.jpg"

# View metrics
curl http://localhost:8000/metrics
```

### Run Smoke Tests

```bash
# Linux/macOS
chmod +x scripts/smoke_test.sh
./scripts/smoke_test.sh http://localhost:8000
```

---

## Monitoring with Prometheus

### Access Prometheus Dashboard

After deploying with Docker Compose:
- Open: http://localhost:9090

### Available Metrics

| Metric | Description |
|--------|-------------|
| `cats_dogs_requests_total` | Total prediction requests |
| `cats_dogs_inference_seconds` | Inference time histogram |
| `cats_dogs_predictions_total` | Predictions by class |
| `cats_dogs_model_loaded` | Model load status |

### Example Prometheus Queries

```promql
# Request rate (requests/second)
rate(cats_dogs_requests_total[5m])

# Average inference time
histogram_quantile(0.95, rate(cats_dogs_inference_seconds_bucket[5m]))

# Prediction distribution
sum by (predicted_class) (cats_dogs_predictions_total)

# Error rate
rate(cats_dogs_requests_total{status="error"}[5m])
```

### Grafana Integration (Optional)

```bash
# Add Grafana to docker-compose.yml
# Or run separately:
docker run -d \
  --name grafana \
  -p 3000:3000 \
  grafana/grafana

# Access: http://localhost:3000 (admin/admin)
# Add Prometheus data source: http://prometheus:9090
```

---

## Troubleshooting

### Common Issues

#### 1. Model not found
```bash
# Check if model exists
ls -la models/

# Pull from DVC
dvc pull models/

# Or create test model
python scripts/create_test_model.py
```

#### 2. Docker build fails
```bash
# Check Docker daemon
docker info

# Clean build cache
docker builder prune -a

# Build with no cache
docker build --no-cache -t cats-dogs-classifier .
```

#### 3. Container not starting
```bash
# Check logs
docker logs cats-dogs-classifier

# Check container status
docker inspect cats-dogs-classifier
```

#### 4. DVC authentication fails
```bash
# Re-authenticate
dvc remote modify --local gdrive gdrive_use_service_account false
dvc push  # Opens browser for OAuth

# Or check service account
cat $GDRIVE_CREDENTIALS_DATA | head -100
```

#### 5. Tests failing
```bash
# Run with verbose output
pytest tests/ -v --tb=long

# Run specific test
pytest tests/test_inference.py -v
```

### Getting Help

- Check logs: `docker compose logs -f`
- Debug container: `docker exec -it cats-dogs-classifier bash`
- View metrics: `curl http://localhost:8000/metrics`

---

## Quick Reference

### Essential Commands

```bash
# Development
python src/models/train.py          # Train model
pytest tests/ -v                     # Run tests
uvicorn src.inference.app:app --reload  # Start dev server

# DVC
dvc add models/best_model.pt        # Track file
dvc push                             # Upload to GDrive
dvc pull                             # Download from GDrive

# Docker
docker compose up -d                 # Start services
docker compose down                  # Stop services
docker compose logs -f               # View logs

# Deployment
./scripts/smoke_test.sh              # Run smoke tests
curl http://localhost:8000/health    # Health check
```

### API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | API info |
| `/health` | GET | Health check |
| `/predict` | POST | Image prediction |
| `/metrics` | GET | Prometheus metrics |
| `/model-info` | GET | Model information |

---

## Checklist

### Before Deployment

- [ ] All tests pass (`pytest tests/`)
- [ ] Model trained and saved
- [ ] Google Drive folder created with "Anyone with the link" sharing
- [ ] Model uploaded to Google Drive (via `dvc push` or manual upload)
- [ ] DVC remote configured (`dvc remote modify gdrive url gdrive://FOLDER_ID`)
- [ ] Docker image builds successfully
- [ ] GitHub secrets configured (`DOCKER_USERNAME`, `DOCKER_PASSWORD`)
- [ ] Smoke tests pass locally

### After Deployment

- [ ] Health endpoint returns 200
- [ ] Prediction endpoint works
- [ ] Prometheus collecting metrics
- [ ] Logs accessible
- [ ] No errors in container logs

---

*Last updated: February 2026*



