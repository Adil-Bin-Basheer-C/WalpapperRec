from PIL import Image
from transformers import CLIPProcessor, CLIPModel
import torch

# Select device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print("Device:", device)

# Load CLIP model and processor
model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32").to(device)
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

# Load image
image = Image.open("../dataset/trainA/trainA/2.jpg").convert("RGB")

# Preprocess image
inputs = processor(images=image, return_tensors="pt")

# Move tensors to GPU
inputs = {k: v.to(device) for k, v in inputs.items()}

# Extract image embedding
with torch.no_grad():
    embedding = model.get_image_features(**inputs)

# L2 Normalize
embedding = torch.nn.functional.normalize(embedding, p=2, dim=1)

print("Embedding shape:", embedding.shape)
print("First 10 values:")
print(embedding[0][:10])