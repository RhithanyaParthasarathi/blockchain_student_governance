import os
import asyncio
import glob
from motor.motor_asyncio import AsyncIOMotorClient
import certifi
from dotenv import load_dotenv

# Get the path to the .env file in the backend directory
base_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(base_dir, "backend", ".env")
load_dotenv(dotenv_path=env_path)

MONGO_URL = os.environ.get("MONGO_URL")
if not MONGO_URL:
    MONGO_URL = "mongodb://localhost:27017"

async def reset_db():
    print("Resetting database...")
    client = AsyncIOMotorClient(MONGO_URL, tlsCAFile=certifi.where())
    database = client.student_governance
    students_collection = database.get_collection("students")
    
    # Reset has_voted for all students
    result = await students_collection.update_many({}, {"$set": {"has_voted": False}})
    print(f"Updated {result.modified_count} student records in the database.")

def reset_blockchain():
    print("Resetting blockchain node files...")
    blockchain_dir = os.path.join(base_dir, "blockchain_model")
    chain_files = glob.glob(os.path.join(blockchain_dir, "chain_*.json"))
    
    for file_path in chain_files:
        try:
            os.remove(file_path)
            print(f"Removed {file_path}")
        except Exception as e:
            print(f"Error removing {file_path}: {e}")

async def main():
    # 1. Reset Blockchain files
    reset_blockchain()
    
    # 2. Reset Database
    await reset_db()
    
    print("\nSystem has been reset. All votes have been cleared from nodes and the database.")
    print("Please restart your nodes and backend to reflect the changes.")

if __name__ == "__main__":
    asyncio.run(main())
