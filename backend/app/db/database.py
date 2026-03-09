from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = "mongodb://localhost:27017"

client = AsyncIOMotorClient(MONGO_URL)

database = client["modeldock_db"]

users_collection = database["users"]
projects_collection = database["projects"]