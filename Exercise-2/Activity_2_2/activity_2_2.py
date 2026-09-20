"""Activity 2.2 - Bookstore CRUD Operations
Update the price of books published before 2010 by 10%.
"""

from pymongo import MongoClient
import json


# Connect to Docker MongoDB
client = MongoClient("mongodb://localhost:27018")

# Select database
db = client["bookstore"]

# Select collection
col = db["books"]


# Load books from JSON
with open("chapter-02/Activity_2_2/activity_2_2.json", "r", encoding="utf-8") as file:
    books = json.load(file)


# Remove old documents so we start fresh
col.delete_many({})


# Insert the books
result = col.insert_many(books)

print("=== CREATE: Inserting 5 books ===")
print(f"[OK] Inserted {len(result.inserted_ids)} books")


# Show prices before update
print("\n=== BEFORE UPDATE ===")

for book in col.find({}, {"title": 1, "year": 1, "price": 1, "_id": 0}):
    print(
        f"  {book['title']:<45} "
        f"({book['year']}) - ${book['price']:.2f}"
    )


# Update books published before 2010
print("\n=== UPDATE: 10% price increase for books before 2010 ===")

update_result = col.update_many(
    {"year": {"$lt": 2010}},
    {"$mul": {"price": 1.10}}
)

print(f"[OK] Updated {update_result.modified_count} book(s)")


# Show prices after update
print("\n=== AFTER UPDATE ===")

for book in col.find({}, {"title": 1, "year": 1, "price": 1, "_id": 0}):
    print(
        f"  {book['title']:<45} "
        f"({book['year']}) - ${book['price']:.2f}"
    )


# Save final MongoDB data as JSON
final_books = list(col.find({}, {"_id": 0}))

with open(
    "chapter-02/Activity_2_2/activity_2_2_final.json",
    "w",
    encoding="utf-8"
) as file:
    json.dump(final_books, file, indent=4)


print("\n[OK] Final data saved to activity_2_2_final.json")


client.close()