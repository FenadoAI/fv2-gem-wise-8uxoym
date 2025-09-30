"""
Bootstrap script to create the first owner account.
Run this before running tests.
"""

import os
import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
from server import hash_password, User

load_dotenv()


async def create_owner():
    """Create the first owner account."""
    mongo_url = os.getenv("MONGO_URL")
    db_name = os.getenv("DB_NAME")

    if not mongo_url or not db_name:
        print("Error: MONGO_URL and DB_NAME must be set in .env")
        sys.exit(1)

    client = AsyncIOMotorClient(mongo_url)
    db = client[db_name]

    # Check if owner already exists
    existing_owner = await db.users.find_one({"email": "owner@jewelcraft.com"})

    if existing_owner:
        print("✓ Owner account already exists")
        print(f"  Email: owner@jewelcraft.com")
        print(f"  Role: {existing_owner['role']}")
        client.close()
        return

    # Create owner
    owner = User(
        username="admin",
        email="owner@jewelcraft.com",
        role="owner"
    )

    owner_doc = owner.model_dump()
    owner_doc["password"] = hash_password("OwnerPass123")

    await db.users.insert_one(owner_doc)

    print("✓ Owner account created successfully!")
    print(f"  Email: owner@jewelcraft.com")
    print(f"  Password: OwnerPass123")
    print(f"  Role: owner")
    print("\n⚠️  IMPORTANT: Change this password in production!")

    client.close()


if __name__ == "__main__":
    print("\n" + "="*50)
    print("BOOTSTRAP OWNER ACCOUNT")
    print("="*50 + "\n")

    asyncio.run(create_owner())

    print("\n" + "="*50)