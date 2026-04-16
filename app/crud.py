from fastapi import HTTPException
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import IntegrityError
import app.models as models


def create_measurement(db, measurement):
    device = get_device_by_external_id(db, measurement.device_id)

    if not device:
        raise HTTPException(status_code=404, detail="Device not found")

    db_obj = models.Measurement(
        device_id=device.id,
        x=measurement.x,
        y=measurement.y,
        z=measurement.z
    )

    try:
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    except Exception:
        db.rollback()
        raise


def get_measurements(db: Session, device_id: str, start=None, end=None):
    query = (
        db.query(models.Measurement)
        .join(models.Device)
        .filter(models.Device.device_id == device_id)
    )

    if start:
        query = query.filter(models.Measurement.timestamp >= start)
    if end:
        query = query.filter(models.Measurement.timestamp <= end)

    return query.order_by(models.Measurement.timestamp.desc()).limit(1000).all()


def create_user(db, user):
    existing = db.query(models.User).filter(models.User.name == user.name).first()

    if existing:
        raise HTTPException(status_code=409, detail="User already exists")
    db_user = models.User(name=user.name)

    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="User already exists")


def get_user_by_id(db, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def create_device(db, device):
    existing = (
        db.query(models.Device)
        .filter(models.Device.device_id == device.device_id)
        .first()
    )

    if existing:
        raise HTTPException(status_code=409, detail="Device already exists")
    user = db.query(models.User).filter(models.User.id == device.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db_device = models.Device(
        device_id=device.device_id,
        user_id=device.user_id
    )

    try:
        db.add(db_device)
        db.commit()
        db.refresh(db_device)
        return db_device
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Device already exists")


def get_device_by_external_id(db, device_id: str):
    return db.query(models.Device).filter(models.Device.device_id == device_id).first()


def get_user_measurements(db, user_id: int):
    return (
        db.query(models.Measurement)
        .join(models.Device)
        .filter(models.Device.user_id == user_id)
        .order_by(models.Measurement.timestamp.desc())
        .limit(1000).all()
    )


def get_user_devices_with_measurements(db, user_id: int):
    return (
        db.query(models.Device)
        .options(joinedload(models.Device.measurements))
        .filter(models.Device.user_id == user_id)
        .all()
    )
