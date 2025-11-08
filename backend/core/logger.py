from datetime import datetime
from core.database import db   # ✅ correct import

async def log_event(collection: str, data: dict):
    data["timestamp"] = datetime.utcnow()  # ✅ correct datetime usage
    await db[collection].insert_one(data)
