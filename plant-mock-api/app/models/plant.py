import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Plant(Base):
    __tablename__ = "plants"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    scientific_name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    common_name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    family: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    genus: Mapped[str] = mapped_column(String(100), nullable=False)
    species: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    native_region: Mapped[str | None] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow
    )

    care: Mapped["PlantCare | None"] = relationship(
        "PlantCare", back_populates="plant", uselist=False, lazy="selectin"
    )


class PlantCare(Base):
    __tablename__ = "plant_care"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    plant_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("plants.id", ondelete="CASCADE"), nullable=False
    )
    watering_frequency: Mapped[str | None] = mapped_column(String(100), nullable=True)
    light_requirement: Mapped[str | None] = mapped_column(String(100), nullable=True)
    humidity_min: Mapped[int | None] = mapped_column(nullable=True)
    humidity_max: Mapped[int | None] = mapped_column(nullable=True)
    temp_min_c: Mapped[int | None] = mapped_column(nullable=True)
    temp_max_c: Mapped[int | None] = mapped_column(nullable=True)
    soil_type: Mapped[str | None] = mapped_column(String(255), nullable=True)
    fertilizing: Mapped[str | None] = mapped_column(String(255), nullable=True)

    plant: Mapped["Plant"] = relationship("Plant", back_populates="care")
