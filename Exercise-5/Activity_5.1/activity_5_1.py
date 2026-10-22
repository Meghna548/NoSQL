from pymongo import MongoClient
from datetime import datetime

client = MongoClient("mongodb://localhost:27017")
client.admin.command("ping")
print("Connected to MongoDB successfully")

db = client["sales_analytics"]
orders = db["orders"]

orders.delete_many({})

order_data = [
    {"customer": "Alice", "product": "Laptop", "quantity": 2, "unit_price": 500, "order_date": datetime(2026, 1, 10), "status": "completed"},
    {"customer": "Bob", "product": "Mouse", "quantity": 3, "unit_price": 25, "order_date": datetime(2026, 1, 12), "status": "completed"},
    {"customer": "Carol", "product": "Keyboard", "quantity": 2, "unit_price": 40, "order_date": datetime(2026, 1, 15), "status": "pending"},
    {"customer": "David", "product": "Monitor", "quantity": 1, "unit_price": 200, "order_date": datetime(2026, 1, 20), "status": "completed"},
    {"customer": "Alice", "product": "Mouse", "quantity": 4, "unit_price": 25, "order_date": datetime(2026, 2, 5), "status": "completed"},
    {"customer": "Bob", "product": "Laptop", "quantity": 1, "unit_price": 500, "order_date": datetime(2026, 2, 8), "status": "pending"},
    {"customer": "Carol", "product": "Monitor", "quantity": 2, "unit_price": 200, "order_date": datetime(2026, 2, 12), "status": "completed"},
    {"customer": "David", "product": "Keyboard", "quantity": 3, "unit_price": 40, "order_date": datetime(2026, 2, 18), "status": "cancelled"},
    {"customer": "Alice", "product": "Monitor", "quantity": 1, "unit_price": 200, "order_date": datetime(2026, 3, 3), "status": "completed"},
    {"customer": "Bob", "product": "Mouse", "quantity": 5, "unit_price": 25, "order_date": datetime(2026, 3, 7), "status": "completed"},
    {"customer": "Carol", "product": "Laptop", "quantity": 1, "unit_price": 500, "order_date": datetime(2026, 3, 10), "status": "pending"},
    {"customer": "David", "product": "Mouse", "quantity": 2, "unit_price": 25, "order_date": datetime(2026, 3, 15), "status": "completed"},
    {"customer": "Alice", "product": "Keyboard", "quantity": 2, "unit_price": 40, "order_date": datetime(2026, 4, 2), "status": "pending"},
    {"customer": "Bob", "product": "Monitor", "quantity": 1, "unit_price": 200, "order_date": datetime(2026, 4, 8), "status": "completed"},
    {"customer": "Carol", "product": "Mouse", "quantity": 6, "unit_price": 25, "order_date": datetime(2026, 4, 12), "status": "completed"},
    {"customer": "David", "product": "Laptop", "quantity": 1, "unit_price": 500, "order_date": datetime(2026, 4, 20), "status": "pending"},
    {"customer": "Alice", "product": "Mouse", "quantity": 2, "unit_price": 25, "order_date": datetime(2026, 5, 5), "status": "completed"},
    {"customer": "Bob", "product": "Keyboard", "quantity": 4, "unit_price": 40, "order_date": datetime(2026, 5, 10), "status": "cancelled"},
    {"customer": "Carol", "product": "Monitor", "quantity": 1, "unit_price": 200, "order_date": datetime(2026, 5, 15), "status": "completed"},
    {"customer": "David", "product": "Mouse", "quantity": 3, "unit_price": 25, "order_date": datetime(2026, 5, 20), "status": "completed"}
]

orders.insert_many(order_data)

print("Inserted", len(order_data), "orders")


print("\n========== MONTHLY REVENUE ==========")

monthly_revenue = [
    {
        "$group": {
            "_id": {
                "year": {"$year": "$order_date"},
                "month": {"$month": "$order_date"}
            },
            "revenue": {
                "$sum": {
                    "$multiply": ["$quantity", "$unit_price"]
                }
            }
        }
    },
    {
        "$sort": {
            "_id.year": 1,
            "_id.month": 1
        }
    }
]

for doc in orders.aggregate(monthly_revenue):
    print(
        doc["_id"]["year"],
        "Month",
        doc["_id"]["month"],
        "Revenue:",
        doc["revenue"]
    )


print("\n========== TOP 3 CUSTOMERS ==========")

top_customers = [
    {
        "$group": {
            "_id": "$customer",
            "total_spending": {
                "$sum": {
                    "$multiply": ["$quantity", "$unit_price"]
                }
            },
            "products_bought": {
                "$addToSet": "$product"
            }
        }
    },
    {
        "$sort": {
            "total_spending": -1
        }
    },
    {
        "$limit": 3
    }
]

for doc in orders.aggregate(top_customers):
    print(
        doc["_id"],
        "Total Spending:",
        doc["total_spending"],
        "Products:",
        doc["products_bought"]
    )


print("\n========== AVERAGE ORDER VALUE BY STATUS ==========")

average_order_value = [
    {
        "$group": {
            "_id": "$status",
            "average_order_value": {
                "$avg": {
                    "$multiply": ["$quantity", "$unit_price"]
                }
            }
        }
    },
    {
        "$sort": {
            "_id": 1
        }
    }
]

for doc in orders.aggregate(average_order_value):
    print(
        doc["_id"],
        "Average Order Value:",
        round(doc["average_order_value"], 2)
    )


print("\nActivity 5.1 completed successfully!")

client.close()
print("MongoDB connection closed")