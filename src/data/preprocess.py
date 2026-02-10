"""
Data preprocessing utilities
- Class-safe splitting (per class)
- ImageFolder compatible output
- Deterministic and reproducible
"""

import random
from pathlib import Path
from typing import Tuple, List
from PIL import Image
import numpy as np
from tqdm import tqdm
import sys

sys.path.append(str(Path(__file__).parent.parent.parent))

from src.utils.config import (
    RAW_DATA_DIR,
    PROCESSED_DATA_DIR,
    TRAIN_DIR,
    VAL_DIR,
    TEST_DIR,
    IMG_SIZE,
    TRAIN_RATIO,
    VAL_RATIO,
    TEST_RATIO,
)

# -----------------------------
# Utility functions
# -----------------------------

def load_and_preprocess_image(
    image_path: Path,
    target_size: Tuple[int, int] = IMG_SIZE
) -> np.ndarray:
    """Load, resize, and normalize an image."""
    try:
        img = Image.open(image_path).convert("RGB")
        img = img.resize(target_size, Image.LANCZOS)
        return np.asarray(img, dtype=np.float32) / 255.0
    except Exception as e:
        print(f"Failed to process {image_path}: {e}")
        return None


def split_dataset(
    data_dir: Path,
    train_ratio: float = TRAIN_RATIO,
    val_ratio: float = VAL_RATIO,
    test_ratio: float = TEST_RATIO,
    seed: int = 42,
) -> Tuple[List[Path], List[Path], List[Path]]:
    """
    Split dataset directory into train/val/test file lists.
    """
    assert abs(train_ratio + val_ratio + test_ratio - 1.0) < 1e-6

    files = get_image_files(data_dir)

    random.seed(seed)
    random.shuffle(files)

    n = len(files)
    train_end = int(n * train_ratio)
    val_end = train_end + int(n * val_ratio)

    train_files = files[:train_end]
    val_files = files[train_end:val_end]
    test_files = files[val_end:]

    return train_files, val_files, test_files



def get_image_files(directory: Path) -> List[Path]:
    """Collect valid image files."""
    exts = {".jpg", ".jpeg", ".png", ".bmp"}
    return [f for f in directory.iterdir() if f.is_file() and f.suffix.lower() in exts]


def save_images(
    files: List[Path],
    dest_dir: Path,
    class_name: str,
):
    """Preprocess and save images into class folders."""
    class_dir = dest_dir / class_name
    class_dir.mkdir(parents=True, exist_ok=True)

    for file_path in tqdm(files, desc=f"{dest_dir.name}/{class_name}"):
        img_array = load_and_preprocess_image(file_path)
        if img_array is None:
            continue

        img = Image.fromarray((img_array * 255).astype(np.uint8))
        img.save(class_dir / file_path.name, format="JPEG", quality=95)


# -----------------------------
# Main preprocessing pipeline
# -----------------------------

def preprocess_dataset():
    print("🚀 Starting dataset preprocessing...")

    if not RAW_DATA_DIR.exists():
        raise FileNotFoundError(f"Raw data directory not found: {RAW_DATA_DIR}")

    class_map = {
        "cat": RAW_DATA_DIR / "cat",
        "dog": RAW_DATA_DIR / "dog",
    }

    # Clean old processed data (idempotent runs)
    for split_dir in [TRAIN_DIR, VAL_DIR, TEST_DIR]:
        if split_dir.exists():
            for item in split_dir.iterdir():
                if item.is_dir():
                    for f in item.iterdir():
                        f.unlink()
                    item.rmdir()

    stats = {}

    for class_name, class_dir in class_map.items():
        if not class_dir.exists():
            raise FileNotFoundError(f"Expected directory not found: {class_dir}")

        files = get_image_files(class_dir)
        train_f, val_f, test_f = split_files(
            files,
            TRAIN_RATIO,
            VAL_RATIO,
            TEST_RATIO,
        )

        stats[class_name] = {
            "train": len(train_f),
            "val": len(val_f),
            "test": len(test_f),
        }

        save_images(train_f, TRAIN_DIR, class_name)
        save_images(val_f, VAL_DIR, class_name)
        save_images(test_f, TEST_DIR, class_name)

    # -----------------------------
    # Sanity checks
    # -----------------------------
    print("\n📊 Final dataset distribution:")
    for split_dir in [TRAIN_DIR, VAL_DIR, TEST_DIR]:
        print(f"\n{split_dir.name}:")
        for cls in ["cat", "dog"]:
            cls_dir = split_dir / cls
            count = len(list(cls_dir.glob("*"))) if cls_dir.exists() else 0
            print(f"  {cls}: {count}")
            assert count > 0, f"{split_dir.name}/{cls} is empty!"

    print("\n✅ Dataset preprocessing completed successfully!")
    print(f"Processed data saved to: {PROCESSED_DATA_DIR}")


if __name__ == "__main__":
    preprocess_dataset()
