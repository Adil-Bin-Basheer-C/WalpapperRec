import { useEffect, useState } from "react";
import Header from "./components/Header";
import api from "./services/api";
import ImageGrid from "./components/ImageGrid";
import "./App.css";

function App() {

    const [votes, setVotes] = useState({});
    const [shown, setShown] = useState([]);
    const [images, setImages] = useState([]);
    const [likedImages, setLikedImages] = useState([]);
    const [showLiked, setShowLiked] = useState(false);
    const [loading, setLoading] = useState(false);

    function handleLike(id) {

        setVotes(prev => {

            const newVotes = { ...prev };

            if (newVotes[id] === "liked") {

                delete newVotes[id];

                setLikedImages(prevLiked =>
                    prevLiked.filter(img => img.image_id !== id)
                );

            }
            else {

                newVotes[id] = "liked";

                const img = images.find(x => x.image_id === id);

                if (img) {

                    setLikedImages(prevLiked => {

                        if (prevLiked.some(x => x.image_id === id))
                            return prevLiked;

                        return [...prevLiked, img];

                    });

                }

            }

            return newVotes;

        });

    }

    function handleDislike(id) {

        setVotes(prev => {

            const newVotes = { ...prev };

            if (newVotes[id] === "disliked") {

                delete newVotes[id];

            }
            else {

                newVotes[id] = "disliked";

                setLikedImages(prevLiked =>
                    prevLiked.filter(img => img.image_id !== id)
                );

            }

            return newVotes;

        });

    }

    async function loadRecommendations() {

        setLoading(true);

        try {

            const liked = Object.keys(votes)
                .filter(id => votes[id] === "liked")
                .map(Number);

            const disliked = Object.keys(votes)
                .filter(id => votes[id] === "disliked")
                .map(Number);

            const response = await api.post("/recommend/preferences", {

                liked,
                disliked,
                shown,
                top_k: 10
            });

            setImages(response.data);

            setShown(prev => [

                ...prev,
                ...response.data.map(img => img.image_id)

            ]);

            setShowLiked(false);

        }
        catch (error) {

            console.error(error);

        }
        finally {

            setLoading(false);

        }

    }

    useEffect(() => {

        async function loadImages() {

            try {

                const response = await api.get("/recommend/random");

                setImages(response.data);

                setShown(response.data.map(img => img.image_id));

            }
            catch (error) {

                console.error(error);

            }

        }

        loadImages();

    }, []);

    return (

        <>

            <Header />

            <div className="top-bar">

                <h2>
                    {showLiked ? "❤️ Liked Wallpapers" : "🖼 Recommended Wallpapers"}
                </h2>

                <div className="toggle-buttons">

                    <button
                        className={!showLiked ? "toggle-btn active" : "toggle-btn"}
                        onClick={() => setShowLiked(false)}
                    >
                        Recommendations
                    </button>

                    <button
                        className={showLiked ? "toggle-btn active" : "toggle-btn"}
                        onClick={() => setShowLiked(true)}
                    >
                        ❤️ Liked ({likedImages.length})
                    </button>

                </div>

            </div>

            <ImageGrid
                images={showLiked ? likedImages : images}
                votes={votes}
                onLike={handleLike}
                onDislike={handleDislike}
            />

            {!showLiked && (

                <button
                    className="next-btn"
                    onClick={loadRecommendations}
                    disabled={loading}
                >
                    {loading ? "Loading..." : "Next Recommendations"}
                </button>

            )}

        </>

    );

}

export default App;