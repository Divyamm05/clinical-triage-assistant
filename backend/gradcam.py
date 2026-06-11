import numpy as np
import torch
from torchvision import transforms
from pytorch_grad_cam import GradCAM
from pytorch_grad_cam.utils.image import show_cam_on_image
from PIL import Image
import io
import base64

def generate_heatmap(model, image_bytes):
    # Target the last conv layer in ResNet50 — deepest features, most semantic meaning
    target_layers = [model.layer4[-1]]
    
    # Preprocessing — same as model.py (consistency is important)
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(
            mean=[0.485, 0.456, 0.406],
            std=[0.229, 0.224, 0.225]
        )
    ])
    
    # We need two versions of the image:
    # 1. Tensor for the model
    # 2. Raw numpy array for the heatmap overlay
    image_bytes.seek(0)  # Reset file pointer before reading again
    pil_image = Image.open(image_bytes).convert("RGB")
    input_tensor = transform(pil_image).unsqueeze(0)
    
    # Raw image as float array (0-1 range) for overlay
    raw_image = np.array(pil_image.resize((224, 224))) / 255.0
    raw_image = raw_image.astype(np.float32)
    
    # Generate the CAM
    cam = GradCAM(model=model, target_layers=target_layers)
    grayscale_cam = cam(input_tensor=input_tensor)[0]  # Shape: (224, 224)
    
    # Overlay heatmap on original image
    visualization = show_cam_on_image(raw_image, grayscale_cam, use_rgb=True)
    
    # Convert to base64 so we can send it over the API as a string
    output_image = Image.fromarray(visualization)
    buffer = io.BytesIO()
    output_image.save(buffer, format="PNG")
    encoded = base64.b64encode(buffer.getvalue()).decode("utf-8")
    
    return encoded  # Frontend will render this as: <img src="data:image/png;base64,{encoded}">