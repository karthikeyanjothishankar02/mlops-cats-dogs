# MLOps Pipeline - Cats vs Dogs Image Classification

[![CI/CD](https://img.shields.io/badge/CI%2FCD-GitHub%20Actions-blue)](https://github.com/features/actions)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)
[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.1-EE4C2C?logo=pytorch&logoColor=white)](https://pytorch.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Setup from Scratch](#setup-from-scratch)
  - [Step 1: Clone the Repository](#step-1-clone-the-repository)
  - [Step 2: Create Virtual Environment](#step-2-create-virtual-environment)
  - [Step 3: Install Dependencies](#step-3-install-dependencies)
  - [Step 4: Download and Prepare Dataset](#step-4-download-and-prepare-dataset)
  - [Step 5: Train the Model](#step-5-train-the-model-optional)
  - [Step 6: Run Tests](#step-6-run-tests)
  - [Step 7: Run Locally](#step-7-run-locally)
- [Deployment](#deployment)
  - [Local Deployment with Docker Compose](#local-deployment-with-docker-compose)
  - [Production Deployment with CI/CD](#production-deployment-with-cicd)
- [API Reference](#api-reference)
- [CI/CD Pipeline](#cicd-pipeline)
- [Monitoring](#monitoring)
- [Tech Stack](#tech-stack)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

---

## Project Overview

End-to-end MLOps pipeline for binary image classification (Cats vs Dogs) designed for a pet adoption platform. This project demonstrates production-ready machine learning deployment with:

- **Automated CI/CD** using GitHub Actions
- **Containerized deployment** with Docker
- **Experiment tracking** with MLflow
- **Data versioning** with DVC
- **Production-grade API** with FastAPI

The classifier achieves **>90% accuracy** and can process images in **50-200ms** on CPU.

---

## Features

| Feature | Description |
|---------|-------------|
| **CNN Model** | Custom 4-block CNN architecture (~50M parameters) for binary classification |
| **FastAPI Service** | Production-ready REST API with automatic OpenAPI documentation |
| **Docker Support** | Multi-stage Dockerfile for optimized container images |
| **CI/CD Pipeline** | Automated testing, building, and deployment with GitHub Actions |
| **Experiment Tracking** | MLflow integration for tracking metrics, parameters, and artifacts |
| **Data Versioning** | DVC for reproducible data pipelines |
| **Health Checks** | Docker-ready liveness and readiness probes |
| **Monitoring** | Prometheus metrics and structured logging |
| **Comprehensive Tests** | 20+ unit tests with coverage reporting |

---

## Project Structure

```
mlops-cats-dogs/
├── .github/
│   └── workflows/
│       ├── ci.yml                 # CI pipeline (test, build, push)
│       └── cd.yml                 # CD pipeline (deploy)
├── data/
│   ├── raw/                       # Raw dataset (Kaggle)
│   └── processed/                 # Preprocessed images
├── deployment/
│   ├── docker-compose.yml         # Docker Compose configuration
│   └── prometheus/
│       └── prometheus.yml         # Prometheus config
├── models/
│   ├── best_model.pt              # Best performing model
│   └── final_model.pt             # Final trained model
├── scripts/
│   ├── download_data.py           # Dataset download script
│   ├── setup.sh                   # Environment setup script
│   └── smoke_test.sh              # Post-deployment tests
├── src/
│   ├── data/
│   │   ├── augmentation.py        # Data augmentation utilities
│   │   └── preprocess.py          # Data preprocessing pipeline
│   ├── inference/
│   │   ├── app.py                 # FastAPI application
│   │   └── predictor.py           # Prediction logic
│   ├── models/
│   │   ├── cnn_model.py           # CNN architecture definition
│   │   └── train.py               # Training script
│   └── utils/
│       ├── config.py              # Configuration settings
│       ├── metrics.py             # Metrics utilities
│       └── monitoring.py          # Monitoring utilities
├── tests/
│   ├── test_inference.py          # Inference tests
│   └── test_preprocess.py         # Preprocessing tests
├── Dockerfile                     # Multi-stage Docker build
├── dvc.yaml                       # DVC pipeline definition
├── requirements.txt               # Production dependencies
├── requirements-dev.txt           # Development dependencies
└── README.md                      # This file
```

---

## Prerequisites

Before starting, ensure you have the following installed:

| Software | Version | Check Command | Download Link |
|----------|---------|---------------|---------------|
| Python | 3.9+ | `python --version` | [python.org](https://www.python.org/downloads/) |
| Git | Latest | `git --version` | [git-scm.com](https://git-scm.com/downloads) |
| Docker | Latest | `docker --version` | [docker.com](https://www.docker.com/products/docker-desktop) |
| Docker Compose | Latest | `docker-compose --version` | Included with Docker Desktop |

**Accounts Required:**
- [GitHub Account](https://github.com/signup) - For repository and CI/CD
- [Docker Hub Account](https://hub.docker.com/signup) - For container registry
- [Kaggle Account](https://www.kaggle.com/account/login) - For dataset download

---

## Setup from Scratch

### Step 1: Clone the Repository

```bash
# Clone the repository
git clone https://github.com/YOUR-USERNAME/mlops-cats-dogs.git
cd mlops-cats-dogs
```

### Step 2: Create Virtual Environment

**Windows (PowerShell):**
```powershell
# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\activate

# You should see (venv) in your prompt
```

**Linux/macOS:**
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
# Upgrade pip
python -m pip install --upgrade pip

# Install production dependencies
pip install -r requirements.txt

# Install development dependencies (for testing)
pip install -r requirements-dev.txt
```

**Verify Installation:**
```bash
python -c "import torch; print(f'PyTorch: {torch.__version__}')"
python -c "import fastapi; print(f'FastAPI: {fastapi.__version__}')"
python -c "import mlflow; print(f'MLflow: {mlflow.__version__}')"
```

### Step 4: Download and Prepare Dataset

**Option A: Download from Kaggle (Manual)**

1. Go to [Kaggle Dogs vs Cats Competition](https://www.kaggle.com/c/dogs-vs-cats/data)
2. Download `train.zip` and extract to `data/raw/train/`
3. You should have images like: `dog.0.jpg`, `cat.0.jpg`, etc.

**Option B: Using the Download Script**
```bash
# Requires Kaggle API credentials configured
python scripts/download_data.py
```

**Run Preprocessing:**
```bash
# Preprocess and split data into train/val/test
python src/data/preprocess.py
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

### Step 5: Train the Model (Optional)

> **Note:** Pre-trained models (`best_model.pt`, `final_model.pt`) are already included in the `models/` directory. Skip this step if you want to use them.

**Start MLflow Tracking Server (Optional - in separate terminal):**
```bash
mlflow ui --port 5000
# Access at http://localhost:5000
```

**Train the Model:**
```bash
# Train with default parameters
python src/models/train.py --epochs 20 --batch_size 32

# Or customize training
python src/models/train.py --epochs 30 --batch_size 64 --learning_rate 0.0001
```

**Training Time:**
- CPU: ~2-3 hours
- GPU: ~15-30 minutes

### Step 6: Run Tests

```bash
# Run all tests
pytest tests/ -v

# Run with coverage report
pytest tests/ -v --cov=src --cov-report=term-missing

# Run specific test file
pytest tests/test_inference.py -v
```

**Expected Output:**
```
tests/test_preprocess.py::TestPreprocessing::test_load_and_preprocess_image_shape PASSED
tests/test_inference.py::TestInference::test_predictor_initialization PASSED
...
===================== 20 passed in 5.23s =====================
```

### Step 7: Run Locally

**Start the FastAPI Server:**
```bash
uvicorn src.inference.app:app --host 0.0.0.0 --port 8000 --reload
```

**Test the API:**
```bash
# Health check
curl http://localhost:8000/health

# Root endpoint
curl http://localhost:8000/

# Test prediction (replace with actual image path)
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@data/processed/test/cat.0.jpg"
```

**Access Interactive Docs:**
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

---

## Deployment

### Local Deployment with Docker Compose

**Start Services:**
```bash
cd deployment

# Set your Docker username (optional for local builds)
export DOCKER_USERNAME=local

# Start services
docker-compose up -d

# Check status
docker-compose ps
```

**View Logs:**
```bash
docker-compose logs -f cats-dogs-classifier
```

**Access Services:**
| Service | URL |
|---------|-----|
| API | http://localhost:8000 |
| API Docs | http://localhost:8000/docs |
| Health Check | http://localhost:8000/health |
| Prometheus Metrics | http://localhost:8000/metrics |
| Prometheus UI | http://localhost:9090 |

**Stop Services:**
```bash
docker-compose down
```

### Production Deployment with CI/CD

#### Step 1: Create Docker Hub Repository

1. Go to [Docker Hub](https://hub.docker.com/)
2. Click **Create Repository**
3. Name it `cats-dogs-classifier`
4. Set visibility to **Public**

#### Step 2: Create Docker Hub Access Token

1. Go to **Account Settings** → **Security**
2. Click **New Access Token**
3. Description: `github-actions-mlops`
4. Permissions: Read, Write, Delete
5. **Copy the token immediately!**

#### Step 3: Configure GitHub Secrets

1. Go to your GitHub repository
2. Navigate to **Settings** → **Secrets and variables** → **Actions**
3. Add these secrets:

| Secret Name | Value |
|-------------|-------|
| `DOCKER_USERNAME` | Your Docker Hub username |
| `DOCKER_PASSWORD` | Your Docker Hub access token |

#### Step 4: Push to GitHub

```bash
# Add all files
git add .

# Commit
git commit -m "Initial commit: MLOps pipeline with CI/CD"

# Push to main branch
git push -u origin main
```

#### Step 5: Monitor Deployment

1. Go to your GitHub repository
2. Click **Actions** tab
3. Watch the **CI/CD** workflow run

**CI Pipeline Stages:**
- ✅ Checkout code
- ✅ Setup Python environment
- ✅ Install dependencies
- ✅ Run linting (flake8)
- ✅ Run tests (pytest)
- ✅ Build Docker image
- ✅ Push to Docker Hub

**CD Pipeline Stages (after CI success):**
- ✅ Pull latest image
- ✅ Deploy with Docker Compose
- ✅ Run smoke tests
- ✅ Verify health endpoint

#### Step 6: Verify Deployment

```bash
# Test the deployed service
curl http://localhost:8000/health

# Test prediction endpoint
curl -X POST "http://localhost:8000/predict" \
  -F "file=@data/processed/test/cat.0.jpg"
```

---

## API Reference

### Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Root endpoint with API info |
| `GET` | `/health` | Health check (for load balancers) |
| `GET` | `/docs` | Interactive Swagger documentation |
| `GET` | `/metrics` | Prometheus metrics (text format) |
| `GET` | `/metrics/json` | Metrics in JSON format (legacy) |
| `POST` | `/predict` | Image classification |

### Predict Endpoint

**Request:**
```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@image.jpg"
```

**Response:**
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

### Health Endpoint

**Response:**
```json
{
  "status": "healthy",
  "model_loaded": true
}
```

---

## CI/CD Pipeline

### Continuous Integration (CI)

Triggered on every push/PR to `main` branch:

```yaml
# .github/workflows/ci.yml
- Checkout code with LFS support
- Setup Python 3.9
- Install dependencies
- Run flake8 linting
- Run pytest tests
- Build Docker image
- Push to Docker Hub (main branch only)
```

### Continuous Deployment (CD)

Triggered after successful CI on `main` branch:

```yaml
# .github/workflows/cd.yml
- Pull latest Docker image
- Deploy with Docker Compose
- Wait for health check
- Run smoke tests
- Rollback on failure
```

### Manual Deployment

You can also trigger deployment manually:

1. Go to **Actions** tab
2. Select **Manual Deploy** workflow
3. Click **Run workflow**
4. Choose environment (staging/production)

---

## Monitoring

### Prometheus Metrics

The application exposes metrics at `/metrics` endpoint for Prometheus scraping.

**Access Metrics:**
```bash
# View raw metrics
curl http://localhost:8000/metrics
```

**Prometheus Configuration:**

The Prometheus config is located at `deployment/prometheus/prometheus.yml`:

```yaml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'cats-dogs-classifier'
    metrics_path: '/metrics'
    static_configs:
      - targets: ['cats-dogs-classifier:8000']
```

**Available Metrics:**
| Metric | Type | Description |
|--------|------|-------------|
| `cats_dogs_requests_total` | Counter | Total number of requests (with `status` label) |
| `cats_dogs_inference_seconds` | Histogram | Inference time distribution |
| `cats_dogs_predictions_total` | Counter | Predictions by class (with `class` label) |
| `cats_dogs_model_loaded` | Gauge | Model loaded status (1 or 0) |

**Example Prometheus Queries:**
```promql
# Request rate per second
rate(cats_dogs_requests_total[5m])

# Average inference time
rate(cats_dogs_inference_seconds_sum[5m]) / rate(cats_dogs_inference_seconds_count[5m])

# Success rate
sum(rate(cats_dogs_requests_total{status="success"}[5m])) / sum(rate(cats_dogs_requests_total[5m]))
```

### MLflow Experiment Tracking

```bash
# Start MLflow UI
mlflow ui --port 5000

# Access at http://localhost:5000
```

Track:
- Training metrics (loss, accuracy)
- Model parameters
- Model artifacts

### Application Logs

```bash
# Docker Compose
docker-compose logs -f cats-dogs-classifier
```

Logs are also stored in the `logs/` directory:
- `app_YYYYMMDD.log` - Application logs
- `requests_YYYYMMDD.json` - Request/response logs
- `metrics.json` - Performance metrics

---

## Tech Stack

| Category | Technology |
|----------|------------|
| **ML Framework** | PyTorch 2.1+ |
| **API Framework** | FastAPI 0.104+ |
| **Experiment Tracking** | MLflow 2.8+ |
| **Data Versioning** | DVC 3.30+ |
| **Containerization** | Docker (multi-stage builds) |
| **CI/CD** | GitHub Actions |
| **Testing** | Pytest with coverage |
| **Monitoring** | Prometheus |

---

## Troubleshooting

### Common Issues

**1. Docker build fails with "out of memory"**
```bash
# Free up Docker resources
docker system prune -af
docker volume prune -f
```

**2. Model file not found error**
```bash
# Verify model files exist
ls -la models/
# Should show: best_model.pt, final_model.pt
```

**3. Port 8000 already in use**
```bash
# Find and kill process using port 8000
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/macOS
lsof -i :8000
kill -9 <PID>
```

**4. CUDA/GPU not detected**
```bash
# Check PyTorch CUDA availability
python -c "import torch; print(torch.cuda.is_available())"
```

**5. Tests failing**
```bash
# Run tests with verbose output
pytest tests/ -v --tb=long

# Check specific test
pytest tests/test_inference.py -v
```

### Getting Help

1. Check the [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for detailed instructions
2. Review GitHub Actions logs in the **Actions** tab
3. Open an issue in the repository

---

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Make your changes
4. Run tests: `pytest tests/ -v --cov=src`
5. Commit: `git commit -m "Add my feature"`
6. Push: `git push origin feature/my-feature`
7. Submit a pull request

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Acknowledgments

- Dataset: [Kaggle Dogs vs Cats](https://www.kaggle.com/c/dogs-vs-cats)
- Built with [FastAPI](https://fastapi.tiangolo.com/), [PyTorch](https://pytorch.org/), and [MLflow](https://mlflow.org/)



