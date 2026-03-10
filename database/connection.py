import motor.motor_asyncio
from config import MONGO_URI, DB_NAME

# ──── MongoDB Connection ────
_client: motor.motor_asyncio.AsyncIOMotorClient = None
db = None


async def connect_db():
    """Connect to MongoDB Atlas via Motor (async)."""
    global _client, db
    _client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
    db = _client[DB_NAME]
    # Ping to verify connection
    await _client.admin.command("ping")
    return db


def get_db():
    """Return the database instance."""
    return db
