from pymongo import MongoClient, UpdateOne

client = MongoClient("mongodb://localhost:27017")
client.admin.command("ping")
print("Connected to MongoDB successfully")

db = client["inventory"]
products = db["products_4_2"]

products.delete_many({})

initial_products = [
    {"sku": "A", "name": "Product A", "price": 100, "stock": 20, "is_active": True},
    {"sku": "B", "name": "Product B", "price": 200, "stock": 30, "is_active": True},
    {"sku": "C", "name": "Product C", "price": 300, "stock": 40, "is_active": True},
    {"sku": "D", "name": "Product D", "price": 400, "stock": 50, "is_active": True},
    {"sku": "E", "name": "Product E", "price": 500, "stock": 60, "is_active": True}
]

products.insert_many(initial_products)
print("Inserted initial products")


def upsert_product(sku, price):
    result = products.update_one(
        {"sku": sku},
        {
            "$set": {"price": price},
            "$setOnInsert": {
                "name": "New Product",
                "stock": 0,
                "is_active": True
            }
        },
        upsert=True
    )

    if result.matched_count > 0:
        print("Existing SKU updated:", sku)
    elif result.upserted_id is not None:
        print("New SKU inserted:", sku)


print("\n========== UPSERT EXISTING SKU ==========")
upsert_product("A", 150)
print(products.find_one({"sku": "A"}, {"_id": 0}))


print("\n========== UPSERT NEW SKU ==========")
upsert_product("F", 600)
print(products.find_one({"sku": "F"}, {"_id": 0}))


print("\n========== BULK WRITE ==========")

operations = [
    UpdateOne({"sku": "A"}, {"$inc": {"stock": 10}}),
    UpdateOne({"sku": "B"}, {"$inc": {"stock": 10}}),
    UpdateOne({"sku": "C"}, {"$inc": {"stock": 10}}),
    UpdateOne({"sku": "D"}, {"$set": {"is_active": False}}),
    UpdateOne({"sku": "E"}, {"$set": {"is_active": False}})
]

bulk_result = products.bulk_write(operations)

print("Matched count:", bulk_result.matched_count)
print("Modified count:", bulk_result.modified_count)
print("Upserted count:", bulk_result.upserted_count)


print("\n========== FINAL PRODUCTS ==========")

for product in products.find({}, {"_id": 0}).sort("sku", 1):
    print(product)


print("\nActivity 4.2 completed successfully!")

client.close()
print("MongoDB connection closed")