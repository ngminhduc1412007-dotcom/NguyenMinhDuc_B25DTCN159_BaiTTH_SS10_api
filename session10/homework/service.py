from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from models import ShipmentModel

def create_shipment_service(tracking_number: str, db: Session):
    existing = db.query(ShipmentModel).filter(ShipmentModel.tracking_number == tracking_number).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="tracking number already exists")

    new_shipment = ShipmentModel(tracking_number=tracking_number)
    db.add(new_shipment)
    db.commit()
    db.refresh(new_shipment)
    return new_shipment

def get_shipments_service(db: Session):
    return db.query(ShipmentModel).all()