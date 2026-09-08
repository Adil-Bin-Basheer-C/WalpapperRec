from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
from pathlib import Path
from loader import DataLoader
from recommender import Recommender
from models import ImageRequest, PreferenceRequest
from fastapi.middleware.cors import CORSMiddleware
import random

app = FastAPI(title="Wallpaper Recommendation API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
BASE_DIR = Path(__file__).resolve().parent
DATASET_DIR = BASE_DIR.parent / "ml" / "dataset"

app.mount(
    "/images",
    StaticFiles(directory=DATASET_DIR),
    name="images"
)

print("Loading recommendation engine...")

loader = DataLoader()
loader.load()

recommender = Recommender(loader)

print("Recommendation engine ready!")

image_map = {
    int(row["image_id"]): row
    for _, row in recommender.loader.metadata.iterrows()
}

@app.get("/")
def home():

    return {
        "message": "Wallpaper Recommendation API is running!"
    }


@app.get("/recommend/random")

def random_recommendations(top_k: int = 10):
    return recommender.random_recommendations(top_k=top_k)

@app.post("/recommend/image")
def recommend(request: ImageRequest):

    return recommender.recommend_from_image(
        request.image_id,
        request.top_k
    )
@app.post("/recommend/preferences")
def recommend_preferences(request: PreferenceRequest):

    return recommender.recommend_from_preferences(
        request.liked,
        request.disliked,
        request.shown,
        request.top_k
    )


@app.get("/download/{image_id}")
def download_image(image_id: int):

    image = image_map.get(image_id)

    if image is None:
        return {"error": "Image not found"}

    relative_path = image["path"].replace("\\", "/")
    relative_path = relative_path.replace("../dataset/", "")

    path = DATASET_DIR / relative_path

    return FileResponse(
        path=path,
        filename=image["filename"],
        media_type="application/octet-stream"
    )