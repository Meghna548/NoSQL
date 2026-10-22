import os
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient(os.getenv("MONGO_URI"))

db = client["indexing_lab_6_2"]
products = db["products"]

# Create the index if it does not already exist
products.create_index(
    [("category", 1), ("price", 1)],
    name="category_price_idx"
)

# Covered query
query = {
    "category": "Electronics",
    "price": {"$gte": 500, "$lte": 1000}
}

projection = {
    "_id": 0,
    "category": 1,
    "price": 1
}

# Run the covered query
cursor = products.find(
    query,
    projection
)

# Explain the query
explain_result = cursor.explain()

print("\nCovered Query:")
print("Query:", query)
print("Projection:", projection)

print("\nWinning Plan:")
print(explain_result["queryPlanner"]["winningPlan"])

print("\nExecution Statistics:")
print(
    "Documents examined:",
    explain_result["executionStats"]["totalDocsExamined"]
)

print(
    "Keys examined:",
    explain_result["executionStats"]["totalKeysExamined"]
)

# Check whether FETCH appears in the execution plan
plan_string = str(
    explain_result["queryPlanner"]["winningPlan"]
)

if "FETCH" in plan_string:
    print("\nFETCH stage is present.")
else:
    print("\nFETCH stage is NOT present.")

print("\nActivity 6.2 Try Yourself completed.")

client.close()