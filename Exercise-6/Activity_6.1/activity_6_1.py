from pymongo import MongoClient
import random


# --------------------------------------------------
# 1. CONNECT TO MONGODB
# --------------------------------------------------

client = MongoClient("mongodb://localhost:27017")

client.admin.command("ping")

print("Connected to MongoDB successfully.")

db = client["indexing_lab"]
products = db["products"]


# --------------------------------------------------
# 2. START WITH A CLEAN COLLECTION
# --------------------------------------------------

products.drop()

print("Products collection cleared.")


# --------------------------------------------------
# 3. GENERATE 50,000 PRODUCTS
# --------------------------------------------------

categories = [
    "Electronics",
    "Clothing",
    "Books",
    "Home",
    "Sports"
]

tags_list = [
    ["new", "sale"],
    ["popular", "featured"],
    ["premium", "new"],
    ["budget", "sale"],
    ["trending", "popular"]
]

products_data = []

for i in range(50000):

    product = {
        "name": f"Product {i}",
        "category": random.choice(categories),
        "price": round(random.uniform(10, 2000), 2),
        "rating": round(random.uniform(1, 5), 1),
        "stock": random.randint(0, 500),
        "tags": random.choice(tags_list)
    }

    products_data.append(product)


print("Generating 50,000 products...")

products.insert_many(products_data)

print("50,000 products inserted.")


# --------------------------------------------------
# 4. REMOVE ALL INDEXES EXCEPT _id
# --------------------------------------------------

for index in products.list_indexes():

    if index["name"] != "_id_":
        products.drop_index(index["name"])


print("Only the default _id index remains.")


# --------------------------------------------------
# 5. FUNCTION TO RUN EXPLAIN
# --------------------------------------------------

def explain_query(filter_query, sort=None):

    command = {
        "find": "products",
        "filter": filter_query
    }

    if sort is not None:
        command["sort"] = sort

    result = db.command(
        "explain",
        command,
        verbosity="executionStats"
    )

    execution_stats = result["executionStats"]

    docs_examined = execution_stats["totalDocsExamined"]

    stages = str(execution_stats["executionStages"])

    if "IXSCAN" in stages:
        stage = "IXSCAN"

    elif "COLLSCAN" in stages:
        stage = "COLLSCAN"

    else:
        stage = "OTHER"

    return stage, docs_examined


# --------------------------------------------------
# 6. FIVE REPRESENTATIVE QUERIES
# --------------------------------------------------

query1_filter = {
    "category": "Electronics"
}

query1_sort = {
    "price": 1
}


query2_filter = {
    "price": {
        "$gte": 500,
        "$lte": 1000
    }
}


query3_filter = {
    "tags": "sale"
}


query4_filter = {
    "name": {
        "$regex": "^Product 1",
        "$options": "i"
    }
}


query5_filter = {
    "rating": {
        "$gte": 4.5
    }
}


# --------------------------------------------------
# 7. BEFORE INDEXES
# --------------------------------------------------

print()
print("======================================")
print("BEFORE INDEXES")
print("======================================")


stage, docs = explain_query(
    query1_filter,
    query1_sort
)

print("Query 1 - Category + Sort")
print("Stage:", stage)
print("Total Docs Examined:", docs)


stage, docs = explain_query(
    query2_filter
)

print()
print("Query 2 - Price Range")
print("Stage:", stage)
print("Total Docs Examined:", docs)


stage, docs = explain_query(
    query3_filter
)

print()
print("Query 3 - Tag Search")
print("Stage:", stage)
print("Total Docs Examined:", docs)


stage, docs = explain_query(
    query4_filter
)

print()
print("Query 4 - Name Search")
print("Stage:", stage)
print("Total Docs Examined:", docs)


stage, docs = explain_query(
    query5_filter
)

print()
print("Query 5 - Rating Filter")
print("Stage:", stage)
print("Total Docs Examined:", docs)


# --------------------------------------------------
# 8. CREATE INDEXES
# --------------------------------------------------

print()
print("======================================")
print("CREATING INDEXES")
print("======================================")


# Query 1:
# category equality + price sorting
products.create_index(
    [
        ("category", 1),
        ("price", 1)
    ],
    name="category_price_idx"
)


# Query 2:
# price range
products.create_index(
    [
        ("price", 1)
    ],
    name="price_idx"
)


# Query 3:
# tags array
products.create_index(
    [
        ("tags", 1)
    ],
    name="tags_idx"
)


# Query 4:
# name search
products.create_index(
    [
        ("name", "text")
    ],
    name="name_text_idx"
)


# Query 5:
# rating filter
products.create_index(
    [
        ("rating", 1)
    ],
    name="rating_idx"
)


print("All indexes created.")


# --------------------------------------------------
# 9. DISPLAY INDEXES
# --------------------------------------------------

print()
print("Indexes:")

for index in products.list_indexes():

    print(
        index["name"],
        ":",
        index["key"]
    )


# --------------------------------------------------
# 10. AFTER INDEXES
# --------------------------------------------------

print()
print("======================================")
print("AFTER INDEXES")
print("======================================")


stage, docs = explain_query(
    query1_filter,
    query1_sort
)

print("Query 1 - Category + Sort")
print("Stage:", stage)
print("Total Docs Examined:", docs)


stage, docs = explain_query(
    query2_filter
)

print()
print("Query 2 - Price Range")
print("Stage:", stage)
print("Total Docs Examined:", docs)


stage, docs = explain_query(
    query3_filter
)

print()
print("Query 3 - Tag Search")
print("Stage:", stage)
print("Total Docs Examined:", docs)


# Text search is demonstrated separately
# because $text requires a text index.

text_query = {
    "$text": {
        "$search": "Product 1"
    }
}

text_result = db.command(
    "explain",
    {
        "find": "products",
        "filter": text_query
    },
    verbosity="executionStats"
)

print()
print("Query 4 - Text Search")
print(
    "Total Docs Examined:",
    text_result["executionStats"]["totalDocsExamined"]
)


stage, docs = explain_query(
    query5_filter
)

print()
print("Query 5 - Rating Filter")
print("Stage:", stage)
print("Total Docs Examined:", docs)


# --------------------------------------------------
# 11. FINISH
# --------------------------------------------------

print()
print("======================================")
print("Activity 6.1 completed.")
print("======================================")


client.close()