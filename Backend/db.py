from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URI = "mongodb://MongoDB_service:27017"
client = AsyncIOMotorClient(MONGO_URI)

def get_db(db_name: str):
    return client[db_name]