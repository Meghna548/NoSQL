from pymongo import MongoClient
from pymongo.errors import OperationFailure


# 1. Connect to MongoDB
client = MongoClient("mongodb://localhost:27017")

client.admin.command("ping")
print("Connected to MongoDB successfully")


# 2. Select database
db = client["inventory"]


# 3. Delete old products collection if it already exists
if "products" in db.list_collection_names():
    db["products"].drop()


# 4. Create schema validation
validator = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["name", "price", "stock", "tags"],
        "properties": {
            "name": {
                "bsonType": "string"
            },
            "price": {
                "bsonType": ["int", "long", "double", "decimal"],
                "minimum": 0.01
            },
            "stock": {
                "bsonType": "int",
                "minimum": 0
            },
            "tags": {
                "bsonType": "array",
                "items": {
                    "bsonType": "string"
                }
            }
        }
    }
}


db.create_collection(
    "products",
    validator=validator,
    validationLevel="strict",
    validationAction="error"
)

products = db["products"]

print("Products collection created with schema validation")


# 5. Insert 10 products
product_data = [
    {
        "name": "Laptop",
        "price": 999,
        "stock": 15,
        "tags": ["electronics", "wireless", "premium"]
    },
    {
        "name": "Wireless Mouse",
        "price": 25,
        "stock": 50,
        "tags": ["electronics", "wireless"]
    },
    {
        "name": "Keyboard",
        "price": 45,
        "stock": 0,
        "tags": ["electronics", "wireless"]
    },
    {
        "name": "Headphones",
        "price": 75,
        "stock": 30,
        "tags": ["electronics", "wireless", "premium"]
    },
    {
        "name": "USB Cable",
        "price": 15,
        "stock": 100,
        "tags": ["electronics", "cable"]
    },
    {
        "name": "Smart Watch",
        "price": 150,
        "stock": 0,
        "tags": ["electronics", "wireless", "premium"]
    },
    {
        "name": "Backpack",
        "price": 40,
        "stock": 20,
        "tags": ["bags", "premium"]
    },
    {
        "name": "Notebook",
        "price": 10,
        "stock": 200,
        "tags": ["stationery"]
    },
    {
        "name": "Gaming Router",
        "price": 120,
        "stock": 10,
        "tags": ["electronics", "wireless"]
    },
    {
        "name": "Desk Lamp",
        "price": 35,
        "stock": 0,
        "tags": ["electronics", "home"]
    }
]

result = products.insert_many(product_data)

print("Inserted", len(result.inserted_ids), "products")


# 6. Display all products
print("\n========== ALL PRODUCTS ==========")

for product in products.find({}, {"_id": 0}):
    print(product)


# 7. Test schema validation
print("\n========== SCHEMA VALIDATION ==========")

invalid_product = {
    "name": "Invalid Product",
    "price": -50,
    "stock": -5,
    "tags": ["electronics"]
}

try:
    products.insert_one(invalid_product)
    print("ERROR: Invalid product was accepted")

except OperationFailure:
    print("Schema validation successfully rejected invalid product")


# 8. Comparison operators
print("\n========== COMPARISON OPERATORS ==========")

print("\nProducts with price between 20 and 50:")

query = {
    "price": {
        "$gte": 20,
        "$lte": 50
    }
}

for product in products.find(query, {"_id": 0}):
    print(product)


print("\nProducts with stock equal to 0:")

query = {
    "stock": 0
}

for product in products.find(query, {"_id": 0}):
    print(product)


# 9. Logical operators
print("\n========== LOGICAL OPERATORS ==========")

print("\nOut of stock OR price above 100:")

query = {
    "$or": [
        {"stock": 0},
        {"price": {"$gt": 100}}
    ]
}

for product in products.find(query, {"_id": 0}):
    print(product)


print("\nIn stock AND tagged premium:")

query = {
    "stock": {
        "$gt": 0
    },
    "tags": "premium"
}

for product in products.find(query, {"_id": 0}):
    print(product)


# 10. Array operators
print("\n========== ARRAY OPERATORS ==========")

print("\nProducts having BOTH electronics AND wireless:")

query = {
    "tags": {
        "$all": ["electronics", "wireless"]
    }
}

for product in products.find(query, {"_id": 0}):
    print(product)


print("\nProducts having exactly 2 tags:")

query = {
    "tags": {
        "$size": 2
    }
}

for product in products.find(query, {"_id": 0}):
    print(product)


# 11. Pagination
print("\n========== PAGINATION ==========")


def get_products_page(page_number, items_per_page):

    skip_count = (page_number - 1) * items_per_page

    cursor = (
        products
        .find({}, {"_id": 0})
        .sort("name", 1)
        .skip(skip_count)
        .limit(items_per_page)
    )

    return list(cursor)


page_number = 1
items_per_page = 5

page = get_products_page(page_number, items_per_page)

print("\nPage 1:")

for product in page:
    print(product)


page_number = 2

page = get_products_page(page_number, items_per_page)

print("\nPage 2:")

for product in page:
    print(product)


# 12. Final information
print("\n========== FINAL INFORMATION ==========")

print("Database:", db.name)
print("Collection:", products.name)
print("Total products:", products.count_documents({}))

print("\nActivity 4.1 completed successfully!")


# 13. Close MongoDB connection
client.close()

print("MongoDB connection closed")