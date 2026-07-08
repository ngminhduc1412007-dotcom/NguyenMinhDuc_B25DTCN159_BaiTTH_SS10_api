from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import get_db
from service import create_shipment_service, get_shipments_service

app = FastAPI()

@app.post("/shipments")
def create_shipment(tracking_number: str, db: Session = Depends(get_db)):
    shipment = create_shipment_service(tracking_number, db)
    return {
        "message": "Success!",
        "data": shipment
    }

@app.get("/shipments")
def get_shipments(db: Session = Depends(get_db)):
    shipments = get_shipments_service(db)
    return {
        "message": "Success!",
        "data": shipments
    }