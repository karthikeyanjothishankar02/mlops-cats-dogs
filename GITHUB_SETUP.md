# GitHub Setup Instructions

## Setting Up GitHub Secrets (Required for CI/CD)

Your CI/CD pipelines require Docker Hub credentials to push images. Follow these steps:

### Step 1: Get Docker Hub Credentials

1. Go to [Docker Hub](https://hub.docker.com/)
2. Sign in or create an account
3. Click on your username → Account Settings → Security
4. Click "New Access Token"
5. Name it "github-actions" and copy the token (you won't see it again!)

### Step 2: Add Secrets to GitHub Repository

1. Go to your GitHub repository
2. Click **Settings** (top right of repo page)
3. In the left sidebar, click **Secrets and variables** → **Actions**
4. Click **New repository secret**

Add these two secrets:

#### Secret 1: DOCKER_USERNAME
- Name: `DOCKER_USERNAME`
- Value: Your Docker Hub username (e.g., `johndoe`)
- Click **Add secret**

#### Secret 2: DOCKER_PASSWORD
- Name: `DOCKER_PASSWORD`
- Value: Your Docker Hub access token (from Step 1)
- Click **Add secret**

### Step 3: Verify Secrets

You should see both secrets listed (values are hidden):
```
DOCKER_USERNAME
DOCKER_PASSWORD
```

## Pushing Your Code to GitHub

### First Time Setup

```bash
# Initialize git (if not already done)
git init

# Add remote (replace with your repo URL)
git remote add origin https://github.com/your-username/mlops-cats-dogs.git

# Check current branch
git branch

# If not on 'main', rename branch
git branch -M main
```

### Commit and Push

```bash
# Check status
git status

# Add all files
git add .

# Commit changes
git commit -m "Add CI/CD pipelines and cleanup repository"

# Push to GitHub
git push -u origin main
```

## What Happens After Push

### 1. CI Pipeline Triggers (Automatic)
Once you push to `main` or `develop`, GitHub Actions will:
- ✓ Checkout your code
- ✓ Install Python dependencies
- ✓ Run linting (flake8)
- ✓ Run unit tests with coverage
- ✓ Build Docker image
- ✓ Test Docker image
- ✓ Push image to Docker Hub (main branch only)

**View Progress:**
1. Go to your repository on GitHub
2. Click **Actions** tab
3. See "CI Pipeline" workflow running

### 2. CD Pipeline Triggers (After CI Success)
If CI succeeds on `main` branch, CD will:
- ✓ Pull latest Docker image
- ✓ Deploy with Docker Compose
- ✓ Run smoke tests (health + prediction)
- ✓ Rollback if tests fail

## Troubleshooting

### "Error: Docker login failed"
**Cause:** GitHub secrets not configured or incorrect
**Solution:**
1. Verify secrets in Settings → Secrets and variables → Actions
2. Check DOCKER_USERNAME is your exact Docker Hub username
3. Regenerate Docker Hub access token if needed

### "Error: Cannot connect to Docker daemon"
**Cause:** Docker not available in GitHub Actions runner
**Solution:** This is expected if using standard GitHub runners. The workflow is configured correctly for GitHub-hosted runners.

### "Tests failed"
**Cause:** Unit tests not passing
**Solution:**
```bash
# Run tests locally first
pytest tests/ -v

# Fix any failing tests before pushing
```

### "Image push failed: denied"
**Cause:** Docker Hub repository doesn't exist or no permission
**Solution:**
1. Create repository on Docker Hub: `cats-dogs-classifier`
2. Make sure it's public or you have access
3. Verify your access token has push permissions

## Manual Testing Before Push

Always test locally before pushing:

```bash
# 1. Run tests
pytest tests/ -v --cov=src

# 2. Check linting
flake8 src/ tests/ --count --max-line-length=127

# 3. Build Docker
docker build -t cats-dogs-classifier:latest .

# 4. Run Docker
docker run -d -p 8000:8000 --name test cats-dogs-classifier:latest

# 5. Test endpoints
curl http://localhost:8000/health
curl -X POST http://localhost:8000/predict -F "file=@test_image.jpg"

# 6. Clean up
docker stop test && docker rm test
```

## Monitoring Your Pipeline

### GitHub Actions Dashboard
- **URL:** `https://github.com/your-username/mlops-cats-dogs/actions`
- **View:** All workflow runs, logs, and status
- **Filter:** By workflow, branch, or status

### CI Workflow Stages
1. ⚙️ Setup (checkout, Python, dependencies)
2. 🔍 Lint (flake8)
3. 🧪 Test (pytest + coverage)
4. 🐳 Docker (build + test)
5. 📦 Push (Docker Hub - main only)

### CD Workflow Stages
1. ⚙️ Setup (checkout, Docker login)
2. 📥 Pull (latest image)
3. 🚀 Deploy (docker-compose)
4. 🔬 Smoke Tests (health + predict)
5. ↩️ Rollback (if failed)

## Expected Timeline

| Action | Time |
|--------|------|
| git push | Instant |
| CI starts | ~10-30 seconds |
| CI completes | ~3-5 minutes |
| CD starts | ~10 seconds after CI |
| CD completes | ~1-2 minutes |
| **Total** | **~5-8 minutes** |

## Success Indicators

### CI Success ✅
- Green checkmark on commit
- Docker image in Docker Hub
- All tests passed
- Coverage report generated

### CD Success ✅
- Service deployed and running
- Health check passed
- Prediction test passed
- No rollback triggered

## Next Steps After Successful Pipeline

1. **Access Your Service:**
   ```bash
   curl http://<deployment-server>:8000/health
   ```

2. **View MLflow UI:**
   ```bash
   # If using docker-compose
   curl http://<deployment-server>:5001
   ```

3. **Monitor Metrics:**
   ```bash
   curl http://<deployment-server>:8000/metrics
   ```

4. **View Logs:**
   ```bash
   docker-compose -f deployment/docker-compose.yml logs -f
   ```

## Common Git Commands

```bash
# See what changed
git status

# Add specific files
git add filename.py

# Add all changes
git add .

# Commit with message
git commit -m "Your message here"

# Push to GitHub
git push origin main

# Pull latest changes
git pull origin main

# Create new branch
git checkout -b feature-branch

# Switch branches
git checkout main

# View commit history
git log --oneline

# Undo last commit (keep changes)
git reset --soft HEAD~1
```

## Getting Help

- **GitHub Actions Logs:** Check Actions tab for detailed error messages
- **Local Testing:** Always test locally first
- **Docker Hub:** Verify images are being pushed
- **Documentation:** 
  - [README.md](README.md) - Project overview
  - [ASSIGNMENT_CHECKLIST.md](ASSIGNMENT_CHECKLIST.md) - Requirements
  - [SETUP_GUIDE.md](SETUP_GUIDE.md) - Local setup
  - [SUMMARY.md](SUMMARY.md) - Changes made

---

**Remember:** Configure GitHub secrets BEFORE pushing, or CI/CD will fail!
