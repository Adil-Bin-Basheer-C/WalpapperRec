
#disliked effect tharnilla
#oombiya alg..cluster cheyyanam
from loader import DataLoader
import numpy as np
import random
class Recommender:
    def __init__(self, loader: DataLoader):
        self.loader = loader
    def get_embedding(self, image_id: int):
        return self.loader.embeddings[image_id]
    def search(self, query_vector, top_k=10):
        query_vector = query_vector.reshape(1, -1)
        similarities, indices = self.loader.index.search(
            query_vector,
            top_k + 1
        )
        return similarities[0], indices[0]

    
    def random_recommendations(
        self,
        excluded=None,
        disliked=None,
        top_k=10
    ):
        if excluded is None:
            excluded = set()

        if disliked is None:
            disliked = []

        available_ids = [
            idx
            for idx in range(len(self.loader.metadata))
            if idx not in excluded
        ]

        if not available_ids:
            return []

        pool_size = min(500, len(available_ids))

        random_ids = random.sample(
            available_ids,
            pool_size
        )

        filtered_ids = []

        for idx in random_ids:

            candidate_embedding = self.get_embedding(idx)

            rejected = False

            for disliked_id in disliked:

                disliked_embedding = self.get_embedding(
                    disliked_id
                )

                similarity = np.dot(
                    candidate_embedding,
                    disliked_embedding
                )

                if similarity > 0.75:
                    rejected = True
                    break

            if not rejected:
                filtered_ids.append(idx)

        random.shuffle(filtered_ids)
        similarities = [0] * len(filtered_ids)
        return self.diverse_recommendations(
            similarities,
            filtered_ids,
            excluded,
            top_k
        )


    def diverse_recommendations(self, similarities, indices, excluded, top_k=10):

        recommendations = []

        threshold = 0.85

        for similarity, idx in zip(similarities, indices):

  

            candidate_embedding = self.loader.embeddings[idx]

            too_similar = False

            for recommendation in recommendations:

                selected_embedding = self.loader.embeddings[
                    recommendation["image_id"]
                ]

                similarity_between = np.dot(
                    candidate_embedding,
                    selected_embedding
                )

                if similarity_between > threshold:
                    too_similar = True
                    break

            if too_similar:
                continue

            image = self.loader.metadata.iloc[idx]

            path = image["path"].replace("\\", "/")
            path = path.replace("../dataset/", "")

            recommendations.append({

                "image_id": int(image["image_id"]),
                "filename": image["filename"],
                "image_url": f"http://127.0.0.1:8000/images/{path}",
                "similarity": float(similarity)

            })

            if len(recommendations) == top_k:
                break

        return recommendations
    
    def recommend_from_preferences(self,liked,disliked=None,shown=None,top_k=10):
        if disliked is None:
            disliked = []

        if shown is None:
            shown = []

        if len(liked) == 0:

            liked=[]

        excluded = set(liked)
        excluded.update(disliked)
        excluded.update(shown)

        if not liked:
            return self.random_recommendations(excluded,set(disliked))

        expl_count=min(2,top_k)
        pers_count=top_k-expl_count

        candidate_scores = {}

        search_k = 100



        for like in liked:

            user_vector = self.loader.embeddings[like].copy()

            if disliked:

                disliked_embeddings = self.loader.embeddings[disliked]

                disliked_vector = np.mean(
                    disliked_embeddings,
                    axis=0
                )

                user_vector = user_vector - 0.3 * disliked_vector

            norm = np.linalg.norm(user_vector)

            if norm != 0:
                user_vector = user_vector / norm

            similarities, indices = self.search(
                user_vector,
                search_k
            )

            for similarity, idx in zip(similarities, indices):

                if idx in excluded:
                    continue

                if idx not in candidate_scores:
                    candidate_scores[idx] = similarity
                else:
                    candidate_scores[idx] = max(
                        candidate_scores[idx],
                        similarity
                    )
        sorted_candidates = sorted(
            candidate_scores.items(),
            key=lambda x: x[1],
            reverse=True
        )

        indices = [idx for idx, _ in sorted_candidates]

        similarities = [score for _, score in sorted_candidates]

        pers= self.diverse_recommendations(
            similarities,
            indices,
            excluded,
            pers_count
        )

        for pers_image in pers:
            excluded.add(pers_image["image_id"])
        expl=self.random_recommendations(excluded,set(disliked),expl_count)

        return pers+expl

    def recommend_from_image(self, image_id: int, top_k=10):

        embedding = self.get_embedding(image_id)

        similarities, indices = self.search(
            embedding,
            top_k
        )

        recommendations = []

        for similarity, idx in zip(similarities, indices):

            if idx == image_id:
                continue

            image = self.loader.metadata.iloc[idx]

            path = image["path"].replace("\\", "/")
            path = path.replace("../dataset/", "")

            recommendations.append({
                "image_id": int(image["image_id"]),
                "filename": image["filename"],
                "image_url": f"http://127.0.0.1:8000/images/{path}",
                "similarity": float(similarity)
            })

        return recommendations
    
    