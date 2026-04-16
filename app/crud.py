from sqlalchemy.orm import Session
import app.models as models
import app.schemas as schemas


def create_measurement(db: Session, measurement: schemas.MeasurementCreate):
    db_obj = models.Measurement(**measurement.dict())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def get_measurements(db: Session, device_id: str, start=None, end=None):
    query = db.query(models.Measurement).filter(models.Measurement.device_id == device_id)

    if start:
        query = query.filter(models.Measurement.timestamp >= start)
    if end:
        query = query.filter(models.Measurement.timestamp <= end)

    return query.all()