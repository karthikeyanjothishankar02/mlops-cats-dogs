"""
Unit tests for inference functions
"""
import pytest
import numpy as np
from PIL import Image
import tempfile
from pathlib import Path
import sys
import torch

sys.path.append(str(Path(__file__).parent.parent))

from src.inference.predictor import CatDogPredictor
from src.models.cnn_model import get_model
from src.utils.config import IMG_SIZE, NUM_CLASSES, MODELS_DIR


class TestInference:
    """Test inference functions"""
    
    @pytest.fixture
    def create_test_image(self):
        """Create a temporary test image"""
        img = Image.new('RGB', (300, 300), color='blue')
        temp_file = tempfile.NamedTemporaryFile(suffix='.jpg', delete=False)
        img.save(temp_file.name)
        temp_file.close()
        yield temp_file.name
        Path(temp_file.name).unlink()
    
    @pytest.fixture
    def create_test_model(self):
        """Create a test model and save it"""
        model = get_model(num_classes=NUM_CLASSES)
        temp_model = tempfile.NamedTemporaryFile(suffix='.pt', delete=False)
        torch.save(model.state_dict(), temp_model.name)
        temp_model.close()
        yield temp_model.name
        Path(temp_model.name).unlink()
    
    def test_model_architecture(self):
        """Test if model has correct architecture"""
        model = get_model(num_classes=NUM_CLASSES)
        
        # Test output shape
        dummy_input = torch.randn(1, 3, IMG_SIZE[0], IMG_SIZE[1])
        output = model(dummy_input)
        
        assert output.shape == (1, NUM_CLASSES)
    
    def test_predictor_initialization(self, create_test_model):
        """Test if predictor initializes correctly"""
        predictor = CatDogPredictor(model_path=create_test_model, device='cpu')
        
        assert predictor.model is not None
        assert predictor.device == torch.device('cpu')
    
    def test_preprocess_image_from_path(self, create_test_model, create_test_image):
        """Test image preprocessing from file path"""
        predictor = CatDogPredictor(model_path=create_test_model, device='cpu')
        tensor = predictor.preprocess_image(create_test_image)
        
        assert tensor.shape == (1, 3, IMG_SIZE[0], IMG_SIZE[1])
        assert isinstance(tensor, torch.Tensor)
    
    def test_preprocess_image_from_pil(self, create_test_model):
        """Test image preprocessing from PIL Image"""
        predictor = CatDogPredictor(model_path=create_test_model, device='cpu')
        img = Image.new('RGB', (300, 300), color='green')
        tensor = predictor.preprocess_image(img)
        
        assert tensor.shape == (1, 3, IMG_SIZE[0], IMG_SIZE[1])
    
    def test_preprocess_image_from_numpy(self, create_test_model):
        """Test image preprocessing from numpy array"""
        predictor = CatDogPredictor(model_path=create_test_model, device='cpu')
        img_array = np.random.randint(0, 255, (300, 300, 3), dtype=np.uint8)
        tensor = predictor.preprocess_image(img_array)
        
        assert tensor.shape == (1, 3, IMG_SIZE[0], IMG_SIZE[1])
    
    def test_predict_output_format(self, create_test_model, create_test_image):
        """Test if prediction output has correct format"""
        predictor = CatDogPredictor(model_path=create_test_model, device='cpu')
        result = predictor.predict(create_test_image)
        
        # Check required keys
        assert 'predicted_class' in result
        assert 'confidence' in result
        assert 'class_index' in result
        assert 'probabilities' in result
        
        # Check types
        assert isinstance(result['predicted_class'], str)
        assert isinstance(result['confidence'], float)
        assert isinstance(result['class_index'], int)
        assert isinstance(result['probabilities'], dict)
    
    def test_predict_confidence_range(self, create_test_model, create_test_image):
        """Test if confidence is in valid range [0, 1]"""
        predictor = CatDogPredictor(model_path=create_test_model, device='cpu')
        result = predictor.predict(create_test_image)
        
        assert 0.0 <= result['confidence'] <= 1.0
    
    def test_predict_probabilities_sum(self, create_test_model, create_test_image):
        """Test if probabilities sum to approximately 1"""
        predictor = CatDogPredictor(model_path=create_test_model, device='cpu')
        result = predictor.predict(create_test_image)
        
        prob_sum = sum(result['probabilities'].values())
        assert abs(prob_sum - 1.0) < 0.01  # Allow small floating point error
    
    def test_predict_batch(self, create_test_model, create_test_image):
        """Test batch prediction"""
        predictor = CatDogPredictor(model_path=create_test_model, device='cpu')
        
        # Create multiple test images
        images = [create_test_image] * 3
        results = predictor.predict_batch(images)
        
        assert len(results) == 3
        assert all('predicted_class' in r for r in results)
    
    def test_model_eval_mode(self, create_test_model):
        """Test if model is in evaluation mode"""
        predictor = CatDogPredictor(model_path=create_test_model, device='cpu')
        assert not predictor.model.training


class TestModelUtilities:
    """Test model utility functions"""
    
    def test_get_model_default(self):
        """Test model creation with default parameters"""
        model = get_model()
        assert model is not None
        assert isinstance(model, torch.nn.Module)
    
    def test_get_model_custom_classes(self):
        """Test model creation with custom number of classes"""
        model = get_model(num_classes=5)
        
        dummy_input = torch.randn(1, 3, IMG_SIZE[0], IMG_SIZE[1])
        output = model(dummy_input)
        
        assert output.shape == (1, 5)
    
    def test_get_model_custom_dropout(self):
        """Test model creation with custom dropout"""
        model = get_model(dropout=0.3)
        assert model is not None
    
    def test_model_parameters_trainable(self):
        """Test if model parameters are trainable"""
        model = get_model()
        trainable = sum(p.numel() for p in model.parameters() if p.requires_grad)
        assert trainable > 0
