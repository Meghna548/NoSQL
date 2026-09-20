from pymongo import MongoClient

atlas_uri = "mongodb+srv://meghnar2284_db_user:n9pykqgtDbkwkcXT@cluster0.7uihtuj.mongodb.net/?appName=Cluster0"

docker_uri = "mongodb://127.0.0.1:27018"

atlas_client = MongoClient(atlas_uri)
docker_client = MongoClient(docker_uri)

atlas_version = atlas_client.server_info()["version"]
docker_version = docker_client.server_info()["version"]

print("========== TRY IT YOURSELF ==========")
print("Atlas Server Version  :", atlas_version)
print("Docker Server Version :", docker_version)

print()
print("========== RESULT ==========")

if atlas_version == docker_version:
    print("The server versions are the same.")
else:
    print("The server versions are different.")

atlas_client.close()
docker_client.close()