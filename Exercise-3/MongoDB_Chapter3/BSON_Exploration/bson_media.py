import sys
import os

# Allow Python to find the config folder in the main project
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.connection import get_db, banner
from bson import Binary


def main():

    banner("BSON Media Insertion - Photo")

    # Connect to MongoDB
    db = get_db("nosql_labs")

    # Create/use collection
    collection = db["media"]

    # Remove old data so we get a clean result
    collection.drop()

    # Path of the photo
    image_path = os.path.join(
        os.path.dirname(__file__),
        "photo.jpg"
    )

    # Check whether photo exists
    if not os.path.exists(image_path):
        print("[ERROR] photo.jpg not found!")
        print("Put your photo inside the BSON_Exploration folder.")
        return

    # Read photo as binary data
    with open(image_path, "rb") as image_file:
        image_data = image_file.read()

    # Create MongoDB document
    document = {
        "filename": "photo.jpg",
        "media_type": "image/jpeg",
        "description": "Photo inserted from my device",
        "data": Binary(image_data)
    }

    # Insert into MongoDB
    result = collection.insert_one(document)

    print("[OK] Photo inserted successfully!")
    print("Inserted document ID:", result.inserted_id)
    print("File name:", document["filename"])
    print("Media type:", document["media_type"])
    print("File size:", len(image_data), "bytes")


if __name__ == "__main__":
    main()