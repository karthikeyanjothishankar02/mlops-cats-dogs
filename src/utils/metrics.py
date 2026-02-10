"""
Utility functions for metrics calculation
"""
import numpy as np
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report,
)
from typing import Dict, Tuple
import matplotlib.pyplot as plt
import seaborn as sns


def calculate_metrics(y_true: np.ndarray, y_pred: np.ndarray) -> Dict[str, float]:
    """
    Calculate classification metrics
    
    Args:
        y_true: True labels
        y_pred: Predicted labels
        
    Returns:
        Dictionary containing accuracy, precision, recall, and f1 score
    """
    metrics = {
        "accuracy": accuracy_score(y_true, y_pred),
        "precision": precision_score(y_true, y_pred, average="binary", zero_division=0),
        "recall": recall_score(y_true, y_pred, average="binary", zero_division=0),
        "f1_score": f1_score(y_true, y_pred, average="binary", zero_division=0),
    }
    return metrics


def get_confusion_matrix(y_true: np.ndarray, y_pred: np.ndarray) -> np.ndarray:
    """
    Calculate confusion matrix
    
    Args:
        y_true: True labels
        y_pred: Predicted labels
        
    Returns:
        Confusion matrix as numpy array
    """
    return confusion_matrix(y_true, y_pred)


def plot_confusion_matrix(
    cm: np.ndarray, class_names: list, save_path: str = None
) -> plt.Figure:
    """
    Plot confusion matrix
    
    Args:
        cm: Confusion matrix
        class_names: List of class names
        save_path: Path to save the plot
        
    Returns:
        Matplotlib figure
    """
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(
        cm,
        annot=True,
        fmt="d",
        cmap="Blues",
        xticklabels=class_names,
        yticklabels=class_names,
        ax=ax,
    )
    ax.set_xlabel("Predicted")
    ax.set_ylabel("Actual")
    ax.set_title("Confusion Matrix")
    
    if save_path:
        plt.savefig(save_path)
    
    return fig


def plot_training_history(
    history: Dict[str, list], save_path: str = None
) -> plt.Figure:
    """
    Plot training history (loss and accuracy)
    
    Args:
        history: Dictionary with training history
        save_path: Path to save the plot
        
    Returns:
        Matplotlib figure
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))
    
    # Plot loss
    ax1.plot(history["train_loss"], label="Train Loss")
    ax1.plot(history["val_loss"], label="Validation Loss")
    ax1.set_xlabel("Epoch")
    ax1.set_ylabel("Loss")
    ax1.set_title("Training and Validation Loss")
    ax1.legend()
    ax1.grid(True)
    
    # Plot accuracy
    ax2.plot(history["train_acc"], label="Train Accuracy")
    ax2.plot(history["val_acc"], label="Validation Accuracy")
    ax2.set_xlabel("Epoch")
    ax2.set_ylabel("Accuracy")
    ax2.set_title("Training and Validation Accuracy")
    ax2.legend()
    ax2.grid(True)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path)
    
    return fig


def print_classification_report(y_true: np.ndarray, y_pred: np.ndarray, class_names: list):
    """
    Print detailed classification report

    Args:
        y_true: True labels
        y_pred: Predicted labels
        class_names: List of class names
    """
    print("\nClassification Report:")
    print("=" * 60)
    # Always use all class indices
    labels = list(range(len(class_names)))
    print(classification_report(
        y_true,
        y_pred,
        labels=labels,
        target_names=class_names,
        zero_division=0  # Avoid division by zero warnings
    ))
