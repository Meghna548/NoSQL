import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.connection import get_db, banner


def main():

    banner("Lab 3.2 - Try Yourself: 10,000 Comments")

    db = get_db("nosql_labs")

    db["large_post"].drop()

    large_post = db["large_post"]

    post = {
        "title": "Post with 10,000 Comments",
        "content": "Example of a post with a very large number of comments.",
        "comment_count": 10000,
        "design": "Referenced comments"
    }

    large_post.insert_one(post)

    print("\nScenario:")
    print("A single post has 10,000 comments.")

    print("\nWhy embedding is problematic:")

    print("1. The document can become very large.")
    print("2. MongoDB documents have a 16 MB BSON size limit.")
    print("3. Updating comments can become more expensive.")
    print("4. Reading the post may load many comments unnecessarily.")
    print("5. Comments represent an unbounded or very large collection.")

    print("\nAlternative design:")

    print("Use a referenced design.")

    print("Store posts in one collection.")
    print("Store comments in another collection.")
    print("Each comment contains the post_id of its parent post.")

    print("\nRecommended structure:")

    print("posts")
    print("  _id")
    print("    |")
    print("    | post_id reference")
    print("    v")
    print("comments")
    print("  post_id")

    print("\nConclusion:")

    print(
        "Referencing is more suitable for 10,000 comments "
        "because comments can be stored and queried independently."
    )


if __name__ == "__main__":
    main()