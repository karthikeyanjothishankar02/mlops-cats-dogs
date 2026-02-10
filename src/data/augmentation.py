"""
Data augmentation utilities
"""
import torch
from torchvision import transforms
from typing import Tuple


def get_train_transforms(img_size: Tuple[int, int] = (224, 224)):
    """
    Get training data augmentation transforms
    
    Args:
        img_size: Target image size (height, width)
        
    Returns:
        torchvision transforms composition
    """
    return transforms.Compose([
        transforms.Resize(img_size),
        transforms.RandomHorizontalFlip(p=0.5),
        transforms.RandomRotation(degrees=15),
        transforms.RandomAffine(degrees=0, translate=(0.1, 0.1)),
        transforms.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2, hue=0.1),
        transforms.RandomPerspective(distortion_scale=0.2, p=0.5),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])


def get_val_transforms(img_size: Tuple[int, int] = (224, 224)):
    """
    Get validation/test data transforms (no augmentation)
    
    Args:
        img_size: Target image size (height, width)
        
    Returns:
        torchvision transforms composition
    """
    return transforms.Compose([
        transforms.Resize(img_size),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])


def get_inference_transforms(img_size: Tuple[int, int] = (224, 224)):
    """
    Get inference transforms (same as validation)
    
    Args:
        img_size: Target image size (height, width)
        
    Returns:
        torchvision transforms composition
    """
    return get_val_transforms(img_size)
