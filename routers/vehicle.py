from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text, select
from sqlalchemy.ext.asyncio import AsyncSession

from models.models import TrackPointModel
from schemas.point import PointResponse
from database import get_session
from geojson import MultiPoint

vehicle_router = APIRouter()


@vehicle_router.get('/vehicles', response_model=list[PointResponse])
async def get_all_vehicles_last_points(db: AsyncSession = Depends(get_session)):
    query_text = text('SELECT track_point_model.id, track_point_model.point,'
                      'track_point_model.speed, track_point_model.gps_time,'
                      'track_point_model.vehicle_id FROM track_point_model '
                      'JOIN (SELECT track_point_model.vehicle_id, MAX(track_point_model.gps_time) '
                      'AS last_gps_time FROM track_point_model group by track_point_model.vehicle_id) AS t '
                      'ON track_point_model.vehicle_id = t.vehicle_id '
                      'AND track_point_model.gps_time = t.last_gps_time')
    points = await db.execute(query_text)
    return points.fetchall()


@vehicle_router.get('/vehicles/{vehicle_id}', response_model=list[PointResponse])
async def get_vehicle_points_by_vehicle_id(vehicle_id: int, db: AsyncSession = Depends(get_session)):
    query = await db.execute(
        select(TrackPointModel).filter_by(vehicle_id=vehicle_id).order_by(TrackPointModel.gps_time))
    points = query.scalars().all()
    if points:
        return points
    raise HTTPException(status_code=404, detail="Vehicle not found")


@vehicle_router.get('/vehicles/{vehicle_id}/track')
async def get_vehicle_track_by_vehicle_id(vehicle_id: int, db: AsyncSession = Depends(get_session)) -> dict:
    query = await db.execute(
        select(TrackPointModel).filter_by(vehicle_id=vehicle_id).order_by(TrackPointModel.gps_time))
    if query.scalars().all():
        points = [PointResponse.model_validate(point) for point in query.scalars().all()]
        track = MultiPoint([tuple(point.serialize_point(value=point.point).values()) for point in points])
        return track
    raise HTTPException(status_code=404, detail="Vehicle not found")
