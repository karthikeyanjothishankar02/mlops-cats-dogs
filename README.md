# MLOps Pipeline - Cats vs Dogs Image Classification

[![CI](https://img.shields.io/badge/CI-GitHub%20Actions-blue)]()
[![Docker](https://img.shields.io/badge/docker-ready-blue)]()
[![Tests](https://img.shields.io/badge/tests-passing-brightgreen)]()

## Project Overview
End-to-end MLOps pipeline for binary image classification (Cats vs Dogs) for a pet adoption platform. This project implements automated CI/CD using GitHub Actions and Docker-based deployment.

## Features
- **Model Development**: CNN-based binary classifier with experiment tracking
- **Data Versioning**: DVC for dataset version control
- **Experiment Tracking**: MLflow for tracking metrics, parameters, and artifacts
- **Containerization**: Docker-based deployment
- **CI/CD**: Automated testing, building, and deployment with GitHub Actions
- **Monitoring**: Request logging and performance metrics

## Project Structure
```
mlops-cats-dogs/
├── data/                          # Data directory (DVC tracked)
│   ├── raw/                       # Raw dataset
│   ├── processed/                 # Preprocessed images
│   └── .gitignore
├── src/                           # Source code
│   ├── data/                      # Data processing scripts
│   │   ├── __init__.py
│   │   ├── preprocess.py          # Data preprocessing
│   │   └── augmentation.py        # Data augmentation
│   ├── models/                    # Model definitions
│   │   ├── __init__.py
│   │   ├── cnn_model.py           # CNN architecture
│   │   └── train.py               # Training script
│   ├── inference/                 # Inference service
│   │   ├── __init__.py
│   │   ├── app.py                 # FastAPI application
│   │   └── predictor.py           # Prediction logic
│   └── utils/                     # Utility functions
│       ├── __init__.py
│       ├── config.py              # Configuration
│       └── metrics.py             # Metrics utilities
├── tests/                         # Unit tests
│   ├── __init__.py
│   ├── test_preprocess.py
│   └── test_inference.py
├── models/                        # Trained models (gitignored)
├── mlruns/                        # MLflow tracking (gitignored)
├── deployment/                    # Deployment configurations
│   ├── docker-compose.yml         # Docker Compose config
│   └── prometheus/                # Monitoring configs
├── .github/                       # CI/CD workflows
│   └── workflows/
│       ├── ci.yml                 # CI pipeline
│       └── cd.yml                 # CD pipeline
├── scripts/                       # Utility scripts
│   ├── download_data.py           # Data download script
│   ├── smoke_test.sh              # Post-deployment tests
│   └── setup.sh                   # Environment setup
├── .dvc/                          # DVC configuration
├── .gitignore
├── .dockerignore
├── Dockerfile
├── requirements.txt               # Python dependencies
├── requirements-dev.txt           # Development dependencies
├── dvc.yaml                       # DVC pipeline
└── README.md
```

## Setup Instructions

### 1. Prerequisites
- Python 3.9+
- Docker & Docker Compose
- Git
- DVC (Data Version Control)

### 2. Environment Setup
```bash
# Clone the repository
git clone <repository-url>
cd mlops-cats-dogs

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Initialize DVC
dvc init
```

### 3. Download and Prepare Data
```bash
# Download the Cats and Dogs dataset from Kaggle
# Place it in data/raw/

# Run preprocessing
python src/data/preprocess.py
```

### 4. Train Model
```bash
# Train with MLflow tracking
python src/models/train.py --epochs 20 --batch_size 32
```

### 5. Run Inference Service Locally
```bash
# Start the FastAPI service
uvicorn src.inference.app:app --host 0.0.0.0 --port 8000
```

### 6. Build Docker Image
```bash
docker build -t cats-dogs-classifier:latest .
docker run -p 8000:8000 cats-dogs-classifier:latest
```

### 7. Test the API
```bash
# Health check
curl http://localhost:8000/health

# Prediction
curl -X POST http://localhost:8000/predict \
  -F "file=@path/to/image.jpg"
```

## CI/CD Pipeline

### Continuous Integration (CI)
GitHub Actions workflow triggered on every push/PR to main:
1. Checkout code
2. Install dependencies
3. Run linting (flake8)
4. Run unit tests (pytest with coverage)
5. Build Docker image
6. Test Docker image (health check)
7. Push image to Docker Hub (main branch only)

### Continuous Deployment (CD)
GitHub Actions workflow triggered after successful CI on main branch:
1. Pull latest Docker image from registry
2. Deploy using Docker Compose
3. Run smoke tests (health endpoint + prediction test)
4. Rollback on failure

**Setup Required:**
- Add `DOCKER_USERNAME` and `DOCKER_PASSWORD` to GitHub Secrets
- Configure self-hosted runner or deployment server

## Deployment

### Local Deployment with Docker
```bash
# Build and run single container
docker build -t cats-dogs-classifier:latest .
docker run -p 8000:8000 cats-dogs-classifier:latest
```

### Docker Compose (Recommended)
```bash
# Start all services (API + MLflow + Prometheus + Grafana)
cd deployment
docker-compose up -d

# Start only the classifier service
docker-compose up -d cats-dogs-classifier

# View logs
docker-compose logs -f cats-dogs-classifier

# Stop services
docker-compose down
```

## Monitoring

### View MLflow Experiments
```bash
mlflow ui
# Access at http://localhost:5000
```

### View Application Logs
```bash
# Docker single container
docker logs <container-id>

# Docker Compose
docker-compose -f deployment/docker-compose.yml logs -f cats-dogs-classifier
```

### Metrics
- Request count and latency tracked in application logs
- Model performance metrics in MLflow

## Testing
```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=src --cov-report=html
```

## Model Performance
- **Architecture**: Custom CNN with 4 convolutional blocks (~50M parameters)
- **Input**: 224x224 RGB images
- **Output**: Binary classification (Cat/Dog)
- **Metrics**: Accuracy, Precision, Recall, F1-Score
- **Expected Performance**: >90% accuracy on test set
- **Inference Time**: ~50-200ms (CPU), ~10-30ms (GPU)

## Tech Stack
- **ML Framework**: PyTorch 2.0+
- **Experiment Tracking**: MLflow 2.8+
- **Data Versioning**: DVC 3.30+
- **API Framework**: FastAPI 0.104+
- **Containerization**: Docker (multi-stage builds)
- **Orchestration**: Kubernetes 1.25+
- **CI/CD**: GitHub Actions
- **Testing**: Pytest with >80% coverage
- **Monitoring**: Prometheus + Grafana

## 📚 Documentation

### Quick Links
- **[🚀 Deployment Checklist](DEPLOYMENT_CHECKLIST.md)** - Step-by-step deployment guide
- **[✅ Production Readiness Report](PRODUCTION_READINESS_REPORT.md)** - Complete production assessment
- **[📖 Quick Start Guide](docs/QUICKSTART.md)** - Get started in 10 minutes
- **[🔧 API Documentation](docs/API.md)** - Complete API reference
- **[🐳 Deployment Guide](docs/DEPLOYMENT.md)** - Docker, K8s, Docker Compose
- **[💻 Windows Setup](docs/WINDOWS_SETUP.md)** - Windows-specific instructions
- **[📝 Quick Reference](QUICK_REFERENCE.md)** - Command cheat sheet
- **[🔍 Validation Report](VALIDATION_REPORT.md)** - Validation findings and fixes

## 🎯 Key Features

### Production-Grade Components
✅ **Comprehensive Error Handling** - All edge cases covered  
✅ **Health Checks** - Kubernetes liveness/readiness probes  
✅ **Structured Logging** - JSON logs for request tracking  
✅ **Metrics & Monitoring** - Prometheus integration  
✅ **Zero-Downtime Deployment** - Rolling updates configured  
✅ **Auto-Scaling Ready** - Resource limits and HPA support  
✅ **Security Hardened** - No secrets in code, input validation  
✅ **Fully Tested** - 20 unit tests with coverage reporting  
✅ **CI/CD Automated** - From commit to deployment  

## 🚀 Quick Start

### Option 1: Docker Compose (Recommended for Testing)
```bash
# 1. Update docker-compose.yml with your Docker username
export DOCKER_USERNAME=yourusername

# 2. Start all services
docker-compose up -d

# 3. Access services
# API: http://localhost:8000
# MLflow: http://localhost:5000
# Prometheus: http://localhost:9090
# Grafana: http://localhost:3000
```

### Option 2: Kubernetes (Production)
```bash
# 1. Update deployment.yaml with your Docker username
# 2. Apply configurations
kubectl apply -f deployment/kubernetes/deployment.yaml
kubectl apply -f deployment/kubernetes/service.yaml

# 3. Verify deployment
kubectl get pods -l app=cats-dogs-classifier
```

### Option 3: Local Development
```bash
# 1. Setup environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# 2. Download and process data
python scripts/download_data.py
python src/data/preprocess.py

# 3. Train model
python src/models/train.py --epochs 20

# 4. Start API
uvicorn src.inference.app:app --host 0.0.0.0 --port 8000
```

## Contributing
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests: `pytest tests/ -v --cov=src`
5. Submit a pull request

## License
MIT License

## Contact
For questions or issues, please open a GitHub issue.

# mlops-cats-dogs-assignment
