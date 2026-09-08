import ImageCard from "./ImageCard";

function ImageGrid({ images, votes, onLike, onDislike }) {

    if(images.length===0){

        return(

            <div className="empty-state">

                ❤️ No liked wallpapers yet.

            </div>

        );

    }

    return(

        <div className="image-grid">

            {images.map((image)=>(

                <ImageCard
                    key={image.image_id}
                    image={image}
                    votes={votes}
                    onLike={onLike}
                    onDislike={onDislike}
                />

            ))}

        </div>

    );

}

export default ImageGrid;