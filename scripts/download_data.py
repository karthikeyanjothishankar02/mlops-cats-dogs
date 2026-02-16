"""
Script to download Cats and Dogs dataset from Kaggle
"""

import os
import sys
import zipfile
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from src.utils.config import RAW_DATA_DIR  # noqa: E402


def download_dataset():
    """
    Download the Cats and Dogs dataset

    Note: This requires Kaggle API credentials to be set up.
    Visit: https://www.kaggle.com/docs/api
    """
    print("=" * 60)
    print("Cats and Dogs Dataset Download")
    print("=" * 60)

    # Check if kaggle is installed
    try:
        import kaggle  # noqa: F401
    except ImportError:
        print("\n⚠ Kaggle API not installed!")
        print("Install it with: pip install kaggle")
        print("\nThen set up your Kaggle API credentials:")
        print("1. Go to https://www.kaggle.com/account")
        print("2. Create New API Token")
        print(
            "3. Place kaggle.json in ~/.kaggle/ (Linux/Mac) "
            "or C:\\Users\\<Username>\\.kaggle\\ (Windows)"
        )
        sys.exit(1)

    # Create raw data directory
    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)

    # Download dataset
    print("\n📥 Downloading dataset from Kaggle...")
    print("Dataset: dogs-vs-cats (Microsoft)")

    try:
        # Option 1: Using Kaggle API for the classic Dogs vs Cats competition
        os.system(f"kaggle competitions download -c dogs-vs-cats -p {RAW_DATA_DIR}")

        # Unzip the dataset
        print("\n📦 Extracting dataset...")
        zip_files = list(RAW_DATA_DIR.glob("*.zip"))

        for zip_file in zip_files:
            print(f"Extracting {zip_file.name}...")
            with zipfile.ZipFile(zip_file, "r") as zip_ref:
                zip_ref.extractall(RAW_DATA_DIR)

            # Remove zip file after extraction
            zip_file.unlink()

        # Further extract train.zip if it exists
        train_zip = RAW_DATA_DIR / "train.zip"
        if train_zip.exists():
            with zipfile.ZipFile(train_zip, "r") as zip_ref:
                zip_ref.extractall(RAW_DATA_DIR)
            train_zip.unlink()

        print("\n✓ Dataset downloaded and extracted successfully!")
        print(f"Location: {RAW_DATA_DIR}")

        # Count files
        image_files = list(RAW_DATA_DIR.glob("**/*.jpg")) + list(
            RAW_DATA_DIR.glob("**/*.jpeg")
        )
        print(f"Total images: {len(image_files)}")

    except Exception as e:
        print(f"\n✗ Error downloading dataset: {e}")
        print("\n📝 Manual Download Instructions:")
        print("1. Visit: https://www.kaggle.com/c/dogs-vs-cats/data")
        print("2. Download train.zip")
        print(f"3. Extract to: {RAW_DATA_DIR}")
        print("\nAlternatively, use a smaller dataset:")
        print("https://www.kaggle.com/datasets/tongpython/cat-and-dog")


if __name__ == "__main__":
    download_dataset()



