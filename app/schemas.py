from pydantic import BaseModel
from datetime import datetime

class MeasurementCreate(BaseModel):
    device_id: str
    x: float
    y: float
    z: float

class MeasurementOut(MeasurementCreate):
    id: int
    timestamp: datetime

    class Config:
        orm_mode = True