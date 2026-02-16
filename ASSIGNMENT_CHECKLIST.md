# MLOps Assignment Checklist

## Use Case: Binary Image Classification (Cats vs Dogs)
**Platform:** Pet Adoption Platform  
**Dataset:** Kaggle Cats and Dogs Classification Dataset

---

## M1: Model Development & Experiment Tracking ✅

### 1.1 Data & Code Versioning ✅
| Requirement | Status | Implementation |
|-------------|--------|----------------|
| Git for source code | ✅ | Full Git repository with proper `.gitignore` |
| DVC for dataset versioning | ✅ | `dvc.yaml` defines data pipeline stages |
| DVC for model files | ✅ | Models stored in Google Drive via DVC |

**Files:**
- [dvc.yaml](dvc.yaml) - DVC pipeline definition
- [.dvc/config](.dvc/config) - DVC remote configuration (Google Drive)
- [.gitignore](.gitignore) - Excludes data and build artifacts

### 1.2 Model Building ✅
| Requirement | Status | Implementation |
|-------------|--------|----------------|
| Baseline CNN model | ✅ | Custom 4-block CNN in `src/models/cnn_model.py` |
| Image preprocessing to 224x224 RGB | ✅ | `src/data/preprocess.py` |
| Train/Val/Test split (80/10/10) | ✅ | `src/data/preprocess.py` with configurable ratios |
| Data augmentation | ✅ | `src/data/augmentation.py` (flip, rotation, color jitter) |
| Model saved in standard format | ✅ | PyTorch `.pt` format in `models/` |

**Files:**
- [src/models/cnn_model.py](src/models/cnn_model.py) - CNN architecture (26M parameters)
- [src/models/train.py](src/models/train.py) - Training script with MLflow
- [src/data/preprocess.py](src/data/preprocess.py) - Data preprocessing pipeline
- [src/data/augmentation.py](src/data/augmentation.py) - Data augmentation transforms

**Model Architecture:**
```
Input: 224x224x3 RGB Image
├── Conv Block 1: 32 filters → BatchNorm → ReLU → MaxPool
├── Conv Block 2: 64 filters → BatchNorm → ReLU → MaxPool
├── Conv Block 3: 128 filters → BatchNorm → ReLU → MaxPool
├── Conv Block 4: 256 filters → BatchNorm → ReLU → MaxPool
├── Flatten
├── FC1: 512 units → Dropout
├── FC2: 128 units → Dropout
└── Output: 2 classes (cat, dog)
```

### 1.3 Experiment Tracking ✅
| Requirement | Status | Implementation |
|-------------|--------|----------------|
| MLflow for experiment tracking | ✅ | Integrated in `train.py` |
| Log parameters | ✅ | batch_size, epochs, lr, dropout |
| Log metrics | ✅ | train/val loss, accuracy per epoch |
| Log artifacts | ✅ | Confusion matrix, training curves, model |

**Usage:**
```bash
# Start MLflow UI
mlflow ui --port 5000

# Train with tracking
python src/models/train.py --epochs 20 --batch_size 32
```

---

## M2: Model Packaging & Containerization ✅

### 2.1 Inference Service ✅
| Requirement | Status | Implementation |
|-------------|--------|----------------|
| REST API with FastAPI | ✅ | `src/inference/app.py` |
| Health check endpoint | ✅ | `GET /health` |
| Prediction endpoint | ✅ | `POST /predict` (multipart image) |
| Returns class probabilities | ✅ | JSON with class labels and probabilities |

**API Endpoints:**
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Root - API info |
| `/health` | GET | Health check (for load balancers) |
| `/predict` | POST | Image classification |
| `/metrics` | GET | Prometheus metrics |
| `/metrics/json` | GET | JSON format metrics |
| `/model-info` | GET | Model information |
| `/docs` | GET | Swagger UI documentation |

**Files:**
- [src/inference/app.py](src/inference/app.py) - FastAPI application
- [src/inference/predictor.py](src/inference/predictor.py) - Prediction logic

### 2.2 Environment Specification ✅
| Requirement | Status | Implementation |
|-------------|--------|----------------|
| requirements.txt | ✅ | Production dependencies |
| requirements-dev.txt | ✅ | Development/testing dependencies |
| Version pinning | ✅ | Major versions pinned for ML libraries |

