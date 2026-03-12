from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import verify_api_key
from app.database import get_db
from app.schemas.plant import PlantListResponse, PlantResponse
from app.services.plant_service import PlantService

router = APIRouter(dependencies=[Depends(verify_api_key)])


@router.get("/search", response_model=PlantListResponse)
async def search_plants(
    q: str = Query(..., min_length=1, description="Search query"),
    db: AsyncSession = Depends(get_db),
):
    service = PlantService(db)
    plants = await service.search_plants(q)
    return PlantListResponse(plants=plants)


@router.get("", response_model=PlantListResponse)
async def list_plants(
    search: str | None = Query(None, description="Search by plant name"),
    family: str | None = Query(None, description="Filter by plant family"),
    db: AsyncSession = Depends(get_db),
):
    service = PlantService(db)
    plants = await service.list_plants(search=search, family=family)
    return PlantListResponse(plants=plants)


@router.get("/{plant_id}", response_model=PlantResponse)
async def get_plant(
    plant_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    service = PlantService(db)
    plant = await service.get_plant_by_id(plant_id)
    if not plant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Plant not found",
        )
    return plant
