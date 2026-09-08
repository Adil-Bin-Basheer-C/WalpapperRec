from pydantic import BaseModel


class Recommendation(BaseModel):
    image_id: int
    filename: str
    path: str
    similarity: float


class ImageRequest(BaseModel):
    image_id: int
    top_k: int = 10

class PreferenceRequest(BaseModel):
    liked: list[int]
    disliked: list[int] = []
    shown: list[int] = []
    top_k: int = 10