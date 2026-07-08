from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field
from typing import Optional

class Carrier(BaseModel):
    code: str
    name: str = Field(min_length=3)
    max_weight_capacity: int = Field(gt=0)
    status: str

class Shipment(BaseModel):
    carrier_id: int
    order_reference: str
    total_weight: int = Field(gt=0)
    dispatch_date: str
    shift: str

app = FastAPI()

carriers = [
    {"id": 1, "code": "GHN", "name": "Giao Hang Nhanh", "max_weight_capacity": 5000, "status": "ACTIVE"},
    {"id": 2, "code": "GHTK", "name": "Giao Hang Tiet Kiem", "max_weight_capacity": 3000, "status": "ACTIVE"},
    {"id": 3, "code": "VTP", "name": "Viettel Post", "max_weight_capacity": 10000, "status": "SUSPENDED"}
]

shipments = [
    {
        "id": 1,
        "carrier_id": 1,
        "order_reference": "ORD-2026-001",
        "total_weight": 4200,
        "dispatch_date": "2026-07-01",
        "shift": "MORNING"
    }
]

@app.post("/carriers")
def create_carrier(carrier: Carrier):
    if carrier.status not in ["ACTIVE", "INACTIVE", "SUSPENDED"]:
        raise HTTPException(400, "Invalid status")

    for c in carriers:
        if c["code"].lower() == carrier.code.lower():
            raise HTTPException(400, "Carrier code already exists")

    new_carrier = carrier.model_dump()
    new_carrier["id"] = max([c["id"] for c in carriers], default=0) + 1
    carriers.append(new_carrier)
    return {
        "message": "Carrier created successfully",
        "data": new_carrier
    }

@app.get("/carriers")
def get_carriers(keyword: Optional[str] = Query(None), status: Optional[str] = Query(None), min_weight: Optional[int] = Query(None)):
    result = carriers
    if keyword:
        result = [c for c in result if keyword.lower() in c["code"].lower() or keyword.lower() in c["name"].lower()]

    if status:
        result = [c for c in result if c["status"] == status]
        
    if min_weight:
        result = [c for c in result if c["max_weight_capacity"] >= min_weight]
    return {
        "message": "Carrier list",
        "data": result
    }

@app.get("/carriers/{carrier_id}")
def get_carrier(carrier_id: int):
    for c in carriers:
        if c["id"] == carrier_id:
            return {
                "message": "Carrier found",
                "data": c
            }
    raise HTTPException(404, "Carrier not found")

@app.put("/carriers/{carrier_id}")
def update_carrier(carrier_id: int, carrier: Carrier):
    if carrier.status not in ["ACTIVE", "INACTIVE", "SUSPENDED"]:
        raise HTTPException(400, "Invalid status")

    for c in carriers:
        if c["id"] != carrier_id and c["code"].lower() == carrier.code.lower():
            raise HTTPException(400, "Carrier code already exists")

    for i in range(len(carriers)):
        if carriers[i]["id"] == carrier_id:
            carriers[i] = carrier.model_dump()
            carriers[i]["id"] = carrier_id
            return {
                "message": "Carrier updated successfully",
                "data": carriers[i]
            }
    raise HTTPException(404, "Carrier not found")

@app.delete("/carriers/{carrier_id}")
def delete_carrier(carrier_id: int):
    for i in range(len(carriers)):
        if carriers[i]["id"] == carrier_id:
            deleted = carriers.pop(i)
            return {
                "message": "Carrier deleted successfully",
                "data": deleted
            }
    raise HTTPException(404, "Carrier not found")

@app.post("/shipments")
def create_shipment(shipment: Shipment):
    if shipment.shift not in ["MORNING", "AFTERNOON", "NIGHT"]:
        raise HTTPException(400, "Invalid shift")
    carrier = None
    for c in carriers:
        if c["id"] == shipment.carrier_id:
            carrier = c
            break

    if carrier is None:
        raise HTTPException(404, "Carrier not found")

    if carrier["status"] != "ACTIVE":
        raise HTTPException(400, "Carrier is not active")

    if shipment.total_weight > carrier["max_weight_capacity"]:
        raise HTTPException(400, "Weight exceeds carrier capacity")

    for s in shipments:
        if (s["carrier_id"] == shipment.carrier_id and s["dispatch_date"] == shipment.dispatch_date and s["shift"] == shipment.shift):
            raise HTTPException(400, "Carrier already has shipment in this shift")

    new_shipment = shipment.model_dump()
    new_shipment["id"] = max([s["id"] for s in shipments], default=0) + 1
    shipments.append(new_shipment)
    return {
        "message": "Shipment created successfully",
        "data": new_shipment
    }


@app.get("/shipments")
def get_shipments():
    return {
        "message": "Shipment list",
        "data": shipments
    }