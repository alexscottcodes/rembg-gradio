# Use a lightweight Python base
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    GRADIO_SERVER_NAME="0.0.0.0"

# Install system dependencies
# libgl1: Replacement for libgl1-mesa-glx on newer Debian/Ubuntu systems
# libglib2.0-0: Required by OpenCV
# libgomp1: Required for ONNX Runtime
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Create a dedicated directory for model cache to ensure permissions work
ENV U2NET_HOME=/app/.u2net

# Copy application code
COPY . .

# Create outputs directory
RUN mkdir -p outputs .u2net

# Expose Gradio port
EXPOSE 7860

# Run the application
CMD ["python", "app.py"]