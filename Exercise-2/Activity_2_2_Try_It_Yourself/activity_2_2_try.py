from pymongo import MongoClient
import json

# Connect to Docker MongoDB
client = MongoClient("mongodb://localhost:27018")

# Use a separate database so Activity 2.2 is not changed
db = client["bookstore_try"]

# Select books collection
books = db["books"]

# Load original books from JSON
with open(
    "chapter-02/Activity_2_2_Try_It_Yourself/activity_2_2_try.json",
    "r",
    encoding="utf-8"
) as file:
    book_data = json.load(file)

# Start with a clean collection
books.delete_many({})

# Insert books
books.insert_many(book_data)

print("=== TRY IT YOURSELF ===")
print("\nBOOKS BEFORE UPDATE")

for book in books.find({}, {"_id": 0, "title": 1, "genre": 1, "price": 1}):
    print(book)

# Increase price of Machine Learning books by 5%
result = books.update_many(
    {"genre": "Machine Learning"},
    {"$mul": {"price": 1.05}}
)

print("\n=== UPDATE RESULT ===")
print("Machine Learning books updated:", result.modified_count)

print("\nBOOKS AFTER UPDATE")

for book in books.find({}, {"_id": 0, "title": 1, "genre": 1, "price": 1}):
    print(book)

# Save final data
final_data = list(books.find({}, {"_id": 0}))

with open(
    "chapter-02/Activity_2_2_Try_It_Yourself/activity_2_2_try_result.json",
    "w",
    encoding="utf-8"
) as file:
    json.dump(final_data, file, indent=4)

print("\n[OK] Try-It-Yourself JSON result saved.")

client.close()