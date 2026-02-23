import os
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = os.environ.get("MONGO_URL", "mongodb://localhost:27017")
client = AsyncIOMotorClient(MONGO_URL)
database = client.student_governance
students_collection = database.get_collection("students")

async def init_db():
    # Create unique index on roll_number
    await students_collection.create_index("roll_number", unique=True)
