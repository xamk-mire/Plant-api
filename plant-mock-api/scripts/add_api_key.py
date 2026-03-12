"""
Add a new API key to the database.
Run from project root: python -m scripts.add_api_key [key_name]

Prints the generated key once - store it securely.
"""
import asyncio
import os
import secrets
import sys
import uuid

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import AsyncSessionLocal, init_db
from app.models import ApiKey
from app.security.api_key import hash_api_key


async def add_key(name: str = "greenhouse-app"):
    await init_db()
    plain_key = f"pk_{secrets.token_urlsafe(32)}"
    key_hash = hash_api_key(plain_key)

    async with AsyncSessionLocal() as session:
        api_key = ApiKey(
            id=uuid.uuid4(),
            key_hash=key_hash,
            name=name,
            is_active=True,
        )
        session.add(api_key)
        await session.commit()

    print(f"API key created: {name}")
    print("\n--- API Key (store securely, shown once) ---")
    print(plain_key)
    print("--------------------------------------------")
    print("Use header: X-API-Key: <key>")


if __name__ == "__main__":
    name = sys.argv[1] if len(sys.argv) > 1 else "greenhouse-app"
    asyncio.run(add_key(name))
