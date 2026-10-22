import os
import time
import random
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient(os.getenv("MONGO_URI"))

db = client["indexing_lab_6_2"]
products = db["products"]

# Start fresh
products.drop()

# --------------------------------------------------
# PART 1: Insert 10,000 documents with no indexes
# --------------------------------------------------

documents_1 = []

for i in range(10000):
    documents_1.append({
        "name": f"Product {i}",
        "category": random.choice([
            "Electronics",
            "Clothing",
            "Books",
            "Home"
        ]),
        "price": round(random.uniform(10, 2000), 2),
        "rating": round(random.uniform(1, 5), 1),
        "stock": random.randint(0, 500),
        "tags": random.sample(
            ["sale", "new", "popular", "discount", "premium"],
            2
        )
    })

start_time = time.perf_counter()

products.insert_many(documents_1)

end_time = time.perf_counter()

time_without_indexes = end_time - start_time

print("\n1. Insert without indexes")
print("Documents inserted:", len(documents_1))
print("Time:", round(time_without_indexes, 4), "seconds")


# --------------------------------------------------
# PART 2: Create 5 indexes
# --------------------------------------------------

products.create_index(
    [("category", 1), ("price", 1)],
    name="category_price_idx"
)

products.create_index(
    [("price", 1)],
    name="price_idx"
)

products.create_index(
    [("tags", 1)],
    name="tags_idx"
)

products.create_index(
    [("stock", 1)],
    name="stock_idx"
)

products.create_index(
    [("rating", 1)],
    name="rating_idx"
)

print("\n5 indexes created.")


# --------------------------------------------------
# PART 3: Insert another 10,000 documents
# --------------------------------------------------

documents_2 = []

for i in range(10000, 20000):
    documents_2.append({
        "name": f"Product {i}",
        "category": random.choice([
            "Electronics",
            "Clothing",
            "Books",
            "Home"
        ]),
        "price": round(random.uniform(10, 2000), 2),
        "rating": round(random.uniform(1, 5), 1),
        "stock": random.randint(0, 500),
        "tags": random.sample(
            ["sale", "new", "popular", "discount", "premium"],
            2
        )
    })

start_time = time.perf_counter()

products.insert_many(documents_2)

end_time = time.perf_counter()

time_with_indexes = end_time - start_time

print("\n2. Insert with 5 indexes")
print("Documents inserted:", len(documents_2))
print("Time:", round(time_with_indexes, 4), "seconds")


# --------------------------------------------------
# PART 4: Calculate percentage slowdown
# --------------------------------------------------

slowdown = (
    (time_with_indexes - time_without_indexes)
    / time_without_indexes
) * 100

print("\n3. Insert performance comparison")
print("Without indexes:", round(time_without_indexes, 4), "seconds")
print("With 5 indexes:", round(time_with_indexes, 4), "seconds")
print("Percentage slowdown:", round(slowdown, 2), "%")


# --------------------------------------------------
# PART 5: Five representative queries
# --------------------------------------------------

queries = [
    (
        "Category + Sort",
        lambda: list(
            products.find(
                {"category": "Electronics"}
            ).sort("price", 1)
        )
    ),

    (
        "Price Range",
        lambda: list(
            products.find(
                {"price": {"$gte": 500, "$lte": 1000}}
            )
        )
    ),

    (
        "Tag Search",
        lambda: list(
            products.find(
                {"tags": "sale"}
            )
        )
    ),

    (
        "Stock Range",
        lambda: list(
            products.find(
                {"stock": {"$gte": 100, "$lte": 300}}
            )
        )
    ),

    (
        "Rating Filter",
        lambda: list(
            products.find(
                {"rating": {"$gte": 4.5}}
            )
        )
    )
]


# --------------------------------------------------
# PART 6: Run queries with all 5 indexes
# --------------------------------------------------

print("\n4. Query performance with 5 indexes")
print("-" * 50)

times_with_5_indexes = {}

for name, query in queries:

    start_time = time.perf_counter()

    query()

    end_time = time.perf_counter()

    query_time = end_time - start_time

    times_with_5_indexes[name] = query_time

    print(
        name,
        ":",
        round(query_time, 6),
        "seconds"
    )


# --------------------------------------------------
# PART 7: Keep only the most critical index
# --------------------------------------------------

products.drop_index("price_idx")
products.drop_index("tags_idx")
products.drop_index("stock_idx")
products.drop_index("rating_idx")

print("\nOnly category_price_idx kept.")


# --------------------------------------------------
# PART 8: Run the same queries again
# --------------------------------------------------

print("\n5. Query performance with only one index")
print("-" * 50)

times_with_one_index = {}

for name, query in queries:

    start_time = time.perf_counter()

    query()

    end_time = time.perf_counter()

    query_time = end_time - start_time

    times_with_one_index[name] = query_time

    print(
        name,
        ":",
        round(query_time, 6),
        "seconds"
    )


# --------------------------------------------------
# PART 9: Compare query times
# --------------------------------------------------

print("\n6. Query comparison")
print("-" * 50)

for name, query_time in times_with_5_indexes.items():

    one_index_time = times_with_one_index[name]

    print("\n", name)
    print(
        "With 5 indexes:",
        round(query_time, 6),
        "seconds"
    )
    print(
        "With 1 index:",
        round(one_index_time, 6),
        "seconds"
    )


print("\nActivity 6.2 completed.")

client.close()