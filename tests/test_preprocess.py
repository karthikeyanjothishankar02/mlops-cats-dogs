"""
Unit tests for data preprocessing functions
"""
import pytest
import numpy as np
from PIL import Image
import tempfile
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent))

from src.data.preprocess import load_and_preprocess_image, split_dataset
from src.utils.config import IMG_SIZE


class TestPreprocessing:
    """Test data preprocessing functions"""
    
    @pytest.fixture
    def create_test_image(self):
        """Create a temporary test image"""
        # Create a temporary image
        img = Image.new('RGB', (300, 300), color='red')
        temp_file = tempfile.NamedTemporaryFile(suffix='.jpg', delete=False)
        img.save(temp_file.name)
        temp_file.close()
        yield temp_file.name
        # Cleanup
        Path(temp_file.name).unlink()
    
    def test_load_and_preprocess_image_shape(self, create_test_image):
        """Test if image is preprocessed to correct shape"""
        img_array = load_and_preprocess_image(create_test_image, IMG_SIZE)
        
        assert img_array is not None
        assert img_array.shape == (IMG_SIZE[0], IMG_SIZE[1], 3)
    
    def test_load_and_preprocess_image_normalization(self, create_test_image):
        """Test if image values are normalized to [0, 1]"""
        img_array = load_and_preprocess_image(create_test_image, IMG_SIZE)
        
        assert img_array is not None
        assert img_array.min() >= 0.0
        assert img_array.max() <= 1.0
    
    def test_load_and_preprocess_image_type(self, create_test_image):
        """Test if output is numpy array"""
        img_array = load_and_preprocess_image(create_test_image, IMG_SIZE)
        
        assert isinstance(img_array, np.ndarray)
        assert img_array.dtype == np.float64 or img_array.dtype == np.float32
    
    def test_load_nonexistent_image(self):
        """Test handling of nonexistent image"""
        result = load_and_preprocess_image("nonexistent_image.jpg")
        assert result is None
    
    def test_split_dataset_ratios(self, tmp_path):
        """Test if dataset split maintains correct ratios"""
        # Create temporary dataset
        for i in range(100):
            img_file = tmp_path / f"image_{i}.jpg"
            img = Image.new('RGB', (100, 100))
            img.save(img_file)
        
        train_files, val_files, test_files = split_dataset(
            tmp_path, 
            train_ratio=0.8, 
            val_ratio=0.1, 
            test_ratio=0.1
        )
        
        total = len(train_files) + len(val_files) + len(test_files)
        
        assert total == 100
        assert len(train_files) == 80
        assert len(val_files) == 10
        assert len(test_files) == 10
    
    def test_split_dataset_no_overlap(self, tmp_path):
        """Test if there's no overlap between splits"""
        # Create temporary dataset
        for i in range(30):
            img_file = tmp_path / f"image_{i}.jpg"
            img = Image.new('RGB', (100, 100))
            img.save(img_file)
        
        train_files, val_files, test_files = split_dataset(tmp_path)
        
        # Convert to sets
        train_set = set(train_files)
        val_set = set(val_files)
        test_set = set(test_files)
        
        # Check for no overlap
        assert len(train_set.intersection(val_set)) == 0
        assert len(train_set.intersection(test_set)) == 0
        assert len(val_set.intersection(test_set)) == 0
    
    def test_split_dataset_reproducibility(self, tmp_path):
        """Test if split is reproducible with same seed"""
        # Create temporary dataset
        for i in range(50):
            img_file = tmp_path / f"image_{i}.jpg"
            img = Image.new('RGB', (100, 100))
            img.save(img_file)
        
        # First split
        train1, val1, test1 = split_dataset(tmp_path, seed=42)
        
        # Second split with same seed
        train2, val2, test2 = split_dataset(tmp_path, seed=42)
        
        # Should be identical
        assert train1 == train2
        assert val1 == val2
        assert test1 == test2
