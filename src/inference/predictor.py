"""
Model predictor for inference
"""
import torch
import numpy as np
from PIL import Image
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent.parent))

from src.models.cnn_model import get_model
from src.data.augmentation import get_inference_transforms
from src.utils.config import NUM_CLASSES, CLASS_NAMES, IMG_SIZE, MODELS_DIR


class CatDogPredictor:
    """
    Predictor class for Cats vs Dogs classification
    """
    
    def __init__(self, model_path: str = None, device: str = None):
        """
        Initialize the predictor
        
        Args:
            model_path: Path to the trained model file
            device: Device to run inference on ('cpu' or 'cuda')
        """
        if device is None:
            self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        else:
            self.device = torch.device(device)
        
        # Load model
        self.model = get_model(num_classes=NUM_CLASSES)
        
        if model_path is None:
            model_path = MODELS_DIR / "best_model.pt"
        
        if not Path(model_path).exists():
            raise FileNotFoundError(f"Model file not found: {model_path}")
        
        # Load model weights
        checkpoint = torch.load(model_path, map_location=self.device)
        
        # Handle different checkpoint formats
        if isinstance(checkpoint, dict) and 'model_state_dict' in checkpoint:
            self.model.load_state_dict(checkpoint['model_state_dict'])
        else:
            self.model.load_state_dict(checkpoint)
        
        self.model = self.model.to(self.device)
        self.model.eval()
        
        # Get transforms
        self.transform = get_inference_transforms(IMG_SIZE)
        
        print(f"Model loaded successfully on {self.device}")
    
    def preprocess_image(self, image_input):
        """
        Preprocess image for inference
        
        Args:
            image_input: PIL Image, numpy array, or file path
            
        Returns:
            Preprocessed tensor
        """
        # Convert to PIL Image if needed
        if isinstance(image_input, str) or isinstance(image_input, Path):
            image = Image.open(image_input).convert('RGB')
        elif isinstance(image_input, np.ndarray):
            image = Image.fromarray(image_input).convert('RGB')
        elif isinstance(image_input, Image.Image):
            image = image_input.convert('RGB')
        else:
            raise ValueError("Unsupported image input type")
        
        # Apply transforms
        tensor = self.transform(image)
        
        # Add batch dimension
        tensor = tensor.unsqueeze(0)
        
        return tensor
    
    def predict(self, image_input, return_probs: bool = True):
        """
        Make prediction on an image
        
        Args:
            image_input: PIL Image, numpy array, or file path
            return_probs: Whether to return probabilities or just the class
            
        Returns:
            Dictionary with prediction results
        """
        # Preprocess image
        tensor = self.preprocess_image(image_input)
        tensor = tensor.to(self.device)
        
        # Inference
        with torch.no_grad():
            outputs = self.model(tensor)
            probabilities = torch.softmax(outputs, dim=1)
            predicted_class_idx = torch.argmax(probabilities, dim=1).item()
            confidence = probabilities[0][predicted_class_idx].item()
        
        predicted_class = CLASS_NAMES[predicted_class_idx]
        
        result = {
            "predicted_class": predicted_class,
            "confidence": confidence,
            "class_index": predicted_class_idx
        }
        
        if return_probs:
            result["probabilities"] = {
                CLASS_NAMES[i]: probabilities[0][i].item()
                for i in range(len(CLASS_NAMES))
            }
        
        return result
    
    def predict_batch(self, image_inputs: list):
        """
        Make predictions on a batch of images
        
        Args:
            image_inputs: List of PIL Images, numpy arrays, or file paths
            
        Returns:
            List of prediction dictionaries
        """
        results = []
        for image_input in image_inputs:
            result = self.predict(image_input)
            results.append(result)
        return results


if __name__ == "__main__":
    # Test predictor
    import argparse
    
    parser = argparse.ArgumentParser(description="Test the predictor")
    parser.add_argument("--image", type=str, required=True, help="Path to test image")
    parser.add_argument("--model", type=str, default=None, help="Path to model file")
    
    args = parser.parse_args()
    
    # Create predictor
    predictor = CatDogPredictor(model_path=args.model)
    
    # Make prediction
    result = predictor.predict(args.image)
    
    print("\nPrediction Results:")
    print(f"  Predicted Class: {result['predicted_class']}")
    print(f"  Confidence: {result['confidence']:.4f}")
    print("\nClass Probabilities:")
    for class_name, prob in result['probabilities'].items():
        print(f"  {class_name}: {prob:.4f}")
