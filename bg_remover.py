import rembg
import numpy as np
from PIL import Image
import onnxruntime as ort
import os

# Create a session globally to avoid reloading the model on every request
# rembg handles session caching, but explicit management is safer for metrics
session = rembg.new_session("u2net")

def estimate_flops(width: int, height: int, model_name: str = "u2net") -> str:
    """
    Provides a theoretical estimate of FLOPs for the U-2-Net architecture.
    Note: Real-world FLOPs depend on the specific ONNX runtime optimizations and hardware instructions.
    
    Standard U-2-Net operates on 320x320 inputs internally, but pre/post processing 
    scales with image size.
    """
    # U-2-Net is roughly 40-50 GFLOPs for a 320x320 input.
    # We will provide a static estimate for the model pass + a linear component for pixel-wise operations.
    
    # Base GFLOPs for U-2-Net (approximate)
    model_gflops = 45.0 
    
    # Pixel operations (composition, resizing, alpha matting)
    # Estimate: ~500 FLOPs per pixel for high-quality resizing and alpha compositing
    pixel_ops = (width * height * 500) / 1e9
    
    total_gflops = model_gflops + pixel_ops
    return f"{total_gflops:.2f} GFLOPs (Theoretical)"

def process_image(input_image: Image.Image, progress_callback=None) -> Image.Image:
    """
    Removes background from a PIL Image.
    """
    if progress_callback:
        progress_callback(0.3, "Preprocessing image...")
    
    # rembg doesn't expose a per-step callback for single inference,
    # so we wrap the main call.
    
    if progress_callback:
        progress_callback(0.5, "Running U-2-Net Inference (CPU)...")
        
    # Run inference
    # alpha_matting=True improves edge quality but is slower
    output_image = rembg.remove(
        input_image, 
        session=session,
        alpha_matting=True,
        alpha_matting_foreground_threshold=240,
        alpha_matting_background_threshold=10,
        alpha_matting_erode=10
    )
    
    if progress_callback:
        progress_callback(0.8, "Post-processing mask...")
        
    return output_image