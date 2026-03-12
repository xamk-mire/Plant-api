"""
Seed script to populate the database with sample plant data.
Run from project root: python -m scripts.seed_plants

Also generates an API key and prints it (store securely).
"""
import asyncio
import os
import secrets
import sys
import uuid

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.database import AsyncSessionLocal, init_db
from app.models import ApiKey, Plant, PlantCare
from app.security.api_key import hash_api_key


PLANT_DATA = [
    {
        "scientific_name": "Monstera deliciosa",
        "common_name": "Swiss Cheese Plant",
        "family": "Araceae",
        "genus": "Monstera",
        "species": "deliciosa",
        "description": "Tropical plant with iconic split leaves, native to Central America.",
        "native_region": "Central America",
        "care": {
            "watering_frequency": "weekly",
            "light_requirement": "bright indirect",
            "humidity_min": 60,
            "humidity_max": 80,
            "temp_min_c": 18,
            "temp_max_c": 27,
            "soil_type": "well-draining, peat-based",
            "fertilizing": "monthly in growing season",
        },
    },
    {
        "scientific_name": "Epipremnum aureum",
        "common_name": "Pothos",
        "family": "Araceae",
        "genus": "Epipremnum",
        "species": "aureum",
        "description": "Hardy trailing vine with heart-shaped leaves, very forgiving for beginners.",
        "native_region": "French Polynesia",
        "care": {
            "watering_frequency": "weekly, when top inch dry",
            "light_requirement": "low to bright indirect",
            "humidity_min": 40,
            "humidity_max": 60,
            "temp_min_c": 15,
            "temp_max_c": 29,
            "soil_type": "well-draining potting mix",
            "fertilizing": "every 2-3 months",
        },
    },
    {
        "scientific_name": "Ficus lyrata",
        "common_name": "Fiddle Leaf Fig",
        "family": "Moraceae",
        "genus": "Ficus",
        "species": "lyrata",
        "description": "Dramatic plant with large, violin-shaped leaves.",
        "native_region": "West Africa",
        "care": {
            "watering_frequency": "weekly",
            "light_requirement": "bright indirect",
            "humidity_min": 40,
            "humidity_max": 60,
            "temp_min_c": 18,
            "temp_max_c": 24,
            "soil_type": "well-draining, rich",
            "fertilizing": "monthly spring to fall",
        },
    },
    {
        "scientific_name": "Sansevieria trifasciata",
        "common_name": "Snake Plant",
        "family": "Asparagaceae",
        "genus": "Dracaena",
        "species": "trifasciata",
        "description": "Tough succulent with upright striped leaves. Excellent air purifier.",
        "native_region": "West Africa",
        "care": {
            "watering_frequency": "every 2-3 weeks",
            "light_requirement": "low to bright indirect",
            "humidity_min": 30,
            "humidity_max": 50,
            "temp_min_c": 10,
            "temp_max_c": 29,
            "soil_type": "cactus/succulent mix",
            "fertilizing": "2-3 times per year",
        },
    },
    {
        "scientific_name": "Philodendron hederaceum",
        "common_name": "Heartleaf Philodendron",
        "family": "Araceae",
        "genus": "Philodendron",
        "species": "hederaceum",
        "description": "Classic trailing vine with glossy heart-shaped leaves.",
        "native_region": "Central America, Caribbean",
        "care": {
            "watering_frequency": "weekly",
            "light_requirement": "medium to bright indirect",
            "humidity_min": 40,
            "humidity_max": 70,
            "temp_min_c": 15,
            "temp_max_c": 26,
            "soil_type": "well-draining peat mix",
            "fertilizing": "monthly in growing season",
        },
    },
    {
        "scientific_name": "Calathea roseopicta",
        "common_name": "Rose Painted Calathea",
        "family": "Marantaceae",
        "genus": "Calathea",
        "species": "roseopicta",
        "description": "Striking foliage with pink and green patterns. Prayer plant family.",
        "native_region": "Brazil",
        "care": {
            "watering_frequency": "keep moist, not soggy",
            "light_requirement": "medium indirect",
            "humidity_min": 60,
            "humidity_max": 80,
            "temp_min_c": 18,
            "temp_max_c": 24,
            "soil_type": "peaty, moisture-retentive",
            "fertilizing": "every 4-6 weeks in growing season",
        },
    },
    {
        "scientific_name": "Aloe vera",
        "common_name": "Aloe Vera",
        "family": "Asphodelaceae",
        "genus": "Aloe",
        "species": "vera",
        "description": "Succulent with medicinal gel. Easy care and drought tolerant.",
        "native_region": "Arabian Peninsula",
        "care": {
            "watering_frequency": "every 2-3 weeks",
            "light_requirement": "bright indirect to full sun",
            "humidity_min": 30,
            "humidity_max": 50,
            "temp_min_c": 10,
            "temp_max_c": 29,
            "soil_type": "cactus/succulent mix",
            "fertilizing": "rarely, once in spring",
        },
    },
    {
        "scientific_name": "Ocimum basilicum",
        "common_name": "Basil",
        "family": "Lamiaceae",
        "genus": "Ocimum",
        "species": "basilicum",
        "description": "Popular culinary herb with aromatic leaves. Great for indoor gardens.",
        "native_region": "Tropical Asia",
        "care": {
            "watering_frequency": "keep soil moist",
            "light_requirement": "bright, 6+ hours",
            "humidity_min": 40,
            "humidity_max": 60,
            "temp_min_c": 18,
            "temp_max_c": 27,
            "soil_type": "rich, well-draining",
            "fertilizing": "every 2-4 weeks",
        },
    },
    {
        "scientific_name": "Spathiphyllum wallisii",
        "common_name": "Peace Lily",
        "family": "Araceae",
        "genus": "Spathiphyllum",
        "species": "wallisii",
        "description": "Elegant plant with white spathes. Tolerates low light.",
        "native_region": "Tropical Americas",
        "care": {
            "watering_frequency": "weekly, droops when thirsty",
            "light_requirement": "low to medium indirect",
            "humidity_min": 50,
            "humidity_max": 70,
            "temp_min_c": 18,
            "temp_max_c": 27,
            "soil_type": "peaty, moisture-retentive",
            "fertilizing": "every 6-8 weeks",
        },
    },
    {
        "scientific_name": "Zamioculcas zamiifolia",
        "common_name": "ZZ Plant",
        "family": "Araceae",
        "genus": "Zamioculcas",
        "species": "zamiifolia",
        "description": "Nearly indestructible plant with glossy green leaves. Tolerates neglect.",
        "native_region": "East Africa",
        "care": {
            "watering_frequency": "every 2-3 weeks",
            "light_requirement": "low to bright indirect",
            "humidity_min": 40,
            "humidity_max": 60,
            "temp_min_c": 15,
            "temp_max_c": 26,
            "soil_type": "well-draining",
            "fertilizing": "2-3 times per year",
        },
    },
    {
        "scientific_name": "Dracaena marginata",
        "common_name": "Dragon Tree",
        "family": "Asparagaceae",
        "genus": "Dracaena",
        "species": "marginata",
        "description": "Architectural plant with spiky leaves and red edges.",
        "native_region": "Madagascar",
        "care": {
            "watering_frequency": "every 1-2 weeks",
            "light_requirement": "medium indirect",
            "humidity_min": 40,
            "humidity_max": 60,
            "temp_min_c": 18,
            "temp_max_c": 24,
            "soil_type": "well-draining loam",
            "fertilizing": "monthly in growing season",
        },
    },
    {
        "scientific_name": "Chlorophytum comosum",
        "common_name": "Spider Plant",
        "family": "Asparagaceae",
        "genus": "Chlorophytum",
        "species": "comosum",
        "description": "Classic houseplant with cascading variegated leaves and plantlets.",
        "native_region": "Southern Africa",
        "care": {
            "watering_frequency": "weekly",
            "light_requirement": "bright indirect",
            "humidity_min": 40,
            "humidity_max": 60,
            "temp_min_c": 13,
            "temp_max_c": 27,
            "soil_type": "well-draining potting mix",
            "fertilizing": "monthly in growing season",
        },
    },
    {
        "scientific_name": "Pilea peperomioides",
        "common_name": "Chinese Money Plant",
        "family": "Urticaceae",
        "genus": "Pilea",
        "species": "peperomioides",
        "description": "Trendy plant with round, coin-shaped leaves on long petioles.",
        "native_region": "Southwest China",
        "care": {
            "watering_frequency": "weekly",
            "light_requirement": "bright indirect",
            "humidity_min": 50,
            "humidity_max": 70,
            "temp_min_c": 15,
            "temp_max_c": 24,
            "soil_type": "well-draining",
            "fertilizing": "monthly in growing season",
        },
    },
    {
        "scientific_name": "Crassula ovata",
        "common_name": "Jade Plant",
        "family": "Crassulaceae",
        "genus": "Crassula",
        "species": "ovata",
        "description": "Succulent with thick, woody stems and oval leaves. Symbol of prosperity.",
        "native_region": "South Africa",
        "care": {
            "watering_frequency": "every 2-3 weeks",
            "light_requirement": "bright light, some direct sun ok",
            "humidity_min": 30,
            "humidity_max": 50,
            "temp_min_c": 10,
            "temp_max_c": 24,
            "soil_type": "cactus/succulent mix",
            "fertilizing": "quarterly",
        },
    },
    {
        "scientific_name": "Mentha spicata",
        "common_name": "Spearmint",
        "family": "Lamiaceae",
        "genus": "Mentha",
        "species": "spicata",
        "description": "Aromatic herb perfect for teas and cooking. Fast-growing.",
        "native_region": "Europe, Asia",
        "care": {
            "watering_frequency": "keep soil moist",
            "light_requirement": "bright, 4-6 hours",
            "humidity_min": 50,
            "humidity_max": 70,
            "temp_min_c": 15,
            "temp_max_c": 24,
            "soil_type": "rich, moisture-retentive",
            "fertilizing": "every 2-4 weeks",
        },
    },
]


