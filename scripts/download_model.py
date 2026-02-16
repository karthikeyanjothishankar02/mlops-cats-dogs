"""
Download model from Google Drive (bypassing DVC)

This script downloads the trained model directly from a public Google Drive folder.
"""

import os
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Google Drive folder ID containing the model
GDRIVE_FOLDER_ID = os.getenv("GDRIVE_FOLDER_ID", "1knSkL_LDsuWTXAIcv6UfdxhuXMUXbC65")

# Model filename to download
MODEL_FILENAME = "best_model.pt"

# Destination directory
MODELS_DIR = Path(__file__).parent.parent / "models"


def download_model_from_gdrive(  # noqa: C901
    folder_id: str = None, filename: str = None, output_dir: Path = None
) -> Path:
    """
    Download model from Google Drive folder.

    Args:
        folder_id: Google Drive folder ID (uses GDRIVE_FOLDER_ID env var)
        filename: Name of the model file to download
        output_dir: Directory to save the model

    Returns:
        Path to the downloaded model file
    """
    try:
        import gdown
    except ImportError:
        print("Installing gdown...")
        import subprocess

        subprocess.check_call([sys.executable, "-m", "pip", "install", "gdown"])
        import gdown

    folder_id = folder_id or GDRIVE_FOLDER_ID
    filename = filename or MODEL_FILENAME
    output_dir = output_dir or MODELS_DIR

    # Ensure output directory exists
    output_dir.mkdir(parents=True, exist_ok=True)

    output_path = output_dir / filename

    # Check if model already exists
    if output_path.exists():
        print(f"Model already exists at {output_path}")
        return output_path

    print(f"Downloading model from Google Drive folder: {folder_id}")
    print(f"Looking for file: {filename}")

    # Download entire folder contents to find the model
    folder_url = f"https://drive.google.com/drive/folders/{folder_id}"

    try:
        # Try to download the specific file by searching the folder
        gdown.download_folder(
            url=folder_url, output=str(output_dir), quiet=False, use_cookies=False
        )

        if output_path.exists():
            print(f"Successfully downloaded model to {output_path}")
            return output_path
        else:
            # Check if model was downloaded with different name
            downloaded_files = list(output_dir.glob("*.pt"))
            if downloaded_files:
                # Rename first .pt file found to best_model.pt
                src = downloaded_files[0]
                if src.name != filename:
                    src.rename(output_path)
                    print(f"Renamed {src.name} to {filename}")
                return output_path

            raise FileNotFoundError(
                f"Model file {filename} not found in downloaded content"
            )

    except Exception as e:
        print(f"Error downloading from folder: {e}")
        print("Attempting direct file URL download...")

        # Fallback: try direct file download if FILE_ID is set
        file_id = os.getenv("GDRIVE_FILE_ID")
        if file_id:
            url = f"https://drive.google.com/uc?id={file_id}"
            gdown.download(url, str(output_path), quiet=False)
            if output_path.exists():
                print(f"Successfully downloaded model to {output_path}")
                return output_path

        raise


def ensure_model_exists() -> Path:
    """
    Ensure the model file exists, downloading if necessary.

    Returns:
        Path to the model file
    """
    model_path = MODELS_DIR / MODEL_FILENAME

    if model_path.exists():
        print(f"Model found at {model_path}")
        return model_path

    print("Model not found locally, downloading from Google Drive...")
    return download_model_from_gdrive()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Download model from Google Drive")
    parser.add_argument(
        "--folder-id",
        type=str,
        default=None,
        help="Google Drive folder ID (or set GDRIVE_FOLDER_ID env var)",
    )
    parser.add_argument(
        "--filename",
        type=str,
        default=MODEL_FILENAME,
        help="Model filename to download",
    )
    parser.add_argument(
        "--output-dir", type=str, default=None, help="Output directory for the model"
    )

    args = parser.parse_args()

    output_dir = Path(args.output_dir) if args.output_dir else MODELS_DIR

    try:
        model_path = download_model_from_gdrive(
            folder_id=args.folder_id, filename=args.filename, output_dir=output_dir
        )
        print(f"\nModel downloaded successfully: {model_path}")
    except Exception as e:
        print(f"\nError: {e}")
        sys.exit(1)



