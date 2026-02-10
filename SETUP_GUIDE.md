# Quick Setup Guide

## Prerequisites
- Python 3.9+
- Docker & Docker Compose installed
- Git installed
- GitHub account
- Docker Hub account

## Initial Setup

### 1. Configure GitHub Secrets
Before pushing to GitHub, add these secrets to your repository:
1. Go to your GitHub repository
2. Navigate to Settings → Secrets and variables → Actions
3. Add the following secrets:
   - `DOCKER_USERNAME`: Your Docker Hub username
   - `DOCKER_PASSWORD`: Your Docker Hub password or access token

### 2. Local Development Setup

```bash
# Clone repository
git clone <your-repo-url>
cd mlops-cats-dogs

# Create virtual environment (Windows)
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Download dataset (place Kaggle dataset in data/raw/)
# Or run: python scripts/download_data.py

# Preprocess data
python src/data/preprocess.py
```

### 3. Train Model (Optional - model already included)

```bash
# Train model with MLflow tracking
python src/models/train.py --epochs 20 --batch_size 32

# View experiments
mlflow ui
# Access at http://localhost:5000
```

### 4. Test Locally

```bash
# Run unit tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=src --cov-report=term
```

### 5. Run Inference Service Locally

```bash
# Start FastAPI service
uvicorn src.inference.app:app --host 0.0.0.0 --port 8000

# In another terminal, test the API
curl http://localhost:8000/health

# Test prediction
curl -X POST "http://localhost:8000/predict" -F "file=@path/to/image.jpg"

# Or visit http://localhost:8000/docs for interactive API docs
```

### 6. Docker Deployment

#### Option A: Single Container
```bash
# Build image
docker build -t cats-dogs-classifier:latest .

# Run container
docker run -p 8000:8000 cats-dogs-classifier:latest

# Test
curl http://localhost:8000/health
```

#### Option B: Docker Compose (Recommended)
```bash
# Start all services
cd deployment
docker-compose up -d

# View logs
docker-compose logs -f cats-dogs-classifier

# Test smoke tests
bash ../scripts/smoke_test.sh http://localhost:8000

# Stop services
docker-compose down
```

### 7. CI/CD Pipeline

Once you push to GitHub with secrets configured:

1. **CI Pipeline** (`.github/workflows/ci.yml`):
   - Triggered on push/PR to main or develop
   - Runs tests, builds Docker image
   - Pushes to Docker Hub (main branch only)

2. **CD Pipeline** (`.github/workflows/cd.yml`):
   - Triggered after successful CI on main branch
   - Pulls latest image and deploys
   - Runs smoke tests
   - Rolls back on failure

## Testing the Complete Pipeline

```bash
# 1. Make a change
echo "# Test change" >> README.md

# 2. Commit and push
git add .
git commit -m "Test CI/CD pipeline"
git push origin main

# 3. Watch GitHub Actions
# Go to your repository → Actions tab
# Monitor CI and CD workflows

# 4. Verify deployment
curl http://<your-deployment-server>:8000/health
```

## Available Endpoints

- `GET /` - Root endpoint with API info
- `GET /health` - Health check
- `GET /docs` - Interactive API documentation (Swagger UI)
- `GET /metrics` - Prometheus metrics
- `POST /predict` - Image classification (accepts multipart/form-data)

## Docker Compose Services

When using `docker-compose up -d`, the following services are available:

| Service | Port | Description |
|---------|------|-------------|
| cats-dogs-classifier | 8000 | Main inference API |
| mlflow | 5001 | MLflow tracking UI |
| prometheus | 9090 | Metrics collection |
| grafana | 3000 | Monitoring dashboards (admin/admin) |

## Troubleshooting

### Tests Failing
```bash
# Check Python version
python --version  # Should be 3.9+

# Reinstall dependencies
pip install -r requirements.txt -r requirements-dev.txt --force-reinstall
```

### Docker Build Fails
```bash
# Clean Docker cache
docker system prune -a

# Rebuild without cache
docker build --no-cache -t cats-dogs-classifier:latest .
```

### Port Already in Use
```bash
# Windows - Find process using port 8000
netstat -ano | findstr :8000

# Kill process (replace PID)
taskkill /PID <PID> /F

# Or change port in docker run command
docker run -p 8080:8000 cats-dogs-classifier:latest
```

### GitHub Actions Failing
1. Check secrets are set correctly (DOCKER_USERNAME, DOCKER_PASSWORD)
2. Verify Docker Hub credentials
3. Check GitHub Actions logs for specific errors
4. Ensure model file exists in `models/` directory

## Project Structure Overview

```
mlops-cats-dogs/
├── .github/workflows/       # CI/CD pipelines
├── src/                     # Source code
│   ├── data/               # Data processing
│   ├── models/             # Model architecture & training
│   ├── inference/          # FastAPI service
│   └── utils/              # Utilities & config
├── tests/                   # Unit tests
├── deployment/              # Docker Compose configs
├── scripts/                 # Helper scripts
├── models/                  # Trained models (gitignored)
├── Dockerfile              # Container definition
├── requirements.txt        # Python dependencies
└── dvc.yaml                # DVC pipeline
```

## Next Steps

1. ✅ Verify all tests pass locally
2. ✅ Configure GitHub secrets
3. ✅ Push to GitHub and verify CI/CD runs
4. ✅ Test deployed service
5. ✅ Monitor logs and metrics
6. 📝 Document any custom modifications

## Support

- Check [README.md](README.md) for detailed documentation
- Review [ASSIGNMENT_CHECKLIST.md](ASSIGNMENT_CHECKLIST.md) for requirement validation
- API documentation: `http://localhost:8000/docs`
