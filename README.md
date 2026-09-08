# Personalized Wallpaper Recommendation System

A personalized wallpaper recommendation system built using **CLIP image embeddings, FAISS similarity search, FastAPI, and React**.

The system recommends wallpapers based on the user's likes and dislikes while also maintaining recommendation diversity.

## Features

* 🖼️ Wallpaper browsing
* 👍 Like wallpapers
* 👎 Dislike wallpapers
* 🎯 Personalized recommendations
* 🔍 Image similarity search using CLIP
* ⚡ Fast similarity search using FAISS
* 🔄 Random recommendations for cold-start users
* 🌈 Diverse recommendations to reduce repetitive results
* 🚫 Avoids previously shown, liked, and disliked images
* ⬇️ Wallpaper download option
* ❤️ View liked wallpapers
* 🌐 React frontend
* 🚀 FastAPI backend

## System Architecture

```text
                    Wallpaper Dataset
                           │
                           ▼
                    CLIP Image Model
                           │
                           ▼
                   Image Embeddings
                           │
                           ▼
                         FAISS
                    Similarity Index
                           │
                           ▼
                  Recommendation Engine
                           │
                    ┌──────┴──────┐
                    │             │
                Likes/Dislikes   History
                    │             │
                    └──────┬──────┘
                           ▼
                   Personalized Results
                           │
                           ▼
                    FastAPI Backend
                           │
                           ▼
                     React Frontend
```

## Technologies Used

### Frontend

* React
* Vite
* JavaScript
* CSS
* Axios

### Backend

* Python
* FastAPI
* Uvicorn
* NumPy
* Pandas
* FAISS

### Machine Learning

* OpenAI CLIP (`clip-vit-base-patch32`)
* PyTorch
* 512-dimensional image embeddings

## Recommendation Approach

### 1. CLIP Embeddings

Each wallpaper is converted into a numerical vector using CLIP.

```text
Image
  ↓
CLIP
  ↓
512-dimensional embedding
```

Similar images have similar embeddings in the vector space.

### 2. FAISS Search

The embeddings are stored in a FAISS index.

When a user likes an image, its embedding is used to find visually similar wallpapers.

### 3. Multiple User Interests

Instead of calculating the mean of all liked images, the system searches separately from each liked wallpaper.

For example:

```text
Liked:
    Nature
    Cars
    Anime

        ↓

Nature → similar candidates
Cars   → similar candidates
Anime  → similar candidates

        ↓

Combine candidates
        ↓
Keep best similarity score
        ↓
Apply diversity filtering
        ↓
Final recommendations
```

This prevents one category from dominating simply because the user has more likes from that category.

### 4. Candidate Scoring

If the same candidate is found from multiple liked images, the system keeps its highest similarity score.

```python
candidate_scores[idx] = max(
    candidate_scores[idx],
    similarity
)
```

This allows a wallpaper to be recommended when it strongly matches **at least one** of the user's interests.

### 5. Diversity Filtering

Highly similar recommendations are removed to avoid showing almost identical wallpapers.

For example:

```text
Mountain 1
Mountain 2  ← removed if too similar
Mountain 3  ← removed if too similar
Car
Space
```

The result contains more visual variety.

### 6. Dislike Filtering

Wallpapers that are highly similar to disliked wallpapers are rejected.

```text
Disliked image
      ↓
Compare candidate embedding
      ↓
Similarity > threshold?
      ↓
Yes → Reject
No  → Keep
```

### 7. Random Recommendations

When the user has no likes, the system uses random recommendations.

Random candidates are filtered using the user's disliked images and the diversity mechanism.

This provides a **cold-start solution** when there is not enough user preference information.

## Project Structure

```text
project/
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Header.jsx
│   │   │   ├── ImageCard.jsx
│   │   │   └── ImageGrid.jsx
│   │   │
│   │   ├── services/
│   │   │   └── api.js
│   │   │
│   │   ├── App.jsx
│   │   └── App.css
│   │
│   └── package.json
│
├── backend/
│   ├── main.py
│   ├── models.py
│   ├── recommender.py
│   ├── loader.py
│   ├── requirements.txt
│   └── venv/
│
├── ml/
│   ├── scripts/
│   │   └── generate_embeddings.py
│   │
│   ├── embeddings/
│   │   ├── embeddings.npy
│   │   └── metadata.csv
│   │
│   └── indexes/
│       └── wallpapers.index
│
├── dataset/
│   └── wallpaper images
│
└── README.md
```

> **Note:** The actual dataset, generated embeddings, FAISS index, API keys, and virtual environment should generally not be uploaded to GitHub.

## Installation

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd <project-folder>
```

### 2. Backend

Create a virtual environment:

```bash
python -m venv venv
```

Activate it on Windows:

```powershell
.\venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the backend:

```bash
uvicorn main:app --reload
```

The API will run at:

```text
http://127.0.0.1:8000
```

### 3. Frontend

Install dependencies:

```bash
npm install
```

Start the React development server:

```bash
npm run dev
```

The frontend will normally be available at:

```text
http://localhost:5173
```

## Generating Embeddings

If the dataset is changed, regenerate the embeddings.

```bash
cd ml/scripts
python generate_embeddings.py
```

This generates:

```text
ml/embeddings/embeddings.npy
ml/embeddings/metadata.csv
```

The FAISS index should then be regenerated from the new embeddings.

## Configuration

API keys should **not** be hard-coded or uploaded to GitHub.

For example:

```python
API_KEY = "YOUR_PEXELS_API_KEY"
```

Use an environment variable or a local configuration file that is included in `.gitignore`.

## Dataset

The project uses wallpaper images obtained through the Pexels API.

The dataset can contain different types of wallpapers such as:

* Nature
* Cars
* Space
* Abstract
* Architecture
* Animals
* Anime
* Other wallpaper categories

The recommendation system does not depend on manually assigned categories for its similarity calculations. CLIP embeddings are used to represent visual characteristics.

## Important GitHub Files

Create a `.gitignore` file before uploading:

```gitignore
# Python
__pycache__/
*.pyc
venv/

# Environment variables
.env

# Dataset
dataset/

# Generated ML files
ml/embeddings/
ml/indexes/

# Node
node_modules/
dist/

# IDE
.vscode/
.idea/
```



unless you specifically want them in the repository and understand the storage/security implications.

## Future Improvements

Possible future improvements include:

* User-based recommendation history
* Download-based preference weighting
* Better exploration strategies
* Adaptive similarity thresholds
* More advanced diversity-aware sampling
* Multi-user personalization
* Recommendation evaluation metrics
* Feedback-based ranking

## License

This project is intended for educational and academic purposes.
