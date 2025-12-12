import gradio as gr
import os
from bg_remover import process_image, estimate_flops
from image_utils import save_image, SUPPORTED_FORMATS
from metrics import ResourceMonitor

def remove_background(image, output_format, progress=gr.Progress()):
    if image is None:
        return None, None, "Please upload an image."

    monitor = ResourceMonitor()
    
    with monitor:
        progress(0.1, desc="Initializing Resource Monitor...")
        
        # 1. Image Processing
        # We pass the progress object to the processor
        result_image = process_image(image, progress_callback=progress)
        
        progress(0.9, desc=f"Converting to {output_format}...")
        
        # 2. Save Image
        output_path = save_image(result_image, output_format)
        
        # 3. Capture Metrics
        metrics = monitor.measure()
        
    # 4. Calculate Theoretical FLOPs
    flops_str = estimate_flops(image.width, image.height)
    
    # Format Metrics String
    metrics_text = (
        f"### Performance Metrics\n"
        f"- **Processing Time:** {metrics.processing_time:.2f} seconds\n"
        f"- **Approx. Calculations:** {flops_str}\n"
        f"- **Peak CPU Usage:** {metrics.peak_cpu_percent}%\n"
        f"- **Peak RAM Usage:** {metrics.peak_ram_mb:.2f} MB"
    )
    
    # Return:
    # 1. Preview Image (Gradio handles PIL -> WebP for display efficiently)
    # 2. Download File Path
    # 3. Metrics Text
    return result_image, output_path, metrics_text

# Custom CSS for a cleaner look
custom_css = """
.gradio-container {
    font-family: 'IBM Plex Sans', sans-serif;
}
#download_btn {
    margin-top: 10px;
}
"""

with gr.Blocks(title="Neural Background Remover", css=custom_css, theme=gr.themes.Soft()) as app:
    gr.Markdown(
        """
        # 🖼️ Neural Background Remover
        Remove image backgrounds locally using CPU. 
        Supports export to **PNG, JPEG, HEIC, AVIF, WebP**, and more.
        """
    )
    
    with gr.Row():
        with gr.Column():
            input_img = gr.Image(
                label="Input Image", 
                type="pil", 
                sources=["upload", "clipboard", "webcam"]
            )
            format_dropdown = gr.Dropdown(
                choices=SUPPORTED_FORMATS, 
                value="PNG", 
                label="Output Format"
            )
            process_btn = gr.Button("Remove Background", variant="primary", size="lg")
            
        with gr.Column():
            # Gradio v5+ automatically optimizes image display
            output_preview = gr.Image(label="Preview (WebP)", type="pil", format="webp")
            output_file = gr.DownloadButton(label="Download High-Res Image", visible=False)
            metrics_display = gr.Markdown(label="Performance Stats")

    # Event binding
    def update_ui(image, fmt):
        # Wrapper to handle visibility logic
        preview, file_path, metrics = remove_background(image, fmt)
        return preview, file_path, gr.DownloadButton(value=file_path, visible=True), metrics

    process_btn.click(
        fn=update_ui,
        inputs=[input_img, format_dropdown],
        outputs=[output_preview, output_file, output_file, metrics_display]
    )

if __name__ == "__main__":
    # Ensure outputs directory exists
    os.makedirs("outputs", exist_ok=True)
    
    # Launch with file access allowed for the outputs folder
    app.launch(
        server_name="0.0.0.0", 
        server_port=7860,
        allowed_paths=["outputs"]
    )