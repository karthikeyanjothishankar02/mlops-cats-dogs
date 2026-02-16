"""
Configuration settings for the MLOps Cats vs Dogs project
"""

import os
from pathlib import Path

# ========================================
# Path Configuration
# ========================================
# Project root directory
PROJECT_ROOT = Path(__file__).parent.parent.parent

# Data directories
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
TRAIN_DIR = PROCESSED_DATA_DIR / "train"
VAL_DIR = PROCESSED_DATA_DIR / "val"
TEST_DIR = PROCESSED_DATA_DIR / "test"

# Models directory
MODELS_DIR = PROJECT_ROOT / "models"

# Logs directory
LOGS_DIR = PROJECT_ROOT / "logs"

# ========================================
# Data Processing Configuration
# ========================================
# Image size (height, width) - standard for CNNs
IMG_SIZE = (224, 224)

# Dataset split ratios
TRAIN_RATIO = 0.8
VAL_RATIO = 0.1
TEST_RATIO = 0.1

# ========================================
# Model Configuration
# ========================================
# Number of output classes (cat, dog)
NUM_CLASSES = 2

# Class names
CLASS_NAMES = ["cat", "dog"]

# ========================================
# Training Configuration
# ========================================
# Training hyperparameters (defaults)
BATCH_SIZE = int(os.getenv("BATCH_SIZE", "32"))
EPOCHS = int(os.getenv("EPOCHS", "20"))
LEARNING_RATE = float(os.getenv("LEARNING_RATE", "0.001"))

# Early stopping
EARLY_STOPPING_PATIENCE = 5

# Random seed for reproducibility
RANDOM_SEED = 42

# ========================================
# MLflow Configuration
# ========================================
MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", "mlruns")
MLFLOW_EXPERIMENT_NAME = os.getenv("MLFLOW_EXPERIMENT_NAME", "cats-dogs-classifier")

# ========================================
# API Configuration
# ========================================
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", "8000"))
API_TITLE = "Cats vs Dogs Classifier API"
API_VERSION = "1.0.0"

# ========================================
# Logging Configuration
# ========================================
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# ========================================
# Docker Configuration
# ========================================
DOCKER_IMAGE_NAME = os.getenv("DOCKER_IMAGE_NAME", "cats-dogs-classifier")
DOCKER_REGISTRY = os.getenv("DOCKER_REGISTRY", "docker.io")


# ========================================
# Ensure directories exist
# ========================================
def create_directories():
    """Create necessary directories if they don't exist"""
    directories = [
        DATA_DIR,
        RAW_DATA_DIR,
        PROCESSED_DATA_DIR,
        TRAIN_DIR,
        VAL_DIR,
        TEST_DIR,
        MODELS_DIR,
        LOGS_DIR,
    ]
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)


# Create directories on module import (optional)
# Uncomment if you want directories created automatically
# create_directories()


if __name__ == "__main__":
    # Print configuration for debugging
    print("=" * 60)
    print("MLOps Cats vs Dogs Configuration")
    print("=" * 60)
    print(f"\nProject Root: {PROJECT_ROOT}")
    print(f"Data Directory: {DATA_DIR}")
    print(f"Models Directory: {MODELS_DIR}")
    print(f"\nImage Size: {IMG_SIZE}")
    print(f"Num Classes: {NUM_CLASSES}")
    print(f"Class Names: {CLASS_NAMES}")
    print(f"\nBatch Size: {BATCH_SIZE}")
    print(f"Epochs: {EPOCHS}")
    print(f"Learning Rate: {LEARNING_RATE}")
    print(f"\nMLflow Experiment: {MLFLOW_EXPERIMENT_NAME}")
    print(f"API Host: {API_HOST}:{API_PORT}")



