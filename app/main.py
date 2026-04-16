from fastapi import FastAPI, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from app.database import SessionLocal, engine, Base
import app.crud as crud
import app.schemas as schemas
import app.analytics as analytics

Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/measurements", response_model=schemas.MeasurementOut)
def create_measurement(measurement: schemas.MeasurementCreate, db: Session = Depends(get_db)):
    db_obj = crud.create_measurement(db, measurement)

    return {
        "id": db_obj.id,
        "device_id": measurement.device_id,
        "x": db_obj.x,
        "y": db_obj.y,
        "z": db_obj.z,
        "timestamp": db_obj.timestamp
    }


@app.get("/analytics")
def get_analytics(
        device_id: str,
        start: datetime = Query(None),
        end: datetime = Query(None),
        db: Session = Depends(get_db)
):
    device = crud.get_device_by_external_id(db, device_id)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")

    if start and end and start > end:
        raise HTTPException(status_code=400, detail="start must be before end")

    measurements = crud.get_measurements(db, device_id, start, end)
    return analytics.analyze(measurements)


@app.post("/users")
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, user)


@app.post("/devices")
def create_device(device: schemas.DeviceCreate, db: Session = Depends(get_db)):
    return crud.create_device(db, device)


@app.get("/users/{user_id}/analytics")
def user_analytics(user_id: int, db: Session = Depends(get_db)):
    user = crud.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    measurements = crud.get_user_measurements(db, user_id)
    return analytics.analyze(measurements)


@app.get("/users/{user_id}/devices/analytics")
def user_devices_analytics(user_id: int, db: Session = Depends(get_db)):
    user = crud.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    devices = crud.get_user_devices_with_measurements(db, user_id)

    result = {}
    for device in devices:
        result[device.device_id] = analytics.analyze(device.measurements)

    return result
