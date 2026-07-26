from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.dependencies import get_db_session
from src.middleware.auth import get_current_user
from src.models.src_models import District, Unit, UnitType

router = APIRouter(prefix="/api/v1/police-stations", tags=["Police Stations"])


@router.get("")
async def list_police_stations(
    district_id: int | None = None,
    session: AsyncSession = Depends(get_db_session),
    user: dict = Depends(get_current_user),
):
    query = (
        select(
            Unit.UnitID,
            Unit.UnitName,
            Unit.DistrictID,
            District.DistrictName,
        )
        .join(District, Unit.DistrictID == District.DistrictID)
        .join(UnitType, Unit.TypeID == UnitType.UnitTypeID)
        .where(UnitType.UnitTypeName.ilike("%police%"), Unit.Active == True)
    )
    if district_id is not None:
        query = query.where(Unit.DistrictID == district_id)
    query = query.order_by(District.DistrictName, Unit.UnitName)
    result = await session.execute(query)
    stations = []
    for row in result.all():
        stations.append({
            "unit_id": row.UnitID,
            "unit_name": row.UnitName,
            "district_id": row.DistrictID,
            "district_name": row.DistrictName,
        })
    return {"items": stations, "total": len(stations)}


@router.get("/districts")
async def list_districts(
    session: AsyncSession = Depends(get_db_session),
    user: dict = Depends(get_current_user),
):
    result = await session.execute(
        select(District.DistrictID, District.DistrictName)
        .where(District.Active == True)
        .order_by(District.DistrictName)
    )
    districts = [{"district_id": row.DistrictID, "district_name": row.DistrictName} for row in result.all()]
    return {"items": districts, "total": len(districts)}


@router.get("/{station_id}")
async def get_police_station(
    station_id: int,
    session: AsyncSession = Depends(get_db_session),
    user: dict = Depends(get_current_user),
):
    query = (
        select(Unit, District.DistrictName)
        .join(District, Unit.DistrictID == District.DistrictID)
        .where(Unit.UnitID == station_id)
    )
    result = await session.execute(query)
    row = result.one_or_none()
    if row is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Police station not found")
    unit, district_name = row
    return {
        "unit_id": unit.UnitID,
        "unit_name": unit.UnitName,
        "district_id": unit.DistrictID,
        "district_name": district_name,
        "type_id": unit.TypeID,
        "state_id": unit.StateID,
    }
