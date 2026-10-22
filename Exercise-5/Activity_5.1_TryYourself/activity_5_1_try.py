from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")
client.admin.command("ping")
print("Connected to MongoDB successfully")

db = client["sales_analytics"]
orders = db["orders"]

pipeline = [
    {
        "$project": {
            "customer": 1,
            "product": 1,
            "order_value": {
                "$multiply": ["$quantity", "$unit_price"]
            }
        }
    },
    {
        "$bucket": {
            "groupBy": "$order_value",
            "boundaries": [0, 50, 200, float("inf")],
            "default": "Other",
            "output": {
                "count": {"$sum": 1},
                "total_value": {"$sum": "$order_value"}
            }
        }
    }
]

print("\n========== ORDER VALUE BUCKETS ==========")

for doc in orders.aggregate(pipeline):
    print(doc)

print("\nActivity 5.1 Try Yourself completed successfully!")

client.close()
print("MongoDB connection closed")