**Files:**
- [requirements.txt](requirements.txt) - PyTorch, FastAPI, MLflow, etc.
- [requirements-dev.txt](requirements-dev.txt) - pytest, flake8, DVC

### 2.3 Containerization ✅
| Requirement | Status | Implementation |
|-------------|--------|----------------|
| Dockerfile | ✅ | Multi-stage build for optimization |
| Build and run locally | ✅ | `docker build` + `docker run` |
| Predictions via curl/Postman | ✅ | Verified endpoints work |

**Dockerfile Features:**
- Multi-stage build (builder + runtime)
- Non-root user for security
- Health check built-in
- Optimized layer caching

**Commands:**
```bash
# Build image
docker build -t cats-dogs-classifier:latest .

# Run container
docker run -p 8000:8000 cats-dogs-classifier:latest

# Test prediction
curl -X POST http://localhost:8000/predict -F "file=@image.jpg"
```

---

## M3: CI Pipeline for Build, Test & Image Creation ✅

### 3.1 Automated Testing ✅
| Requirement | Status | Implementation |
|-------------|--------|----------------|
| Unit tests for preprocessing | ✅ | `tests/test_preprocess.py` |
| Unit tests for inference | ✅ | `tests/test_inference.py` |
| Tests run via pytest | ✅ | `pytest.ini` configured |

**Test Coverage:**
- `test_preprocess.py`: Image loading, normalization, dataset splitting
- `test_inference.py`: Model architecture, predictor, batch prediction

**Run Tests:**
```bash
pytest tests/ -v --cov=src
```

### 3.2 CI Setup (GitHub Actions) ✅
| Requirement | Status | Implementation |
|-------------|--------|----------------|
| Trigger on push/PR | ✅ | `on: push/pull_request` to main |
| Checkout repository | ✅ | `actions/checkout@v4` with LFS |
| Install dependencies | ✅ | `pip install -r requirements.txt` |
| Run unit tests | ✅ | `pytest tests/` |
| Build Docker image | ✅ | `docker/build-push-action@v5` |

**Files:**
- [.github/workflows/ci.yml](.github/workflows/ci.yml) - Main CI/CD pipeline

**CI Pipeline Stages:**
1. Checkout code (with Git LFS)
2. Setup Python 3.9
3. Install dependencies
4. Lint with flake8
5. Run pytest
6. Build Docker image
7. Push to Docker Hub (main branch only)

### 3.3 Artifact Publishing ✅
| Requirement | Status | Implementation |
|-------------|--------|----------------|
| Push to container registry | ✅ | Docker Hub via GitHub Actions |
| Tagged images | ✅ | `latest` + commit SHA |

**Docker Hub Image:**
```
<DOCKER_USERNAME>/cats-dogs-classifier:latest
<DOCKER_USERNAME>/cats-dogs-classifier:<commit-sha>
```

---

## M4: CD Pipeline & Deployment ✅

### 4.1 Deployment Target (Docker Compose) ✅
| Requirement | Status | Implementation |
|-------------|--------|----------------|
| Docker Compose deployment | ✅ | `deployment/docker-compose.yml` |
| Infrastructure manifests | ✅ | Services defined with health checks |

**Docker Compose Services:**
| Service | Port | Description |
|---------|------|-------------|
| cats-dogs-classifier | 8000 | Main inference API |
| prometheus | 9090 | Metrics collection & UI |

**Files:**
- [deployment/docker-compose.yml](deployment/docker-compose.yml)
- [deployment/prometheus/prometheus.yml](deployment/prometheus/prometheus.yml)

### 4.2 CD / GitOps Flow ✅
| Requirement | Status | Implementation |
|-------------|--------|----------------|
| Pull new image from registry | ✅ | `docker pull` in workflow |
| Auto-deploy on main branch | ✅ | CD runs after successful CI |
| Update running service | ✅ | `docker-compose up -d --pull always` |

**Files:**
- [.github/workflows/ci.yml](.github/workflows/ci.yml) - Combined CI/CD
- [.github/workflows/cd.yml](.github/workflows/cd.yml) - Manual deploy

**Deployment Flow:**
1. CI completes successfully on main
2. CD job pulls latest image
3. Stops existing containers
4. Starts new containers
5. Waits for health check
6. Runs smoke tests

