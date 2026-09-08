from loader import DataLoader
from recommender import Recommender

loader = DataLoader()
loader.load()

recommender = Recommender(loader)

results = recommender.recommend_from_image(0)

for image in results:

    print(image)