from uuid import UUID

from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Plant
from app.schemas.plant import CareSchema, PlantResponse


class PlantService:
    def __init__(self, db: AsyncSession):
        self.db = db

    def _to_response(self, plant: Plant) -> PlantResponse:
        care_schema = None
        if plant.care:
            c = plant.care
            care_schema = CareSchema(
                watering_frequency=c.watering_frequency,
                light_requirement=c.light_requirement,
                humidity_range=(
                    {"min": c.humidity_min, "max": c.humidity_max}
                    if c.humidity_min is not None or c.humidity_max is not None
                    else None
                ),
                temperature_range_c=(
                    {"min": c.temp_min_c, "max": c.temp_max_c}
                    if c.temp_min_c is not None or c.temp_max_c is not None
                    else None
                ),
                soil_type=c.soil_type,
                fertilizing=c.fertilizing,
            )
        return PlantResponse(
            id=plant.id,
            scientific_name=plant.scientific_name,
            common_name=plant.common_name,
            family=plant.family,
            genus=plant.genus,
            species=plant.species,
            description=plant.description,
            native_region=plant.native_region,
            care=care_schema,
        )

    async def list_plants(
        self,
        search: str | None = None,
        family: str | None = None,
    ) -> list[PlantResponse]:
        stmt = select(Plant)
        if search:
            pattern = f"%{search}%"
            stmt = stmt.where(
                or_(
                    Plant.scientific_name.ilike(pattern),
                    Plant.common_name.ilike(pattern),
                )
            )
        if family:
            stmt = stmt.where(Plant.family.ilike(family))
        stmt = stmt.order_by(Plant.common_name)
        result = await self.db.execute(stmt)
        plants = result.scalars().all()
        return [self._to_response(p) for p in plants]

    async def search_plants(self, q: str) -> list[PlantResponse]:
        return await self.list_plants(search=q)

    async def get_plant_by_id(self, plant_id: UUID) -> PlantResponse | None:
        result = await self.db.execute(select(Plant).where(Plant.id == plant_id))
        plant = result.scalar_one_or_none()
        return self._to_response(plant) if plant else None
