"""
Enhanced monitoring module for the inference service
"""
import logging
import time
from datetime import datetime
from functools import wraps
from pathlib import Path
import json
from typing import Dict, Any

# Configure logging
LOG_DIR = Path(__file__).parent.parent.parent / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

# Create logger
logger = logging.getLogger("mlops_monitor")
logger.setLevel(logging.INFO)

# File handler for application logs
app_log_file = LOG_DIR / f"app_{datetime.now().strftime('%Y%m%d')}.log"
file_handler = logging.FileHandler(app_log_file)
file_handler.setLevel(logging.INFO)

# Console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Formatter
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add handlers
logger.addHandler(file_handler)
logger.addHandler(console_handler)


class RequestLogger:
    """
    Logger for API requests and responses
    """
    
    def __init__(self, log_file: str = None):
        if log_file is None:
            log_file = LOG_DIR / f"requests_{datetime.now().strftime('%Y%m%d')}.json"
        self.log_file = Path(log_file)
    
    def log_request(self, request_data: Dict[str, Any]):
        """
        Log request data to file
        
        Args:
            request_data: Dictionary containing request information
        """
        with open(self.log_file, 'a') as f:
            json.dump(request_data, f)
            f.write('\n')


class PerformanceMonitor:
    """
    Monitor for tracking performance metrics
    """
    
    def __init__(self):
        self.metrics = {
            "request_count": 0,
            "total_inference_time": 0.0,
            "errors": 0,
            "predictions": {
                "cat": 0,
                "dog": 0
            }
        }
        self.metrics_file = LOG_DIR / "metrics.json"
    
    def record_request(self, inference_time: float, predicted_class: str, success: bool = True):
        """
        Record request metrics
        
        Args:
            inference_time: Time taken for inference
            predicted_class: Predicted class
            success: Whether request was successful
        """
        self.metrics["request_count"] += 1
        self.metrics["total_inference_time"] += inference_time
        
        if not success:
            self.metrics["errors"] += 1
        else:
            if predicted_class in self.metrics["predictions"]:
                self.metrics["predictions"][predicted_class] += 1
    
    def get_metrics(self) -> Dict[str, Any]:
        """
        Get current metrics
        
        Returns:
            Dictionary of metrics
        """
        avg_time = (
            self.metrics["total_inference_time"] / self.metrics["request_count"]
            if self.metrics["request_count"] > 0
            else 0
        )
        
        return {
            **self.metrics,
            "average_inference_time": avg_time,
            "error_rate": (
                self.metrics["errors"] / self.metrics["request_count"]
                if self.metrics["request_count"] > 0
                else 0
            )
        }
    
    def save_metrics(self):
        """
        Save metrics to file
        """
        with open(self.metrics_file, 'w') as f:
            json.dump(self.get_metrics(), f, indent=2)
    
    def reset_metrics(self):
        """
        Reset all metrics
        """
        self.metrics = {
            "request_count": 0,
            "total_inference_time": 0.0,
            "errors": 0,
            "predictions": {
                "cat": 0,
                "dog": 0
            }
        }


def log_prediction(func):
    """
    Decorator to log predictions
    """
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start_time = time.time()
        request_logger = RequestLogger()
        
        try:
            result = await func(*args, **kwargs)
            inference_time = time.time() - start_time
            
            # Log request
            log_data = {
                "timestamp": datetime.now().isoformat(),
                "inference_time_ms": inference_time * 1000,
                "predicted_class": result.get("predicted_class"),
                "confidence": result.get("confidence"),
                "success": True
            }
            request_logger.log_request(log_data)
            
            logger.info(
                f"Prediction: {result.get('predicted_class')} "
                f"(confidence: {result.get('confidence'):.4f}, "
                f"time: {inference_time*1000:.2f}ms)"
            )
            
            return result
            
        except Exception as e:
            inference_time = time.time() - start_time
            
            # Log error
            log_data = {
                "timestamp": datetime.now().isoformat(),
                "inference_time_ms": inference_time * 1000,
                "error": str(e),
                "success": False
            }
            request_logger.log_request(log_data)
            
            logger.error(f"Prediction error: {e}")
            raise
    
    return wrapper


# Global performance monitor instance
performance_monitor = PerformanceMonitor()


def get_logger():
    """
    Get the application logger
    
    Returns:
        Logger instance
    """
    return logger


def get_performance_monitor():
    """
    Get the performance monitor
    
    Returns:
        PerformanceMonitor instance
    """
    return performance_monitor
