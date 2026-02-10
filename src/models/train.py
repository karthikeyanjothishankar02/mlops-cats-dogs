"""
Model training script with MLflow tracking
"""
import argparse
import os
import sys
from pathlib import Path
import time
from datetime import datetime

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from torchvision import datasets
import mlflow
import mlflow.pytorch
import numpy as np

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent.parent))

from src.models.cnn_model import get_model
from src.data.augmentation import get_train_transforms, get_val_transforms
from src.utils.config import (
    TRAIN_DIR,
    VAL_DIR,
    TEST_DIR,
    MODELS_DIR,
    BATCH_SIZE,
    EPOCHS,
    LEARNING_RATE,
    NUM_CLASSES,
    CLASS_NAMES,
    IMG_SIZE,
    MLFLOW_EXPERIMENT_NAME,
)
from src.utils.metrics import (
    calculate_metrics,
    get_confusion_matrix,
    plot_confusion_matrix,
    plot_training_history,
    print_classification_report,
)


def get_data_loaders(batch_size: int = BATCH_SIZE):
    """
    Create data loaders for training, validation, and testing
    
    Args:
        batch_size: Batch size for data loaders
        
    Returns:
        Tuple of (train_loader, val_loader, test_loader)
    """
    # Create datasets with transforms
    train_dataset = datasets.ImageFolder(
        TRAIN_DIR,
        transform=get_train_transforms(IMG_SIZE)
    )
    
    val_dataset = datasets.ImageFolder(
        VAL_DIR,
        transform=get_val_transforms(IMG_SIZE)
    )
    
    test_dataset = datasets.ImageFolder(
        TEST_DIR,
        transform=get_val_transforms(IMG_SIZE)
    )
    
    # Create data loaders
    train_loader = DataLoader(
        train_dataset,
        batch_size=batch_size,
        shuffle=True,
        num_workers=2,
        pin_memory=True
    )
    
    val_loader = DataLoader(
        val_dataset,
        batch_size=batch_size,
        shuffle=False,
        num_workers=2,
        pin_memory=True
    )
    
    test_loader = DataLoader(
        test_dataset,
        batch_size=batch_size,
        shuffle=False,
        num_workers=2,
        pin_memory=True
    )
    
    return train_loader, val_loader, test_loader


def train_epoch(model, train_loader, criterion, optimizer, device):
    """
    Train for one epoch
    
    Args:
        model: PyTorch model
        train_loader: Training data loader
        criterion: Loss function
        optimizer: Optimizer
        device: Device to train on
        
    Returns:
        Tuple of (average_loss, accuracy)
    """
    model.train()
    running_loss = 0.0
    correct = 0
    total = 0
    
    for inputs, labels in train_loader:
        inputs, labels = inputs.to(device), labels.to(device)
        
        # Zero gradients
        optimizer.zero_grad()
        
        # Forward pass
        outputs = model(inputs)
        loss = criterion(outputs, labels)
        
        # Backward pass and optimization
        loss.backward()
        optimizer.step()
        
        # Statistics
        running_loss += loss.item() * inputs.size(0)
        _, predicted = torch.max(outputs, 1)
        total += labels.size(0)
        correct += (predicted == labels).sum().item()
    
    epoch_loss = running_loss / total
    epoch_acc = correct / total
    
    return epoch_loss, epoch_acc


