"""
Data preprocessing module for Cats vs Dogs classification

This module provides functions for:
- Loading and preprocessing images
- Splitting dataset into train/validation/test sets
- Processing raw Kaggle data into proper directory structure
"""
import os
import random
import shutil
from pathlib import Path
from typing import List, Optional, Tuple

import numpy as np
from PIL import Image
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
    RANDOM_SEED,
)


def load_and_preprocess_image(
    image_path: str,
    target_size: Tuple[int, int] = IMG_SIZE,
    normalize: bool = True
) -> Optional[np.ndarray]:
    """
    Load and preprocess a single image
    
    Args:
        image_path: Path to the image file
        target_size: Target size (height, width) for resizing
        normalize: Whether to normalize pixel values to [0, 1]
        
    Returns:
        Preprocessed image as numpy array, or None if loading fails
    """
    try:
        # Load image
        image = Image.open(image_path)
        
        # Convert to RGB if necessary
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Resize to target size
        image = image.resize((target_size[1], target_size[0]), Image.Resampling.LANCZOS)
        
        # Convert to numpy array
        img_array = np.array(image)
        
        # Normalize to [0, 1]
        if normalize:
            img_array = img_array.astype(np.float64) / 255.0
        
        return img_array
    
    except Exception as e:
        print(f"Error loading image {image_path}: {e}")
        return None


def split_dataset(
    source_dir: Path,
    train_ratio: float = TRAIN_RATIO,
    val_ratio: float = VAL_RATIO,
    test_ratio: float = TEST_RATIO,
    seed: int = RANDOM_SEED,
    extensions: Tuple[str, ...] = ('.jpg', '.jpeg', '.png', '.bmp')
) -> Tuple[List[Path], List[Path], List[Path]]:
    """
    Split dataset files into train/validation/test sets
    
    Args:
        source_dir: Directory containing image files
        train_ratio: Fraction of data for training
        val_ratio: Fraction of data for validation
        test_ratio: Fraction of data for testing
        seed: Random seed for reproducibility
        extensions: Tuple of valid file extensions
        
    Returns:
        Tuple of (train_files, val_files, test_files) lists
    """
    source_dir = Path(source_dir)
    
    # Get all image files
    all_files = []
    for ext in extensions:
        all_files.extend(list(source_dir.glob(f"*{ext}")))
        all_files.extend(list(source_dir.glob(f"*{ext.upper()}")))
    
    # Remove duplicates and sort for reproducibility
    all_files = sorted(list(set(all_files)))
    
    if len(all_files) == 0:
        print(f"Warning: No image files found in {source_dir}")
        return [], [], []
    
    # Set random seed for reproducibility
    random.seed(seed)
    
    # Shuffle files
    shuffled_files = all_files.copy()
    random.shuffle(shuffled_files)
    
    # Calculate split indices
    total = len(shuffled_files)
    train_end = int(total * train_ratio)
    val_end = train_end + int(total * val_ratio)
    
    # Split files
    train_files = shuffled_files[:train_end]
    val_files = shuffled_files[train_end:val_end]
    test_files = shuffled_files[val_end:]
    
    return train_files, val_files, test_files


