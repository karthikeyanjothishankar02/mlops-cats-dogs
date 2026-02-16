"""
Data augmentation transforms for Cats vs Dogs classification

This module provides PyTorch transforms for:
- Training augmentation (random flips, rotations, color jitter, etc.)
- Validation/Test transforms (normalize only)
- Inference transforms (for prediction)
"""
from torchvision import transforms
from typing import Tuple


def get_train_transforms(
    img_size: Tuple[int, int] = (224, 224),
    mean: Tuple[float, ...] = (0.485, 0.456, 0.406),
    std: Tuple[float, ...] = (0.229, 0.224, 0.225)
) -> transforms.Compose:
    """
    Get training data transforms with augmentation
    
    Augmentations applied:
    - Random resized crop
    - Random horizontal flip
    - Random rotation
    - Color jitter (brightness, contrast, saturation, hue)
    - Random affine transformations
    - Normalization with ImageNet statistics
    
    Args:
        img_size: Target image size (height, width)
        mean: Normalization mean (default: ImageNet)
        std: Normalization std (default: ImageNet)
        
    Returns:
        Composed transforms for training
    """
    return transforms.Compose([
        # Resize with some random crop variation
        transforms.RandomResizedCrop(
            img_size,
            scale=(0.8, 1.0),
            ratio=(0.9, 1.1)
        ),
        # Random horizontal flip (50% probability)
        transforms.RandomHorizontalFlip(p=0.5),
        # Random rotation up to 15 degrees
        transforms.RandomRotation(degrees=15),
        # Color jitter for robustness
        transforms.ColorJitter(
            brightness=0.2,
            contrast=0.2,
            saturation=0.2,
            hue=0.1
        ),
        # Random affine for slight perspective changes
        transforms.RandomAffine(
            degrees=0,
            translate=(0.1, 0.1),
            scale=(0.9, 1.1)
        ),
        # Convert to tensor
        transforms.ToTensor(),
        # Normalize with ImageNet statistics
        transforms.Normalize(mean=mean, std=std),
    ])


def get_val_transforms(
    img_size: Tuple[int, int] = (224, 224),
    mean: Tuple[float, ...] = (0.485, 0.456, 0.406),
    std: Tuple[float, ...] = (0.229, 0.224, 0.225)
) -> transforms.Compose:
    """
    Get validation/test data transforms (no augmentation)
    
    Args:
        img_size: Target image size (height, width)
        mean: Normalization mean (default: ImageNet)
        std: Normalization std (default: ImageNet)
        
    Returns:
        Composed transforms for validation/testing
    """
    return transforms.Compose([
        # Resize to target size
        transforms.Resize(img_size),
        # Center crop to ensure consistent size
        transforms.CenterCrop(img_size),
        # Convert to tensor
        transforms.ToTensor(),
        # Normalize with ImageNet statistics
        transforms.Normalize(mean=mean, std=std),
    ])


def get_inference_transforms(
    img_size: Tuple[int, int] = (224, 224),
    mean: Tuple[float, ...] = (0.485, 0.456, 0.406),
    std: Tuple[float, ...] = (0.229, 0.224, 0.225)
) -> transforms.Compose:
    """
    Get inference transforms for prediction
    
    Same as validation transforms but can be customized for production
    
    Args:
        img_size: Target image size (height, width)
        mean: Normalization mean (default: ImageNet)
        std: Normalization std (default: ImageNet)
        
    Returns:
        Composed transforms for inference
    """
    return transforms.Compose([
        # Resize to target size
        transforms.Resize(img_size),
        # Center crop to ensure consistent size
        transforms.CenterCrop(img_size),
        # Convert to tensor
        transforms.ToTensor(),
        # Normalize with ImageNet statistics
        transforms.Normalize(mean=mean, std=std),
    ])


def get_test_time_augmentation_transforms(
    img_size: Tuple[int, int] = (224, 224),
    mean: Tuple[float, ...] = (0.485, 0.456, 0.406),
    std: Tuple[float, ...] = (0.229, 0.224, 0.225)
) -> list:
    """
    Get multiple transforms for Test Time Augmentation (TTA)
    
    Returns multiple transform variants that can be applied to the same
    image for more robust predictions through averaging.
    
    Args:
        img_size: Target image size (height, width)
        mean: Normalization mean
        std: Normalization std
        
    Returns:
        List of composed transforms for TTA
    """
    base_transforms = [
        transforms.Resize(img_size),
        transforms.ToTensor(),
        transforms.Normalize(mean=mean, std=std),
    ]
    
    tta_variants = [
        # Original
        transforms.Compose([
            transforms.Resize(img_size),
            transforms.CenterCrop(img_size),
            transforms.ToTensor(),
            transforms.Normalize(mean=mean, std=std),
        ]),
        # Horizontal flip
        transforms.Compose([
            transforms.Resize(img_size),
            transforms.CenterCrop(img_size),
            transforms.RandomHorizontalFlip(p=1.0),
            transforms.ToTensor(),
            transforms.Normalize(mean=mean, std=std),
        ]),
        # Slight zoom in
        transforms.Compose([
            transforms.Resize(int(img_size[0] * 1.1)),
            transforms.CenterCrop(img_size),
            transforms.ToTensor(),
            transforms.Normalize(mean=mean, std=std),
        ]),
        # Slight zoom out
        transforms.Compose([
            transforms.Resize(int(img_size[0] * 0.9)),
            transforms.Pad(padding=int(img_size[0] * 0.05), fill=0),
            transforms.Resize(img_size),
            transforms.ToTensor(),
            transforms.Normalize(mean=mean, std=std),
        ]),
    ]
    
    return tta_variants


# ImageNet statistics for reference
IMAGENET_MEAN = (0.485, 0.456, 0.406)
IMAGENET_STD = (0.229, 0.224, 0.225)


if __name__ == "__main__":
    """
    Test the augmentation transforms
    """
    from PIL import Image
    import torch
    
    # Create a dummy image
    dummy_image = Image.new('RGB', (300, 300), color='blue')
    
    # Test training transforms
    print("Testing training transforms...")
    train_transform = get_train_transforms()
    train_output = train_transform(dummy_image)
    print(f"  Output shape: {train_output.shape}")
    print(f"  Output dtype: {train_output.dtype}")
    print(f"  Output range: [{train_output.min():.3f}, {train_output.max():.3f}]")
    
    # Test validation transforms
    print("\nTesting validation transforms...")
    val_transform = get_val_transforms()
    val_output = val_transform(dummy_image)
    print(f"  Output shape: {val_output.shape}")
    print(f"  Output dtype: {val_output.dtype}")
    
    # Test inference transforms
    print("\nTesting inference transforms...")
    inf_transform = get_inference_transforms()
    inf_output = inf_transform(dummy_image)
    print(f"  Output shape: {inf_output.shape}")
    
    # Test TTA transforms
    print("\nTesting TTA transforms...")
    tta_transforms = get_test_time_augmentation_transforms()
    print(f"  Number of TTA variants: {len(tta_transforms)}")
    for i, tta in enumerate(tta_transforms):
        output = tta(dummy_image)
        print(f"  Variant {i+1} shape: {output.shape}")
    
    print("\nAll augmentation tests passed!")



