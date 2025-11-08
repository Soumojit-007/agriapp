import os
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

load_dotenv()

# Read URI and DB name directly from .env
MONGODB_URI = os.getenv("MONGODB_URI")
MONGODB_DB_NAME = os.getenv("MONGODB_DB_NAME", "agriapp")

if not MONGODB_URI:
    raise ValueError("❌ MONGODB_URI is missing in your .env file")

# Create MongoDB client (async)
client = AsyncIOMotorClient(MONGODB_URI)

# Select database
db = client[MONGODB_DB_NAME]