async def ensure_api_key(session: AsyncSession) -> str:
    result = await session.execute(select(ApiKey).where(ApiKey.is_active == True))
    existing = result.scalars().first()
    if existing:
        print("An API key already exists. Create a new one manually if needed.")
        return ""

    plain_key = f"pk_{secrets.token_urlsafe(32)}"
    key_hash = hash_api_key(plain_key)
    api_key = ApiKey(
        id=uuid.uuid4(),
        key_hash=key_hash,
        name="greenhouse-app-dev",
        is_active=True,
    )
    session.add(api_key)
    await session.flush()
    return plain_key


async def seed():
    await init_db()
    async with AsyncSessionLocal() as session:
        # Check if plants already exist
        result = await session.execute(select(Plant))
        if result.scalars().first():
            print("Plants already seeded. Skipping.")
            return

        for data in PLANT_DATA:
            care_data = data.get("care", {})
            plant_data = {k: v for k, v in data.items() if k != "care"}
            plant = Plant(
                id=uuid.uuid4(),
                **plant_data,
            )
            session.add(plant)
            await session.flush()
            care = PlantCare(
                id=uuid.uuid4(),
                plant_id=plant.id,
                **care_data,
            )
            session.add(care)

        plain_key = await ensure_api_key(session)
        await session.commit()

        print(f"Seeded {len(PLANT_DATA)} plants.")
        if plain_key:
            print("\n--- API Key (store securely, shown once) ---")
            print(plain_key)
            print("--------------------------------------------")
            print("Use header: X-API-Key: <key>")


if __name__ == "__main__":
    asyncio.run(seed())
