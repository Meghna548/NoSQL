import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.connection import get_db, banner, print_json


def main():

    banner("Lab 3.2: Migrate from Referenced to Embedded Design")

    db = get_db("nosql_labs")

    # Remove old collections if they exist
    db["posts"].drop()
    db["comments"].drop()
    db["posts_embedded"].drop()

    posts_col = db["posts"]
    comments_col = db["comments"]

    # ==================================================
    # PART A: REFERENCED DESIGN
    # ==================================================

    print("=== PART A: Referenced Design ===")

    # Insert 5 posts
    posts = [
        {
            "title": "Why NoSQL Matters for AI",
            "author": "arjun",
            "tags": ["nosql", "ai"],
            "created": "2024-01-15"
        },
        {
            "title": "MongoDB Aggregation Tips",
            "author": "sneha",
            "tags": ["mongodb", "aggregation"],
            "created": "2024-01-20"
        },
        {
            "title": "Vector Search Deep Dive",
            "author": "kavya",
            "tags": ["vector", "ai", "search"],
            "created": "2024-02-01"
        },
        {
            "title": "CAP Theorem Explained",
            "author": "arjun",
            "tags": ["cap", "distributed"],
            "created": "2024-02-10"
        },
        {
            "title": "Graph Databases for Fraud",
            "author": "rahul",
            "tags": ["neo4j", "fraud", "graph"],
            "created": "2024-02-15"
        }
    ]

    post_result = posts_col.insert_many(posts)
    post_ids = post_result.inserted_ids

    print(f"Inserted {len(post_ids)} posts")

    # Insert 10 comments = 2 comments per post
    comment_data = [
        ["Great overview!", "reader1"],
        ["I prefer SQL though", "reader2"],

        ["The $lookup stage is powerful", "reader4"],
        ["Can you cover $facet next?", "reader1"],

        ["HNSW vs IVF comparison?", "reader6"],
        ["How does this scale?", "reader2"],

        ["AP systems are underrated", "reader7"],
        ["Good for interviews too", "reader3"],

        ["Neo4j Cypher is intuitive", "reader8"],
        ["Graph + Vector hybrid?", "reader6"]
    ]

    comments = []

    for i, post_id in enumerate(post_ids):

        for j in range(2):

            text, author = comment_data[i * 2 + j]

            comments.append({
                "post_id": post_id,
                "text": text,
                "author": author
            })

    comments_col.insert_many(comments)

    print(f"Inserted {len(comments)} comments")

    # ==================================================
    # PART B: $LOOKUP
    # ==================================================

    print("\n--- Referenced Design: $lookup ---")

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

    result = list(posts_col.aggregate(pipeline))

    print_json(result[0])

    print(
        f"Post: {result[0]['title']} -> "
        f"{len(result[0]['comments'])} comments"
    )

    # ==================================================
    # PART C: EMBEDDED DESIGN
    # ==================================================

    print("\n=== PART C: Embedded Design ===")

    embedded_col = db["posts_embedded"]

    embedded_posts = []

    for i, post in enumerate(posts):

        post_comments = comment_data[i * 2:(i + 1) * 2]

        embedded_posts.append({
            **post,
            "comments": [
                {
                    "text": text,
                    "author": author
                }
                for text, author in post_comments
            ]
        })

    embedded_col.insert_many(embedded_posts)

    print(
        f"Inserted {len(embedded_posts)} embedded posts"
    )

    # ==================================================
    # PART D: COMPARISON
    # ==================================================

    print("\n--- Embedded Design: Single Find ---")

    embedded_result = embedded_col.find_one(
        {
            "_id": embedded_posts[0]["_id"]
        }
    )

    print_json(embedded_result)

    print(
        f"Post: {embedded_result['title']} -> "
        f"{len(embedded_result['comments'])} comments"
    )

    print("\n=== Design Comparison ===")

    print(
        "Referenced design: 1 aggregation query using $lookup"
    )

    print(
        "Embedded design: 1 find query retrieves post and comments together"
    )

    print("\nReferenced Design:")
    print("- Posts and comments are stored separately")
    print("- Comments contain post_id")
    print("- $lookup is used to combine them")

    print("\nEmbedded Design:")
    print("- Comments are stored inside the post")
    print("- A single find retrieves the post and comments")

    banner("Lab 3.2 Complete")


if __name__ == "__main__":
    main()