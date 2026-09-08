import pandas as pd

metadata = pd.read_csv("../ml/embeddings/metadata.csv")

print(metadata.columns)
print(metadata.head())