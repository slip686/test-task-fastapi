from geoalchemy2 import Geometry

from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import relationship, DeclarativeBase


class Base(AsyncAttrs, DeclarativeBase):
    pass


class TrackPointModel(Base):
    __tablename__ = 'track_point_model'
    id = Column(Integer, primary_key=True)
    point = Column(Geometry(geometry_type='POINT', srid=4326))
    speed = Column(Integer)
    gps_time = Column(DateTime(timezone=True))
    vehicle_id = Column(ForeignKey("vehicle_model.vehicle_id"))


class VehicleModel(Base):
    __tablename__ = 'vehicle_model'
    vehicle_id = Column(Integer, primary_key=True, unique=True)
    track_points = relationship('TrackPointModel')