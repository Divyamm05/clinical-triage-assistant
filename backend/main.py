from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from contextlib import asynccontextmanager
import io
import os

from model import load_model, preprocess_image, predict, get_triage
from gradcam import generate_heatmap

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.model = load_model()
    print("Model loaded and ready!")
    yield
    print("Shutting down...")

app = FastAPI(title="Clinical Triage Assistant", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/predict")
async def predict_endpoint(file: UploadFile = File(...)):
    contents = await file.read()
    image_bytes = io.BytesIO(contents)

    model = app.state.model
    image_tensor = preprocess_image(image_bytes)
    results = predict(model, image_tensor)
    triage = get_triage(results)

    image_bytes.seek(0)
    heatmap_b64 = generate_heatmap(model, image_bytes)

    return {
        "predictions": results[:5],
        "triage": triage,
        "heatmap": heatmap_b64
    }

# Serve React frontend — only active when built (i.e. on HuggingFace)
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    app.mount("/assets", StaticFiles(directory=f"{static_dir}/assets"), name="assets")

    @app.get("/")
    def root():
        return FileResponse(os.path.join(static_dir, "index.html"))
else:
    @app.get("/")
    def root():
        return {"status": "Clinical Triage Assistant is running"}