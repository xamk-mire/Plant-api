from uuid import UUID

from pydantic import BaseModel


class CareSchema(BaseModel):
    watering_frequency: str | None = None
    light_requirement: str | None = None
    humidity_range: dict[str, int] | None = None
    temperature_range_c: dict[str, int] | None = None
    soil_type: str | None = None
    fertilizing: str | None = None


class PlantResponse(BaseModel):
    id: UUID
    scientific_name: str
    common_name: str
    family: str
    genus: str
    species: str
    description: str | None = None
    native_region: str | None = None
    care: CareSchema | None = None

    class Config:
        from_attributes = True


class PlantListResponse(BaseModel):
    plants: list[PlantResponse]
