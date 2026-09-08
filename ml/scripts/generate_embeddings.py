import os
import csv
import numpy as np
from PIL import Image
from tqdm import tqdm

import torch
from transformers import CLIPProcessor, CLIPModel

# -----------------------------
# Configuration
# -----------------------------

DATASET_DIR = "../dataset"

print(os.path.abspath(DATASET_DIR))

OUTPUT_DIR = "../embeddings"

EMBEDDING_FILE = os.path.join(OUTPUT_DIR, "embeddings.npy")
METADATA_FILE = os.path.join(OUTPUT_DIR, "metadata.csv")

BATCH_SIZE = 32

SUPPORTED_EXTENSIONS = (
    ".jpg",
    ".jpeg",
    ".png",
    ".bmp",
    ".webp"
)

# -----------------------------
# Device
# -----------------------------

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

print(f"\nUsing device : {device}")

# -----------------------------
# Load CLIP
# -----------------------------

model = CLIPModel.from_pretrained(
    "openai/clip-vit-base-patch32"
).to(device)

processor = CLIPProcessor.from_pretrained(
    "openai/clip-vit-base-patch32"
)

model.eval()

# -----------------------------
# Collect image paths
# -----------------------------

image_paths = []

for root, _, files in os.walk(DATASET_DIR):

    for file in files:

        if file.lower().endswith(SUPPORTED_EXTENSIONS):

            image_paths.append(
                os.path.join(root, file)
            )

image_paths.sort()

print(f"Found {len(image_paths)} images.")

# -----------------------------
# Prepare output directory
# -----------------------------

os.makedirs(OUTPUT_DIR, exist_ok=True)

metadata = []

all_embeddings = []

image_id = 0

# -----------------------------
# Batch Processing
# -----------------------------

for start in tqdm(range(0, len(image_paths), BATCH_SIZE)):

    batch_paths = image_paths[start:start+BATCH_SIZE]

    images = []

    valid_paths = []

    for path in batch_paths:

        try:

            image = Image.open(path).convert("RGB")

            images.append(image)

            valid_paths.append(path)

        except Exception:

            continue

    if len(images) == 0:

        continue

    inputs = processor(
        images=images,
        return_tensors="pt",
        padding=True
    )

    inputs = {
        k: v.to(device)
        for k, v in inputs.items()
    }

    with torch.no_grad():

        embeddings = model.get_image_features(**inputs)

        embeddings = torch.nn.functional.normalize(
            embeddings,
            p=2,
            dim=1
        )

    embeddings = embeddings.cpu().numpy()

    for emb, path in zip(embeddings, valid_paths):

        all_embeddings.append(emb)

        metadata.append([
            image_id,
            os.path.basename(path),
            path
        ])

        image_id += 1

# -----------------------------
# Save embeddings
# -----------------------------

all_embeddings = np.array(
    all_embeddings,
    dtype=np.float32
)

np.save(
    EMBEDDING_FILE,
    all_embeddings
)

# -----------------------------
# Save metadata
# -----------------------------

with open(
    METADATA_FILE,
    "w",
    newline="",
    encoding="utf-8"
) as f:

    writer = csv.writer(f)

    writer.writerow([
        "image_id",
        "filename",
        "path"
    ])

    writer.writerows(metadata)

print()

print("Finished!")

print(f"Embeddings shape : {all_embeddings.shape}")

print(f"Saved embeddings to : {EMBEDDING_FILE}")

print(f"Saved metadata to   : {METADATA_FILE}")