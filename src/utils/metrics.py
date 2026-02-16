"""
Metrics utilities for model evaluation and visualization
"""

from pathlib import Path
from typing import Dict, List, Optional, Tuple

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)


def calculate_metrics(
    y_true: np.ndarray, y_pred: np.ndarray, average: str = "binary"
) -> Dict[str, float]:
    """
    Calculate classification metrics

    Args:
        y_true: Ground truth labels
        y_pred: Predicted labels
        average: Averaging strategy for multi-class

    Returns:
        Dictionary of metrics
    """
    metrics = {
        "accuracy": accuracy_score(y_true, y_pred),
        "precision": precision_score(y_true, y_pred, average=average, zero_division=0),
        "recall": recall_score(y_true, y_pred, average=average, zero_division=0),
        "f1_score": f1_score(y_true, y_pred, average=average, zero_division=0),
    }

    # Add AUC-ROC for binary classification
    if len(np.unique(y_true)) == 2:
        try:
            metrics["auc_roc"] = roc_auc_score(y_true, y_pred)
        except ValueError:
            metrics["auc_roc"] = 0.0

    return metrics


def get_confusion_matrix(y_true: np.ndarray, y_pred: np.ndarray) -> np.ndarray:
    """
    Get confusion matrix

    Args:
        y_true: Ground truth labels
        y_pred: Predicted labels

    Returns:
        Confusion matrix as numpy array
    """
    return confusion_matrix(y_true, y_pred)


def plot_confusion_matrix(
    cm: np.ndarray,
    class_names: List[str],
    title: str = "Confusion Matrix",
    save_path: Optional[Path] = None,
    figsize: Tuple[int, int] = (8, 6),
) -> plt.Figure:
    """
    Plot confusion matrix as heatmap

    Args:
        cm: Confusion matrix
        class_names: List of class names
        title: Plot title
        save_path: Path to save figure (optional)
        figsize: Figure size

    Returns:
        Matplotlib figure
    """
    fig, ax = plt.subplots(figsize=figsize)

    sns.heatmap(
        cm,
        annot=True,
        fmt="d",
        cmap="Blues",
        xticklabels=class_names,
        yticklabels=class_names,
        ax=ax,
    )

    ax.set_xlabel("Predicted Label")
    ax.set_ylabel("True Label")
    ax.set_title(title)

    plt.tight_layout()

    if save_path:
        save_path = Path(save_path)
        save_path.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(save_path, dpi=150, bbox_inches="tight")
        print(f"Confusion matrix saved to: {save_path}")

    return fig


def plot_training_history(
    history: Dict[str, List[float]],
    title: str = "Training History",
    save_path: Optional[Path] = None,
    figsize: Tuple[int, int] = (12, 4),
) -> plt.Figure:
    """
    Plot training and validation loss/accuracy curves

    Args:
        history: Dictionary with 'train_loss', 'val_loss', 'train_acc', 'val_acc' lists
        title: Plot title
        save_path: Path to save figure (optional)
        figsize: Figure size

    Returns:
        Matplotlib figure
    """
    fig, axes = plt.subplots(1, 2, figsize=figsize)
    epochs = range(1, len(history["train_loss"]) + 1)

    # Loss plot
    axes[0].plot(epochs, history["train_loss"], "b-", label="Training Loss")
    axes[0].plot(epochs, history["val_loss"], "r-", label="Validation Loss")
    axes[0].set_xlabel("Epoch")
    axes[0].set_ylabel("Loss")
    axes[0].set_title("Training and Validation Loss")
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)

    # Accuracy plot
    axes[1].plot(epochs, history["train_acc"], "b-", label="Training Accuracy")
    axes[1].plot(epochs, history["val_acc"], "r-", label="Validation Accuracy")
    axes[1].set_xlabel("Epoch")
    axes[1].set_ylabel("Accuracy")
    axes[1].set_title("Training and Validation Accuracy")
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)

    plt.suptitle(title, fontsize=14)
    plt.tight_layout()

    if save_path:
        save_path = Path(save_path)
        save_path.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(save_path, dpi=150, bbox_inches="tight")
        print(f"Training history plot saved to: {save_path}")

    return fig


def print_classification_report(
    y_true: np.ndarray, y_pred: np.ndarray, class_names: List[str]
) -> str:
    """
    Print and return classification report

    Args:
        y_true: Ground truth labels
        y_pred: Predicted labels
        class_names: List of class names

    Returns:
        Classification report as string
    """
    report = classification_report(y_true, y_pred, target_names=class_names, digits=4)
    print("\nClassification Report:")
    print("=" * 60)
    print(report)
    print("=" * 60)
    return report


def save_metrics_json(metrics: Dict[str, float], save_path: Path) -> None:
    """
    Save metrics to JSON file

    Args:
        metrics: Dictionary of metrics
        save_path: Path to save JSON file
    """
    import json

    save_path = Path(save_path)
    save_path.parent.mkdir(parents=True, exist_ok=True)

    with open(save_path, "w") as f:
        json.dump(metrics, f, indent=2)

    print(f"Metrics saved to: {save_path}")


if __name__ == "__main__":
    # Test metrics utilities
    print("Testing metrics utilities...")

    # Sample data
    y_true = np.array([0, 0, 1, 1, 0, 1, 0, 1])
    y_pred = np.array([0, 0, 1, 0, 0, 1, 1, 1])
    class_names = ["cat", "dog"]

    # Calculate metrics
    metrics = calculate_metrics(y_true, y_pred)
    print("\nMetrics:")
    for name, value in metrics.items():
        print(f"  {name}: {value:.4f}")

    # Confusion matrix
    cm = get_confusion_matrix(y_true, y_pred)
    print(f"\nConfusion Matrix:\n{cm}")

    # Classification report
    print_classification_report(y_true, y_pred, class_names)

    print("\nMetrics utilities test complete!")



