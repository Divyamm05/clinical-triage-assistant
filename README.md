---
title: Clinical Triage Assistant
emoji: 🏥
colorFrom: blue
colorTo: indigo
sdk: docker
pinned: false
---

# 🏥 Clinical Triage Assistant
AI-powered chest X-ray analysis with explainability, built with PyTorch, FastAPI, and React.

## Features
- Upload a chest X-ray and get AI-predicted diagnoses with confidence scores
- GradCAM heatmap highlighting regions of concern
- Triage priority: URGENT / MONITOR / ROUTINE

## Tech Stack
- **Frontend:** React + Tailwind CSS
- **Backend:** FastAPI + Python
- **ML Model:** ResNet50 fine-tuned on NIH ChestX-ray14 (14 pathologies)
- **Explainability:** GradCAM via pytorch-grad-cam

## Run Locally
```bash
# Backend
cd backend && pip install -r requirements.txt
uvicorn main:app --reload

# Frontend
cd frontend && npm install && npm run dev
```

## Disclaimer
For research purposes only. Not a substitute for clinical diagnosis.
