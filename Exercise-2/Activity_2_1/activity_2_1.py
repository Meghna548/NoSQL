from pymongo import MongoClient


# MongoDB Atlas connection
atlas_uri = "mongodb+srv://meghnar2284_db_user:n9pykqgtDbkwkcXT@cluster0.7uihtuj.mongodb.net/?appName=Cluster0"

# Docker MongoDB connection
docker_uri = "mongodb://127.0.0.1:27018"


# Connect to Atlas
atlas_client = MongoClient(atlas_uri)

# Connect to Docker MongoDB
docker_client = MongoClient(docker_uri)


# Get server information
atlas_info = atlas_client.server_info()
docker_info = docker_client.server_info()


print("========== MONGODB SERVER VERSION COMPARISON ==========")

print("\nAtlas MongoDB")
print("Version:", atlas_info["version"])

print("\nDocker MongoDB")
print("Version:", docker_info["version"])


print("\n========== COMPARISON ==========")

if atlas_info["version"] == docker_info["version"]:
    print("Both MongoDB servers have the same version.")
else:
    print("The MongoDB server versions are different.")


# Close connections
atlas_client.close()
docker_client.close()