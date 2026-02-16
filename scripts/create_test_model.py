"""
Create a test model for CI/CD pipeline testing
This generates untrained model weights for testing the inference pipeline
"""

import json
import sys
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent))

import torch  # noqa: E402

from src.models.cnn_model import get_model  # noqa: E402
from src.utils.config import MODELS_DIR, NUM_CLASSES  # noqa: E402


def create_test_model():
    """
    Create and save an untrained model for testing purposes
    """
    print("=" * 60)
    print("Creating Test Model for CI/CD")
    print("=" * 60)

    # Ensure models directory exists
    MODELS_DIR.mkdir(parents=True, exist_ok=True)

    # Create model
    print("\nCreating model architecture...")
    model = get_model(num_classes=NUM_CLASSES)

    # Count parameters
    total_params = sum(p.numel() for p in model.parameters())
    print(f"Total parameters: {total_params:,}")

    # Save as best_model.pt (checkpoint format)
    best_model_path = MODELS_DIR / "best_model.pt"
    torch.save(
        {
            "epoch": 0,
            "model_state_dict": model.state_dict(),
            "val_acc": 0.5,  # Random initialization
            "val_loss": 1.0,
        },
        best_model_path,
    )
    print(f"\n✓ Saved best_model.pt to: {best_model_path}")

    # Save as final_model.pt (state dict only)
    final_model_path = MODELS_DIR / "final_model.pt"
    torch.save(model.state_dict(), final_model_path)
    print(f"✓ Saved final_model.pt to: {final_model_path}")

    # Create metrics file
    metrics = {
        "accuracy": 0.5,
        "precision": 0.5,
        "recall": 0.5,
        "f1_score": 0.5,
        "test_accuracy": 0.5,
        "note": "Test model - not trained, random weights",
    }
    metrics_path = MODELS_DIR / "metrics.json"
    with open(metrics_path, "w") as f:
        json.dump(metrics, f, indent=2)
    print(f"✓ Saved metrics.json to: {metrics_path}")

    # Test model loading
    print("\nVerifying model can be loaded...")
    loaded_checkpoint = torch.load(best_model_path, map_location="cpu")
    test_model = get_model(num_classes=NUM_CLASSES)
    test_model.load_state_dict(loaded_checkpoint["model_state_dict"])

    # Test forward pass
    dummy_input = torch.randn(1, 3, 224, 224)
    output = test_model(dummy_input)
    print(f"✓ Forward pass successful: output shape {output.shape}")

    print("\n" + "=" * 60)
    print("Test model creation complete!")
    print("=" * 60)
    print("\nNote: This model has random weights and is for testing only.")
    print("For a trained model, run: python src/models/train.py")


if __name__ == "__main__":
    create_test_model()



