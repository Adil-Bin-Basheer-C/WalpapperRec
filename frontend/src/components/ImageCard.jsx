import "./ImageCard.css";

function ImageCard({ image, votes, onLike, onDislike }) {

    const status = votes[image.image_id];

    return (

        <div className="image-card">

            <img
                src={image.image_url}
                alt={image.filename}
            />

            <div className="card-body">

                <div className="similarity">
                    Similarity : {(image.similarity * 100).toFixed(1)}%
                </div>

            <div className="buttons">

                <div className="vote-buttons">

                    <button
                        className={`like-btn ${status === "liked" ? "active" : ""}`}
                        onClick={() => onLike(image.image_id)}
                    >
                        {status === "liked" ? "❤️ Liked" : "👍 Like"}
                    </button>

                    <button
                        className={`dislike-btn ${status === "disliked" ? "active" : ""}`}
                        onClick={() => onDislike(image.image_id)}
                    >
                        {status === "disliked" ? "💔 Disliked" : "👎 Dislike"}
                    </button>

                </div>

                <a
                    className="download-link"
                    href={`http://127.0.0.1:8000/download/${image.image_id}`}
                >
                    <button className="download-btn">
                        ⬇ Download Wallpaper
                    </button>
                </a>

            </div>

            </div>

        </div>

    );

}

export default ImageCard;