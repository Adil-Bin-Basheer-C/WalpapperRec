import os
import faiss
import numpy as np


EMBEDDINGS_FILE = "../embeddings/embeddings.npy"
INDEX_DIR = "../indexes"
INDEX_FILE = os.path.join(INDEX_DIR, "wallpapers.index")


def main():

    print("Loading embeddings...")

    embeddings = np.load(EMBEDDINGS_FILE).astype(np.float32)

    print("Embeddings shape:", embeddings.shape)

    dimension = embeddings.shape[1]

    print("Embedding dimension:", dimension)

    os.makedirs(INDEX_DIR, exist_ok=True)

    # Exact cosine similarity search
    # Embeddings are already normalized, so
    # Inner Product == Cosine Similarity

    index = faiss.IndexFlatIP(dimension)

    print("Adding embeddings to FAISS...")

    index.add(embeddings)

    print("Total vectors:", index.ntotal)

    faiss.write_index(index, INDEX_FILE)

    print("\nDone!")

    print("Saved index to:", INDEX_FILE)


if __name__ == "__main__":
    main()