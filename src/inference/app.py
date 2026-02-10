"""
FastAPI Application for Cats vs Dogs Classification
"""
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from PIL import Image
import io
import time
import logging
from datetime import datetime
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent.parent))

from src.inference.predictor import CatDogPredictor
from src.utils.config import MODELS_DIR, API_HOST, API_PORT

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Cats vs Dogs Classifier API",
    description="Binary image classification API for pet adoption platform",
    version="1.0.0"
)

# Global predictor instance
predictor = None

# Request metrics
request_count = 0
total_inference_time = 0.0


@app.on_event("startup")
async def startup_event():
    """
    Initialize the model on startup
    """
    global predictor
    try:
        logger.info("Loading model...")
        model_path = MODELS_DIR / "best_model.pt"
        
        if not model_path.exists():
            logger.warning(f"Best model not found at {model_path}, trying final_model.pt")
            model_path = MODELS_DIR / "final_model.pt"
        
        predictor = CatDogPredictor(model_path=str(model_path))
        logger.info("Model loaded successfully!")
    except Exception as e:
        logger.error(f"Error loading model: {e}")
        raise


@app.get("/")
async def root():
    """
    Root endpoint
    """
    return {
        "message": "Cats vs Dogs Classifier API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "predict": "/predict",
            "metrics": "/metrics"
        }
    }


@app.get("/health")
async def health_check():
    """
    Health check endpoint
    """
    if predictor is None:
        return JSONResponse(
            status_code=503,
            content={
                "status": "unhealthy",
                "message": "Model not loaded"
            }
        )
    
    return {
        "status": "healthy",
        "model_loaded": True,
        "timestamp": datetime.now().isoformat()
    }


@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    global request_count, total_inference_time

    if predictor is None:
        raise HTTPException(status_code=503, detail="Model not loaded")

    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")

    # Step 1: Open image safely
    try:
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
    except Exception as e:
        logger.error(f"Invalid image file {file.filename}: {e}")
        raise HTTPException(status_code=400, detail=f"Invalid image file: {str(e)}")

    # Step 2: Run prediction
    try:
        start_time = time.time()
        result = predictor.predict(image, return_probs=True)
        inference_time = time.time() - start_time

        # Update metrics
        request_count += 1
        total_inference_time += inference_time

        # Add metadata
        result["inference_time_ms"] = round(inference_time * 1000, 2)
        result["timestamp"] = datetime.now().isoformat()

        logger.info(
            f"Prediction: {result['predicted_class']} "
            f"(confidence: {result['confidence']:.4f}, "
            f"time: {result['inference_time_ms']}ms)"
        )

        return result
    except Exception as e:
        logger.error(f"Error during prediction for {file.filename}: {e}")
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")



@app.get("/metrics")
async def get_metrics():
    """
    Get API metrics
    """
    avg_inference_time = (
        total_inference_time / request_count if request_count > 0 else 0
    )
    
    return {
        "total_requests": request_count,
        "average_inference_time_ms": round(avg_inference_time * 1000, 2),
        "total_inference_time_s": round(total_inference_time, 2),
        "model_loaded": predictor is not None
    }


@app.get("/model-info")
async def model_info():
    """
    Get model information
    """
    if predictor is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    return {
        "model_type": "Custom CNN",
        "input_size": "224x224",
        "classes": ["cat", "dog"],
        "device": str(predictor.device)
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=API_HOST, port=API_PORT)
