import os
import certifi
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

# Get the path to the .env file in the backend directory
base_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(base_dir, ".env")
load_dotenv(dotenv_path=env_path)

MONGO_URL = os.environ.get("MONGO_URL")
if not MONGO_URL:
    # Final fallback to localhost only if not in .env
    MONGO_URL = "mongodb://localhost:27017"

client = AsyncIOMotorClient(MONGO_URL, tlsCAFile=certifi.where())
database = client.student_governance
students_collection = database.get_collection("students")

async def init_db():
    # Create unique index on roll_number
    await students_collection.create_index("roll_number", unique=True)
