import os
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient(os.getenv("MONGO_URI"))

db = client["indexing_lab"]
products = db["products"]

# Run representative queries multiple times
for i in range(5):

    # Query 1: Category + sort by price
    list(
        products.find(
            {"category": "Electronics"}
        ).sort("price", 1)
    )

    # Query 2: Price range
    list(
        products.find(
            {"price": {"$gte": 500, "$lte": 1000}}
        )
    )

    # Query 3: Tag search
    list(
        products.find(
            {"tags": "sale"}
        )
    )

    # Query 4: Name search
    list(
        products.find(
            {"name": {"$regex": "Product 1", "$options": "i"}}
        )
    )

    # Query 5: Rating filter
    list(
        products.find(
            {"rating": {"$gte": 4.5}}
        )
    )

# Display index usage statistics
print("\nIndex Usage Statistics:")
print("-" * 50)

stats = products.aggregate([
    {"$indexStats": {}}
])

for stat in stats:
    print(
        "Index:",
        stat["name"],
        "| Operations:",
        stat["accesses"]["ops"]
    )

client.close()

print("\nActivity 6.1 Try Yourself completed.")