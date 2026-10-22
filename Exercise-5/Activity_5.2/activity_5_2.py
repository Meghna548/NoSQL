from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")

client.admin.command("ping")
print("Connected to MongoDB successfully")

db = client["sales_lookup"]

products = db["products"]
orders = db["orders"]

products.delete_many({})
orders.delete_many({})

product_data = [
    {
        "name": "Laptop",
        "category": "Electronics",
        "base_price": 500
    },
    {
        "name": "Mouse",
        "category": "Electronics",
        "base_price": 25
    },
    {
        "name": "Keyboard",
        "category": "Electronics",
        "base_price": 40
    },
    {
        "name": "Monitor",
        "category": "Electronics",
        "base_price": 200
    },
    {
        "name": "Desk",
        "category": "Furniture",
        "base_price": 150
    }
]

product_result = products.insert_many(product_data)

orders_data = [
    {
        "product_id": product_result.inserted_ids[0],
        "order_date": "2026-01-10",
        "quantity": 2
    },
    {
        "product_id": product_result.inserted_ids[1],
        "order_date": "2026-01-12",
        "quantity": 3
    },
    {
        "product_id": product_result.inserted_ids[2],
        "order_date": "2026-01-15",
        "quantity": 1
    },
    {
        "product_id": product_result.inserted_ids[3],
        "order_date": "2026-02-05",
        "quantity": 2
    },
    {
        "product_id": product_result.inserted_ids[0],
        "order_date": "2026-02-10",
        "quantity": 1
    },
    {
        "product_id": product_result.inserted_ids[1],
        "order_date": "2026-02-15",
        "quantity": 5
    },
    {
        "product_id": product_result.inserted_ids[2],
        "order_date": "2026-03-01",
        "quantity": 2
    },
    {
        "product_id": product_result.inserted_ids[3],
        "order_date": "2026-03-10",
        "quantity": 1
    }
]

orders.insert_many(orders_data)

print("Products inserted:", products.count_documents({}))
print("Orders inserted:", orders.count_documents({}))

print("\nProducts:")
for product in products.find():
    print(product)

print("\nOrders:")
for order in orders.find():
    print(order)

lookup_pipeline = [
    {
        "$lookup": {
            "from": "products",
            "localField": "product_id",
            "foreignField": "_id",
            "as": "product"
        }
    },
    {
        "$unwind": "$product"
    },
    {
        "$project": {
            "_id": 0,
            "order_date": 1,
            "product_name": "$product.name",
            "quantity": 1,
            "total": {
                "$multiply": [
                    "$quantity",
                    "$product.base_price"
                ]
            }
        }
    }
]

print("\nOrders with Product Details:")

for result in orders.aggregate(lookup_pipeline):
    print(result)

never_ordered_pipeline = [
    {
        "$lookup": {
            "from": "orders",
            "localField": "_id",
            "foreignField": "product_id",
            "as": "orders"
        }
    },
    {
        "$match": {
            "orders": {
                "$size": 0
            }
        }
    },
    {
        "$project": {
            "_id": 0,
            "name": 1,
            "category": 1,
            "base_price": 1
        }
    }
]

print("\nProducts Never Ordered:")

for result in products.aggregate(never_ordered_pipeline):
    print(result)