def validate(model, val_loader, criterion, device):
    """
    Validate the model
    
    Args:
        model: PyTorch model
        val_loader: Validation data loader
        criterion: Loss function
        device: Device to validate on
        
    Returns:
        Tuple of (average_loss, accuracy, predictions, true_labels)
    """
    model.eval()
    running_loss = 0.0
    correct = 0
    total = 0
    all_preds = []
    all_labels = []
    
    with torch.no_grad():
        for inputs, labels in val_loader:
            inputs, labels = inputs.to(device), labels.to(device)
            
            # Forward pass
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            
            # Statistics
            running_loss += loss.item() * inputs.size(0)
            _, predicted = torch.max(outputs, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
            
            all_preds.extend(predicted.cpu().numpy())
            all_labels.extend(labels.cpu().numpy())
    
    epoch_loss = running_loss / total
    epoch_acc = correct / total
    
    return epoch_loss, epoch_acc, np.array(all_preds), np.array(all_labels)


def train_model(args):
    """
    Main training function
    
    Args:
        args: Command line arguments
    """
    # Set device
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")
    
    # Set MLflow experiment
    mlflow.set_experiment(MLFLOW_EXPERIMENT_NAME)
    
    # Start MLflow run
    with mlflow.start_run(run_name=f"cnn_training_{datetime.now().strftime('%Y%m%d_%H%M%S')}"):
        # Log parameters
        mlflow.log_param("model_architecture", "Custom CNN")
        mlflow.log_param("batch_size", args.batch_size)
        mlflow.log_param("epochs", args.epochs)
        mlflow.log_param("learning_rate", args.learning_rate)
        mlflow.log_param("optimizer", "Adam")
        mlflow.log_param("image_size", IMG_SIZE)
        mlflow.log_param("dropout", args.dropout)
        
        # Get data loaders
        print("Loading data...")
        train_loader, val_loader, test_loader = get_data_loaders(args.batch_size)
        print(f"Training samples: {len(train_loader.dataset)}")
        print(f"Validation samples: {len(val_loader.dataset)}")
        print(f"Test samples: {len(test_loader.dataset)}")
        
        # Create model
        print("\nCreating model...")
        model = get_model(num_classes=NUM_CLASSES, dropout=args.dropout)
        model = model.to(device)
        
        # Loss and optimizer
        criterion = nn.CrossEntropyLoss()
        optimizer = optim.Adam(model.parameters(), lr=args.learning_rate)
        scheduler = optim.lr_scheduler.ReduceLROnPlateau(
            optimizer, mode='min', factor=0.5, patience=3
        )
        
        # Training history
        history = {
            "train_loss": [],
            "train_acc": [],
            "val_loss": [],
            "val_acc": []
        }
        
        best_val_acc = 0.0
        
        # Training loop
        print(f"\nStarting training for {args.epochs} epochs...")
        start_time = time.time()
        
        for epoch in range(args.epochs):
            epoch_start = time.time()
            
            # Train
            train_loss, train_acc = train_epoch(
                model, train_loader, criterion, optimizer, device
            )
            
            # Validate
            val_loss, val_acc, val_preds, val_labels = validate(
                model, val_loader, criterion, device
            )
            
            # Update learning rate
            scheduler.step(val_loss)
            
            # Save history
            history["train_loss"].append(train_loss)
            history["train_acc"].append(train_acc)
            history["val_loss"].append(val_loss)
            history["val_acc"].append(val_acc)
            
            # Log metrics to MLflow
            mlflow.log_metric("train_loss", train_loss, step=epoch)
            mlflow.log_metric("train_acc", train_acc, step=epoch)
            mlflow.log_metric("val_loss", val_loss, step=epoch)
            mlflow.log_metric("val_acc", val_acc, step=epoch)
            
            epoch_time = time.time() - epoch_start
            
            print(f"Epoch [{epoch+1}/{args.epochs}] ({epoch_time:.2f}s)")
            print(f"  Train Loss: {train_loss:.4f} | Train Acc: {train_acc:.4f}")
            print(f"  Val Loss: {val_loss:.4f} | Val Acc: {val_acc:.4f}")
            
            # Save best model
            if val_acc > best_val_acc:
                best_val_acc = val_acc
                model_path = MODELS_DIR / "best_model.pt"
                torch.save({
                    'epoch': epoch,
                    'model_state_dict': model.state_dict(),
                    'optimizer_state_dict': optimizer.state_dict(),
                    'val_acc': val_acc,
                    'val_loss': val_loss,
                }, model_path)
                print(f"  ✓ New best model saved! (Val Acc: {val_acc:.4f})")
        
        total_time = time.time() - start_time
        print(f"\nTraining completed in {total_time/60:.2f} minutes")
        print(f"Best validation accuracy: {best_val_acc:.4f}")
        
        # Test evaluation
        print("\nEvaluating on test set...")
        test_loss, test_acc, test_preds, test_labels = validate(
            model, test_loader, criterion, device
        )
        
        print(f"Test Loss: {test_loss:.4f}")
        print(f"Test Accuracy: {test_acc:.4f}")
        
        # Calculate detailed metrics
        test_metrics = calculate_metrics(test_labels, test_preds)
        print(f"\nTest Metrics:")
        for metric, value in test_metrics.items():
            print(f"  {metric}: {value:.4f}")
            mlflow.log_metric(f"test_{metric}", value)
        
        # Confusion matrix
        cm = get_confusion_matrix(test_labels, test_preds)
        cm_fig = plot_confusion_matrix(cm, CLASS_NAMES, save_path=MODELS_DIR / "confusion_matrix.png")
        mlflow.log_figure(cm_fig, "confusion_matrix.png")
        
        # Training history plot
        history_fig = plot_training_history(history, save_path=MODELS_DIR / "training_history.png")
        mlflow.log_figure(history_fig, "training_history.png")
        
        # Classification report
        print_classification_report(test_labels, test_preds, CLASS_NAMES)
        
        # Log model to MLflow
        mlflow.pytorch.log_model(model, "model")
        
        # Save final model
        final_model_path = MODELS_DIR / "final_model.pt"
        torch.save(model.state_dict(), final_model_path)
        mlflow.log_artifact(str(final_model_path))
        
        print(f"\n✓ Training complete! Model saved to {MODELS_DIR}")


def main():
    parser = argparse.ArgumentParser(description="Train Cats vs Dogs CNN model")
    parser.add_argument("--batch_size", type=int, default=BATCH_SIZE, help="Batch size")
    parser.add_argument("--epochs", type=int, default=EPOCHS, help="Number of epochs")
    parser.add_argument("--learning_rate", type=float, default=LEARNING_RATE, help="Learning rate")
    parser.add_argument("--dropout", type=float, default=0.5, help="Dropout rate")
    
    args = parser.parse_args()
    
    # Check if processed data exists
    if not TRAIN_DIR.exists():
        print("Error: Processed training data not found!")
        print("Please run: python src/data/preprocess.py")
        sys.exit(1)
    
    train_model(args)


if __name__ == "__main__":
    main()
