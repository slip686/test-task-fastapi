import datetime
from pydantic import BaseModel, field_serializer
from geoalchemy2.elements import WKBElement as WKBGeographyElement
from geoalchemy2.shape import to_shape


class PointResponse(BaseModel):
    id: int
    point: str | WKBGeographyElement
    speed: int
    gps_time: datetime.datetime
    vehicle_id: int

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True

    @field_serializer('point')
    def serialize_point(self, value: str | WKBGeographyElement):
        point = value
        if isinstance(value, str):
            point = WKBGeographyElement(value)
        return {'latitude': to_shape(point).x,
                'longitude': to_shape(point).y}
