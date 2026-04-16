from pydantic import BaseModel
from datetime import datetime

class MeasurementCreate(BaseModel):
    device_id: str
    x: float
    y: float
    z: float

class MeasurementOut(BaseModel):
    id: int
    device_id: str
    x: float
    y: float
    z: float
    timestamp: datetime

    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    name: str


class DeviceCreate(BaseModel):
    device_id: str
    user_id: int