from fastapi import FastAPI, Depends, Query
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
    return crud.create_measurement(db, measurement)


@app.get("/analytics")
def get_analytics(
    device_id: str,
    start: datetime = Query(None),
    end: datetime = Query(None),
    db: Session = Depends(get_db)
):
    measurements = crud.get_measurements(db, device_id, start, end)
    return analytics.analyze(measurements)