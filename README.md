# **🖼️ Neural Background Remover**

A powerful, modular web application that removes image backgrounds using deep learning (U-2-Net). This app runs entirely on your CPU and provides detailed performance metrics for every image processed.

## **✨ Features**

* **Accurate Removal:** Uses the U-2-Net model with alpha matting for high-quality edge detection (great for hair and fur\!).  
* **Privacy First:** Runs locally on your machine. No images are uploaded to the cloud.  
* **Rich Feedback:**  
  * Real-time progress bars.  
  * **Performance Metrics:** See exactly how much RAM and CPU power the task took, plus a theoretical estimate of the calculations (FLOPs) performed.  
* **Wide Format Support:**  
  * Import/Export: **PNG, JPEG, WebP, BMP, TIFF**.  
  * Modern Formats: **HEIC** (iPhone photos) and **AVIF**.  
* **Dockerized:** Ready to deploy with a single container.

## **🚀 Quick Start (Docker)**

The easiest way to run the app is using Docker. This ensures all system libraries (like those needed for HEIC files) are installed correctly.

1. **Build the Image:**  
   docker build \-t bg-remover .

2. **Run the Container:**  
   docker run \-p 7860:7860 bg-remover

3. Open the App:  
   Go to http://localhost:7860 in your browser.

**Note:** The first time you run the app, it will download the U-2-Net AI model (approx. 170MB). This happens automatically.

## **🛠️ Local Installation (Python)**

If you prefer to run it without Docker, you'll need Python 3.10+ installed.

1. **Clone or Download the code.**  
2. Install System Dependencies (Linux only):  
   You need these for image processing libraries to work correctly.  
   sudo apt-get install libgl1-mesa-glx libglib2.0-0 libgomp1

3. **Install Python Requirements:**  
   pip install \-r requirements.txt

4. **Run the App:**  
   python app.py

## **📂 Project Structure**

We organized the code into separate files to make it easier to learn from and modify:

* **app.py**: The main entry point. It builds the Gradio interface and handles the "click" events.  
* **bg\_remover.py**: Contains the "Brain". It loads the AI model and estimates the math (FLOPs) required.  
* **image\_utils.py**: Handles the "Eyes" and "Hands". It opens complex files like HEIC and saves your results in the format you choose.  
* **metrics.py**: The "Stopwatch". It measures how fast your CPU is working and how much memory is being used.  
* **Dockerfile**: A recipe for building the computer environment needed to run the app.

## **📊 Understanding the Metrics**

After you process an image, the app displays three key stats:

1. **Processing Time:** How long the AI took to "think" and remove the background.  
2. **Peak RAM Usage:** The maximum amount of memory the app needed. Larger images \= more RAM.  
3. **Approx. Calculations (GFLOPs):** A "GigaFLOP" is one billion math operations. This number estimates how much math the computer did to understand your image.

## **📝 License**

This project utilizes the [Rembg](https://github.com/danielgatis/rembg) library. Please refer to their repository for specific licensing details regarding the U-2-Net model.