### 4.3 Smoke Tests / Health Check ✅
| Requirement | Status | Implementation |
|-------------|--------|----------------|
| Post-deploy smoke test | ✅ | `scripts/smoke_test.sh` |
| Health endpoint check | ✅ | `curl /health` |
| Prediction test | ✅ | Creates test image, calls `/predict` |
| Pipeline fails on test failure | ✅ | Exit code 1 on failure |

**Smoke Tests:**
1. Health check endpoint
2. Root endpoint
3. Metrics endpoint
4. Model info endpoint
5. Prediction endpoint (with generated image)

---

## M5: Monitoring, Logs & Final Submission ✅

### 5.1 Basic Monitoring & Logging ✅
| Requirement | Status | Implementation |
|-------------|--------|----------------|
| Request/response logging | ✅ | Python logging in `app.py` |
| Request count metric | ✅ | Prometheus Counter |
| Latency metric | ✅ | Prometheus Histogram |
| Exclude sensitive data | ✅ | Only metadata logged |

**Prometheus Metrics:**
| Metric | Type | Labels |
|--------|------|--------|
| `cats_dogs_requests_total` | Counter | status (success/error) |
| `cats_dogs_inference_seconds` | Histogram | - |
| `cats_dogs_predictions_total` | Counter | predicted_class |
| `cats_dogs_model_loaded` | Gauge | - |

**Prometheus Configuration:**
- Scrape interval: 15 seconds
- Target: `cats-dogs-classifier:8000/metrics`

### 5.2 Model Performance Tracking ✅
| Requirement | Status | Implementation |
|-------------|--------|----------------|
| Collect prediction requests | ✅ | Logged with timestamps |
| Track predictions by class | ✅ | Counter per class |
| Inference time distribution | ✅ | Histogram buckets |

**Example Prometheus Queries:**
```promql
# Request rate
rate(cats_dogs_requests_total[5m])

# Average inference time
rate(cats_dogs_inference_seconds_sum[5m]) / rate(cats_dogs_inference_seconds_count[5m])

# Predictions by class
sum by (predicted_class) (cats_dogs_predictions_total)
```

---

## Quick Start Commands

### Local Development
```bash
# Install dependencies
pip install -r requirements.txt -r requirements-dev.txt

# Create test model
python scripts/create_test_model.py

# Run tests
pytest tests/ -v

# Start API
uvicorn src.inference.app:app --host 0.0.0.0 --port 8000
```

### Docker Deployment
```bash
# Build and run with Docker Compose
cd deployment
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f cats-dogs-classifier

# Run smoke tests
bash ../scripts/smoke_test.sh http://localhost:8000

# Access Prometheus
# http://localhost:9090
```

### CI/CD Setup
1. Add GitHub secrets: `DOCKER_USERNAME`, `DOCKER_PASSWORD`
2. Push to main branch
3. Monitor Actions tab
4. Verify deployment

---

## Project Files Summary

| Category | Files |
|----------|-------|
| **Source Code** | `src/data/`, `src/models/`, `src/inference/`, `src/utils/` |
| **Tests** | `tests/test_preprocess.py`, `tests/test_inference.py` |
| **Configuration** | `requirements.txt`, `pytest.ini`, `dvc.yaml` |
| **Docker** | `Dockerfile`, `deployment/docker-compose.yml` |
| **CI/CD** | `.github/workflows/ci.yml`, `.github/workflows/cd.yml` |
| **Monitoring** | `deployment/prometheus/prometheus.yml` |
| **Scripts** | `scripts/download_data.py`, `scripts/smoke_test.sh`, `scripts/create_test_model.py` |
| **Documentation** | `README.md`, `SETUP_GUIDE.md`, `GITHUB_SETUP.md` |

---

## Verification Checklist

- [x] **M1:** Model trained and tracked with MLflow
- [x] **M1:** Data versioned with DVC
- [x] **M1:** Code versioned with Git
- [x] **M2:** FastAPI inference service created
- [x] **M2:** Health and predict endpoints working
- [x] **M2:** Dockerfile builds successfully
- [x] **M3:** Unit tests pass with pytest
- [x] **M3:** CI pipeline runs on push
- [x] **M3:** Docker image pushed to registry
- [x] **M4:** Docker Compose deployment works
- [x] **M4:** CD auto-deploys on main branch
- [x] **M4:** Smoke tests validate deployment
- [x] **M5:** Prometheus metrics exposed
- [x] **M5:** Logging enabled for requests
- [x] **M5:** Monitoring dashboard accessible



