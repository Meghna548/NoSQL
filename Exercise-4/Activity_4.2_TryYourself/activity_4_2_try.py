from pymongo import MongoClient, UpdateOne

client = MongoClient("mongodb://localhost:27017")
client.admin.command("ping")
print("Connected to MongoDB successfully")

db = client["inventory"]
products = db["products_4_2_try"]

product_data = [
    {"sku": "P001", "name": "Laptop", "price": 900, "stock": 20},
    {"sku": "P002", "name": "Mouse", "price": 25, "stock": 50},
    {"sku": "P003", "name": "Keyboard", "price": 45, "stock": 30},
    {"sku": "P004", "name": "Headphones", "price": 75, "stock": 15},
    {"sku": "P005", "name": "Monitor", "price": 200, "stock": 10}
]

operations = []

for product in product_data:
    operations.append(
        UpdateOne(
            {"sku": product["sku"]},
            {"$set": product},
            upsert=True
        )
    )

result = products.bulk_write(operations)

print("\n========== BULK IMPORT RESULT ==========")
print("Matched count:", result.matched_count)
print("Modified count:", result.modified_count)
print("Upserted count:", result.upserted_count)

print("\n========== PRODUCTS ==========")

for product in products.find({}, {"_id": 0}).sort("sku", 1):
    print(product)

print("\nTotal products:", products.count_documents({}))

print("\nIdempotent bulk import completed successfully!")

client.close()
print("MongoDB connection closed")