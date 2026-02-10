#!/bin/bash

# Environment setup script
# Usage: ./setup.sh

echo "=================================="
echo "MLOps Environment Setup"
echo "=================================="
echo ""

# Check Python version
echo "Checking Python version..."
PYTHON_VERSION=$(python --version 2>&1 | awk '{print $2}')
echo "Python version: $PYTHON_VERSION"
echo ""

# Create virtual environment
echo "Creating virtual environment..."
python -m venv venv
echo "✓ Virtual environment created"
echo ""

# Activate virtual environment
echo "Activating virtual environment..."
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi
echo "✓ Virtual environment activated"
echo ""

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip
echo ""

# Install requirements
echo "Installing requirements..."
pip install -r requirements.txt
echo "✓ Core requirements installed"
echo ""

echo "Installing development requirements..."
pip install -r requirements-dev.txt
echo "✓ Development requirements installed"
echo ""

# Initialize DVC
echo "Initializing DVC..."
dvc init
echo "✓ DVC initialized"
echo ""

# Initialize Git (if not already initialized)
if [ ! -d ".git" ]; then
    echo "Initializing Git repository..."
    git init
    echo "✓ Git initialized"
    echo ""
fi

# Create necessary directories
echo "Creating project directories..."
mkdir -p data/raw
mkdir -p data/processed
mkdir -p models
mkdir -p logs
mkdir -p mlruns
echo "✓ Directories created"
echo ""

# Set up pre-commit hooks (optional)
echo "Setting up pre-commit hooks..."
pip install pre-commit
cat > .pre-commit-config.yaml <<EOL
repos:
  - repo: https://github.com/psf/black
    rev: 23.9.1
    hooks:
      - id: black
        language_version: python3.9

  - repo: https://github.com/pycqa/isort
    rev: 5.12.0
    hooks:
      - id: isort

  - repo: https://github.com/pycqa/flake8
    rev: 6.1.0
    hooks:
      - id: flake8
        args: [--max-line-length=127]
EOL
pre-commit install
echo "✓ Pre-commit hooks installed"
echo ""

echo "=================================="
echo "✓ Setup complete!"
echo "=================================="
echo ""
echo "Next steps:"
echo "1. Download dataset: python scripts/download_data.py"
echo "2. Preprocess data: python src/data/preprocess.py"
echo "3. Train model: python src/models/train.py"
echo "4. Run tests: pytest tests/"
echo "5. Start API: uvicorn src.inference.app:app --reload"
echo ""
