import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image
import numpy as np

# The 14 diseases the NIH CheXNet dataset covers
CLASSES = [
    "Atelectasis", "Cardiomegaly", "Effusion", "Infiltration",
    "Mass", "Nodule", "Pneumonia", "Pneumothorax", "Consolidation",
    "Edema", "Emphysema", "Fibrosis", "Pleural_Thickening", "Hernia"
]

def load_model():
    # Load ResNet50 — same architecture you've seen at USC
    model = models.resnet50(weights="IMAGENET1K_V1")
    
    # Replace the last layer: ImageNet has 1000 classes, we need 14
    model.fc = nn.Linear(model.fc.in_features, len(CLASSES))
    
    # Set to eval mode — turns off dropout/batchnorm training behavior
    model.eval()
    return model

def preprocess_image(image_bytes):
    # This is the standard ImageNet normalization — same values used in your USC work
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(
            mean=[0.485, 0.456, 0.406],
            std=[0.229, 0.224, 0.225]
        )
    ])
    image = Image.open(image_bytes).convert("RGB")
    return transform(image).unsqueeze(0)  # Add batch dimension: [1, 3, 224, 224]

def predict(model, image_tensor):
    with torch.no_grad():  # No gradient tracking needed for inference
        outputs = model(image_tensor)
        # Sigmoid because this is multi-label (patient can have multiple conditions)
        probs = torch.sigmoid(outputs).squeeze().numpy()
    
    results = []
    for i, prob in enumerate(probs):
        results.append({
            "condition": CLASSES[i],
            "confidence": round(float(prob), 3)
        })
    
    # Sort by confidence, highest first
    results.sort(key=lambda x: x["confidence"], reverse=True)
    return results

def get_triage(results):
    top_confidence = results[0]["confidence"]
    if top_confidence >= 0.85:
        return "URGENT"
    elif top_confidence >= 0.60:
        return "MONITOR"
    else:
        return "ROUTINE"