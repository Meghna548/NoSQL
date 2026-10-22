import os
from pymongo import MongoClient
from bson import Binary
from bson.json_util import dumps


def print_json(data):
    print(dumps(data, indent=4))


def main():

    print("=" * 60)
    print("Activity 3.2 - Referenced to Embedded Design")
    print("=" * 60)

    # =========================================================
    # CONNECT TO MONGODB
    # =========================================================

    client = MongoClient("mongodb://localhost:27017")

    db = client["nosql_labs"]

    print("\n[OK] Connected to MongoDB at localhost:27017")


    # =========================================================
    # CREATE COLLECTIONS
    # =========================================================

    db["posts"].drop()
    db["comments"].drop()
    db["posts_embedded"].drop()

    posts_col = db["posts"]
    comments_col = db["comments"]
    embedded_col = db["posts_embedded"]


    # =========================================================
    # READ PHOTO FROM DEVICE
    # =========================================================

    image_path = os.path.join(
        os.path.dirname(__file__),
        "photo.jpg"
    )

    if not os.path.exists(image_path):

        print("\n[ERROR] photo.jpg not found!")
        print("Make sure photo.jpg is inside Activity_3.2.")

        return

    with open(image_path, "rb") as image_file:
        image_data = image_file.read()

    print("\n[OK] Photo found:")
    print(image_path)

    print("[OK] Photo size:", len(image_data), "bytes")


    # =========================================================
    # 1. REFERENCED DESIGN
    # =========================================================

    print("\n" + "=" * 60)
    print("1. REFERENCED DESIGN")
    print("=" * 60)

    posts = [

        {
            "title": "Introduction to MongoDB",
            "content": "MongoDB is a NoSQL document database.",
            "author": "Student 1",

            "image": Binary(image_data),
            "image_filename": "photo.jpg",
            "media_type": "image/jpeg"
        },

        {
            "title": "Learning Python",
            "content": "Python is a popular programming language.",
            "author": "Student 2"
        },

        {
            "title": "Understanding NoSQL",
            "content": "NoSQL databases provide flexible data models.",
            "author": "Student 3"
        },

        {
            "title": "Introduction to Artificial Intelligence",
            "content": "Artificial Intelligence is used in many applications.",
            "author": "Student 4"
        },

        {
            "title": "Introduction to Machine Learning",
            "content": "Machine Learning allows computers to learn from data.",
            "author": "Student 5"
        }
    ]


    # Insert 5 posts

    post_result = posts_col.insert_many(posts)

    post_ids = post_result.inserted_ids

    print("\nPosts inserted:", len(post_ids))

    print("Photo inserted into Post 1: YES")


    # =========================================================
    # INSERT 10 COMMENTS
    # =========================================================

    print("\nInserting 10 comments...")

    comment_data = [

        ("Great introduction to MongoDB!", "Alice"),
        ("This explanation was very useful.", "Rahul"),

        ("Python is really interesting.", "Meera"),
        ("I enjoyed learning Python.", "Arjun"),

        ("NoSQL databases are flexible.", "Anu"),
        ("Good explanation of NoSQL.", "Vivek"),

        ("AI has many real-world applications.", "Diya"),
        ("Very interesting topic!", "Kiran"),

        ("Machine Learning is fascinating.", "Neha"),
        ("This helped me understand ML.", "Rohan")
    ]


    comments = []


    # 2 comments for each post

    for i, post_id in enumerate(post_ids):

        for j in range(2):

            text, author = comment_data[i * 2 + j]

            comments.append(
                {
                    "post_id": post_id,
                    "text": text,
                    "author": author
                }
            )


    comments_col.insert_many(comments)

    print("Comments inserted:", len(comments))


    # =========================================================
    # 2. $LOOKUP
    # =========================================================

    print("\n" + "=" * 60)
    print("2. RETRIEVE POST WITH COMMENTS USING $LOOKUP")
    print("=" * 60)


    pipeline = [

        {
            "$match": {
                "_id": post_ids[0]
            }
        },

        {
            "$lookup": {
                "from": "comments",

                "localField": "_id",

                "foreignField": "post_id",

                "as": "comments"
            }
        }
    ]


    lookup_result = list(
        posts_col.aggregate(pipeline)
    )


    if lookup_result:

        print("\nPost 1 with comments:")

        display_post = dict(lookup_result[0])

        # Don't print the actual binary image in terminal
        display_post["image"] = "Binary image data (photo.jpg)"

        print_json(display_post)


    # =========================================================
    # 3. MIGRATE TO EMBEDDED DESIGN
    # =========================================================

    print("\n" + "=" * 60)
    print("3. MIGRATE TO EMBEDDED DESIGN")
    print("=" * 60)


    embedded_posts = []


    for post in posts_col.find():

        # Find comments belonging to this post

        post_comments = list(
            comments_col.find(
                {"post_id": post["_id"]},

                {
                    "_id": 0,
                    "post_id": 0
                }
            )
        )


        # Copy post

        embedded_post = dict(post)


        # Put comments inside the post

        embedded_post["comments"] = post_comments


        embedded_posts.append(
            embedded_post
        )


    # Insert migrated posts

    embedded_col.insert_many(embedded_posts)


    print(
        "Posts migrated to embedded collection:",
        len(embedded_posts)
    )


    # =========================================================
    # DISPLAY EMBEDDED POST
    # =========================================================

    embedded_result = embedded_col.find_one(
        {"_id": post_ids[0]}
    )


    if embedded_result:

        print("\nEmbedded Post 1:")

        display_embedded = dict(embedded_result)

        # Don't print binary image data

        display_embedded["image"] = \
            "Binary image data (photo.jpg)"

        print_json(display_embedded)


    # =========================================================
    # 4. QUERY COMPARISON
    # =========================================================

    print("\n" + "=" * 60)
    print("4. QUERY COMPARISON")
    print("=" * 60)


    print("\nREFERENCED DESIGN")
    print("-----------------")

    print("Collections:")
    print("1. posts")
    print("2. comments")

    print("\nTo display a post with comments:")
    print("1 aggregation query using $lookup")


    print("\nEMBEDDED DESIGN")
    print("----------------")

    print("Collection:")
    print("1. posts_embedded")

    print("\nTo display a post with comments:")
    print("1 find query")

    print("Comments are already inside the post.")


    print("\nCOMPARISON")
    print("----------")

    print(
        "Referenced design : "
        "1 aggregation query using $lookup"
    )

    print(
        "Embedded design   : "
        "1 find query"
    )


    print("\nEmbedded design is convenient when comments")
    print("are small in number and usually read with the post.")


    print("\nReferenced design is better when comments")
    print("become very large or need independent access.")


    # =========================================================
    # FINAL RESULT
    # =========================================================

    print("\n" + "=" * 60)
    print("ACTIVITY 3.2 COMPLETED SUCCESSFULLY!")
    print("=" * 60)


    print("\nFinal data:")

    print(
        "Posts           :",
        posts_col.count_documents({})
    )

    print(
        "Comments        :",
        comments_col.count_documents({})
    )

    print(
        "Embedded posts  :",
        embedded_col.count_documents({})
    )

    print("Photo in Post 1 : YES")


    client.close()


if __name__ == "__main__":
    main()