def organize_kaggle_dataset(
    raw_dir: Path = RAW_DATA_DIR,
    processed_dir: Path = PROCESSED_DATA_DIR,
    train_ratio: float = TRAIN_RATIO,
    val_ratio: float = VAL_RATIO,
    test_ratio: float = TEST_RATIO,
    seed: int = RANDOM_SEED
) -> dict:
    """
    Organize the Kaggle Cats vs Dogs dataset into train/val/test splits
    
    The Kaggle dataset has format: cat.0.jpg, dog.0.jpg, etc.
    This function organizes them into:
    - processed/train/cat/
    - processed/train/dog/
    - processed/val/cat/
    - processed/val/dog/
    - processed/test/cat/
    - processed/test/dog/
    
    Args:
        raw_dir: Directory containing raw images
        processed_dir: Output directory for processed data
        train_ratio: Fraction for training
        val_ratio: Fraction for validation
        test_ratio: Fraction for testing
        seed: Random seed
        
    Returns:
        Dictionary with statistics about the processed data
    """
    raw_dir = Path(raw_dir)
    processed_dir = Path(processed_dir)
    
    print("=" * 60)
    print("Organizing Cats vs Dogs Dataset")
    print("=" * 60)
    
    # Find the train folder in raw data (Kaggle structure)
    train_folder = raw_dir / "train"
    if train_folder.exists():
        source_folder = train_folder
    else:
        source_folder = raw_dir
    
    print(f"Source folder: {source_folder}")
    
    # Get all cat and dog images
    all_images = list(source_folder.glob("*.jpg")) + list(source_folder.glob("*.jpeg"))
    
    cat_images = [f for f in all_images if f.name.lower().startswith('cat')]
    dog_images = [f for f in all_images if f.name.lower().startswith('dog')]
    
    print(f"Found {len(cat_images)} cat images")
    print(f"Found {len(dog_images)} dog images")
    
    if len(cat_images) == 0 and len(dog_images) == 0:
        print("No images found! Please download the dataset first.")
        return {"error": "No images found"}
    
    # Create output directories
    splits = ['train', 'val', 'test']
    classes = ['cat', 'dog']
    
    for split in splits:
        for cls in classes:
            (processed_dir / split / cls).mkdir(parents=True, exist_ok=True)
    
    # Split and copy images
    stats = {}
    random.seed(seed)
    
    for cls, images in [('cat', cat_images), ('dog', dog_images)]:
        # Shuffle images
        shuffled = images.copy()
        random.shuffle(shuffled)
        
        # Calculate split indices
        total = len(shuffled)
        train_end = int(total * train_ratio)
        val_end = train_end + int(total * val_ratio)
        
        split_images = {
            'train': shuffled[:train_end],
            'val': shuffled[train_end:val_end],
            'test': shuffled[val_end:]
        }
        
        for split, split_files in split_images.items():
            dest_dir = processed_dir / split / cls
            for src_file in split_files:
                dest_file = dest_dir / src_file.name
                if not dest_file.exists():
                    shutil.copy2(src_file, dest_file)
            
            stats[f"{split}_{cls}"] = len(split_files)
            print(f"  {split}/{cls}: {len(split_files)} images")
    
    print("\n" + "=" * 60)
    print("Dataset organization complete!")
    print("=" * 60)
    
    return stats


def preprocess_and_save(
    source_dir: Path,
    output_dir: Path,
    target_size: Tuple[int, int] = IMG_SIZE
) -> int:
    """
    Preprocess all images in source directory and save to output directory
    
    Args:
        source_dir: Source directory with original images
        output_dir: Output directory for preprocessed images
        target_size: Target size for images
        
    Returns:
        Number of images processed
    """
    source_dir = Path(source_dir)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    processed_count = 0
    
    for img_path in source_dir.glob("*"):
        if img_path.suffix.lower() in ['.jpg', '.jpeg', '.png', '.bmp']:
            try:
                # Load and resize image
                img = Image.open(img_path).convert('RGB')
                img = img.resize((target_size[1], target_size[0]), Image.Resampling.LANCZOS)
                
                # Save preprocessed image
                output_path = output_dir / img_path.name
                img.save(output_path, quality=95)
                processed_count += 1
                
            except Exception as e:
                print(f"Error processing {img_path}: {e}")
    
    return processed_count


if __name__ == "__main__":
    """
    Main script to preprocess the Cats vs Dogs dataset
    """
    import argparse
    
    parser = argparse.ArgumentParser(description="Preprocess Cats vs Dogs dataset")
    parser.add_argument("--raw-dir", type=str, default=str(RAW_DATA_DIR),
                        help="Raw data directory")
    parser.add_argument("--output-dir", type=str, default=str(PROCESSED_DATA_DIR),
                        help="Output directory for processed data")
    parser.add_argument("--train-ratio", type=float, default=TRAIN_RATIO,
                        help="Training set ratio")
    parser.add_argument("--val-ratio", type=float, default=VAL_RATIO,
                        help="Validation set ratio")
    parser.add_argument("--test-ratio", type=float, default=TEST_RATIO,
                        help="Test set ratio")
    parser.add_argument("--seed", type=int, default=RANDOM_SEED,
                        help="Random seed")
    
    args = parser.parse_args()
    
    # Organize the dataset
    organize_kaggle_dataset(
        raw_dir=Path(args.raw_dir),
        processed_dir=Path(args.output_dir),
        train_ratio=args.train_ratio,
        val_ratio=args.val_ratio,
        test_ratio=args.test_ratio,
        seed=args.seed
    )



