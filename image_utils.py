import os
from PIL import Image
import pillow_heif
import pillow_avif  # Registers AVIF support automatically on import

# Register HEIF opener
pillow_heif.register_heif_opener()

SUPPORTED_FORMATS = [
    "PNG", "JPEG", "JPG", "TIFF", "AVIF", "WEBP", "BMP", "HEIC", "HEIF"
]

def save_image(image: Image.Image, output_format: str, output_dir: str = "outputs") -> str:
    """
    Saves the PIL image to the specified format and returns the file path.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Clean up format string
    fmt = output_format.upper().strip()
    if fmt == "JPG":
        fmt = "JPEG"
    
    filename = f"output_{os.urandom(4).hex()}.{output_format.lower()}"
    filepath = os.path.join(output_dir, filename)

    # Handle formats that don't support transparency (Alpha channel)
    if fmt in ["JPEG", "BMP"] and image.mode == "RGBA":
        # Composite over white background
        background = Image.new("RGB", image.size, (255, 255, 255))
        background.paste(image, mask=image.split()[3]) # 3 is the alpha channel
        image = background

    save_kwargs = {}
    
    # Format specific optimizations
    if fmt == "WEBP":
        save_kwargs["quality"] = 90
        save_kwargs["method"] = 6
    elif fmt == "JPEG":
        save_kwargs["quality"] = 95
        save_kwargs["optimize"] = True
    elif fmt == "PNG":
        save_kwargs["optimize"] = True
    elif fmt in ["HEIC", "HEIF"]:
        # pillow_heif handles the saving via the standard save method once registered,
        # but we need to ensure the format string is correct for PIL to pick up the plugin.
        # usually 'HEIF' is the format identifier for PIL save
        fmt = "HEIF" 
        save_kwargs["quality"] = 90

    try:
        image.save(filepath, format=fmt, **save_kwargs)
    except Exception as e:
        # Fallback for complex format errors
        print(f"Error saving as {fmt}: {e}")
        # Try generic save
        image.save(filepath)

    return filepath