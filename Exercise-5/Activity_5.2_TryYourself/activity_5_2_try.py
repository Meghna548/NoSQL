from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")

client.admin.command("ping")
print("Connected to MongoDB successfully")

db = client["sales_lookup"]

products = db["products"]
orders = db["orders"]

pipeline = [
    {
        "$lookup": {
            "from": "products",
            "let": {
                "productId": "$product_id"
            },
            "pipeline": [
                {
                    "$match": {
                        "$expr": {
                            "$eq": [
                                "$_id",
                                "$$productId"
                            ]
                        }
                    }
                },
                {
                    "$match": {
                        "category": "Electronics"
                    }
                }
            ],
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
            "quantity": 1,
            "product_name": "$product.name",
            "category": "$product.category",
            "base_price": "$product.base_price"
        }
    }
]

print("\nOrders for Electronics Products:")

for result in orders.aggregate(pipeline):
    print(result)