from pymongo import MongoClient


# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017")

client.admin.command("ping")

print("Connected to MongoDB successfully")


# Select database and collection
db = client["inventory"]
products = db["products"]


# Ask user for search text
search_text = input("Enter product name to search: ")


# Regex query - case insensitive
query = {
    "name": {
        "$regex": search_text,
        "$options": "i"
    }
}


# Display matching products
print("\n========== SEARCH RESULTS ==========")

results = products.find(query, {"_id": 0})

count = 0

for product in results:
    print(product)
    count += 1


print("\nNumber of matching products:", count)


# Close connection
client.close()

print("\nMongoDB connection closed")