import faiss
import numpy as np
import pandas as pd

EMBEDDINGS_FILE = "../embeddings/embeddings.npy"
METADATA_FILE = "../embeddings/metadata.csv"
INDEX_FILE = "../indexes/wallpapers.index"

TOP_K = 10


def main():

    embeddings = np.load(EMBEDDINGS_FILE).astype(np.float32)

    metadata = pd.read_csv(METADATA_FILE)

    index = faiss.read_index(INDEX_FILE)

    image_id = int(input("Enter image id: "))

    query = embeddings[image_id].reshape(1, -1)

    similarities, indices = index.search(query, TOP_K + 1)

    print("\nMost Similar Wallpapers\n")

    for score, idx in zip(similarities[0], indices[0]):

        if idx == image_id:
            continue

        print(f"Image ID : {idx}")
        print(f"Similarity : {score:.4f}")
        print(f"Path : {metadata.iloc[idx]['path']}")
        print("-" * 50)


if __name__ == "__main__":
    main()