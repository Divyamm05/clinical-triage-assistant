from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import io

from model import load_model, preprocess_image, predict, get_triage
from gradcam import generate_heatmap

# Lifespan: load model once when server starts, reuse for every request
# Loading it on every request would take 2-3 seconds each time — bad UX
@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.model = load_model()
    print("Model loaded and ready!")
    yield  # Server runs here
    print("Shutting down...")

app = FastAPI(title="Clinical Triage Assistant", lifespan=lifespan)

# CORS: allows your React frontend (localhost:5173) to talk to this backend (localhost:8000)
# Without this, the browser blocks cross-origin requests — a very common gotcha
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"status": "Clinical Triage Assistant is running"}

@app.post("/predict")
async def predict_endpoint(file: UploadFile = File(...)):
    # Read uploaded file into memory as bytes
    contents = await file.read()
    image_bytes = io.BytesIO(contents)
    
    # Run prediction
    model = app.state.model
    image_tensor = preprocess_image(image_bytes)
    results = predict(model, image_tensor)
    triage = get_triage(results)
    
    # Generate GradCAM heatmap
    image_bytes.seek(0)  # Reset pointer — we need to read the image again
    heatmap_b64 = generate_heatmap(model, image_bytes)
    
    return {
        "predictions": results[:5],  # Top 5 conditions
        "triage": triage,
        "heatmap": heatmap_b64
    }