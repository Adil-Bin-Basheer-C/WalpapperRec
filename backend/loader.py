import os

import faiss
import numpy as np
import pandas as pd


# -----------------------------
# Paths
# -----------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

ML_DIR = os.path.join(BASE_DIR, "..", "ml")

EMBEDDINGS_PATH = os.path.join(
    ML_DIR,
    "embeddings",
    "embeddings.npy"
)

METADATA_PATH = os.path.join(
    ML_DIR,
    "embeddings",
    "metadata.csv"
)

INDEX_PATH = os.path.join(
    ML_DIR,
    "indexes",
    "wallpapers.index"
)


class DataLoader:

    def __init__(self):

        self.embeddings = None
        self.metadata = None
        self.index = None

    def load(self):

        print("Loading embeddings...")

        self.embeddings = np.load(
            EMBEDDINGS_PATH
        ).astype(np.float32)

        print("Loading metadata...")

        self.metadata = pd.read_csv(
            METADATA_PATH
        )

        print("Loading FAISS index...")

        self.index = faiss.read_index(
            INDEX_PATH
        )

        print()

        print("Data loaded successfully!")

        print("Embeddings :", self.embeddings.shape)

        print("Metadata :", len(self.metadata))

        print("FAISS vectors :", self.index.ntotal)