from fastapi import FastAPI, Request, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
import re

class Asset(BaseModel):
    serial_number: str
    model: str = Field(min_length=2, max_length=255)
    stock_available: int = Field(ge=0)
    status: str


class Allocation(BaseModel):
    asset_id: int
    employee_email: str
    allocated_quantity: int = Field(gt=0)
    start_date: str
    duration_months: int

app = FastAPI()

assets = [
    {"id": 1, "serial_number": "SN-MAC-01", "model": "MacBook Pro M3", "stock_available": 5, "status": "READY"},
    {"id": 2, "serial_number": "SN-DELL-02", "model": "Dell UltraSharp 27", "stock_available": 10, "status": "READY"},
    {"id": 3, "serial_number": "SN-THINK-03", "model": "ThinkPad X1 Carbon", "stock_available": 0, "status": "REPAIRING"}
]

allocations = [
    {
        "id": 1,
        "asset_id": 1,
        "employee_email": "dev.nguyen@company.com",
        "allocated_quantity": 1,
        "start_date": "2026-07-01",
        "duration_months": 12
    }
]

def create_response(request: Request, status_code: int, message: str, data=None, error=None):
    return {
        "status_code": status_code,
        "message": message,
        "data": data,
        "error": error,
        "timestamp": datetime.now().isoformat(),
        "path": request.url.path
    }

@app.exception_handler(HTTPException)
def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content=create_response(
            request=request,
            status_code=exc.status_code,
            message=exc.detail,
            data=None,
            error=exc.detail
        )
    )

@app.post("/assets")
def create_asset(request: Request, asset: Asset):
    if asset.status not in ["READY", "ALLOCATED", "REPAIRING", "SCRAPPED"]:
        raise HTTPException(400, "Invalid status")

    for a in assets:
        if a["serial_number"].lower() == asset.serial_number.lower():
            raise HTTPException(400, "Serial number already exists")

    new_asset = asset.model_dump()
    new_asset["id"] = max([a["id"] for a in assets], default=0) + 1
    assets.append(new_asset)
    return create_response(
        request=request,
        status_code=201,
        message="Asset created successfully",
        data=new_asset
    )

@app.get("/assets")
def get_assets(request: Request, keyword: Optional[str] = Query(None), status: Optional[str] = Query(None), min_stock: Optional[int] = Query(None)):
    result = assets
    if keyword:
        pattern = re.compile(keyword, re.IGNORECASE)
        result = [a for a in result if pattern.search(a["serial_number"])or pattern.search(a["model"])]

    if status:
        result = [a for a in result if a["status"] == status]

    if min_stock is not None:
        result = [ a for a in result if a["stock_available"] >= min_stock]
    return create_response(
        request=request,
        status_code=200,
        message="Asset list",
        data=result
    )

@app.get("/assets/{asset_id}")
def get_asset(request: Request, asset_id: int):
    for asset in assets:
        if asset["id"] == asset_id:
            return create_response(
                request=request,
                status_code=200,
                message="Asset found",
                data=asset
            )
    raise HTTPException(404, "Asset not found")

@app.put("/assets/{asset_id}")
def update_asset(request: Request, asset_id: int, asset: Asset):
    if asset.status not in ["READY", "ALLOCATED", "REPAIRING", "SCRAPPED"]:
        raise HTTPException(400, "Invalid status")

    for a in assets:
        if (a["id"] != asset_id and a["serial_number"].lower() == asset.serial_number.lower()):
            raise HTTPException(400, "Serial number already exists")

    for i in range(len(assets)):
        if assets[i]["id"] == asset_id:
            assets[i] = asset.model_dump()
            assets[i]["id"] = asset_id
            return create_response(
                request=request,
                status_code=200,
                message="Asset updated successfully",
                data=assets[i]
            )
    raise HTTPException(404, "Asset not found")

@app.delete("/assets/{asset_id}")
def delete_asset(request: Request, asset_id: int):
    for i in range(len(assets)):
        if assets[i]["id"] == asset_id:
            deleted = assets.pop(i)
            return create_response(
                request=request,
                status_code=200,
                message="Asset deleted successfully",
                data=deleted
            )
    raise HTTPException(404, "Asset not found")

@app.post("/allocations")
def create_allocation(request: Request, allocation: Allocation):
    asset = None
    for a in assets:
        if a["id"] == allocation.asset_id:
            asset = a
            break

    if asset is None:
        raise HTTPException(404, "Asset not found")

    if asset["status"] != "READY":
        raise HTTPException(400, "Asset is not ready")

    if allocation.allocated_quantity > asset["stock_available"]:
        raise HTTPException(400,"Allocated quantity exceeds stock available")

    email_pattern = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'
    if not re.match(email_pattern, allocation.employee_email):
        raise HTTPException(400, "Invalid email format")

    if allocation.duration_months < 1 or allocation.duration_months > 12:
        raise HTTPException(400,"Duration must be between 1 and 12 months")

    new_allocation = allocation.model_dump()
    new_allocation["id"] = (max([a["id"] for a in allocations], default=0) + 1)
    allocations.append(new_allocation)

    asset["stock_available"] -= allocation.allocated_quantity

    if asset["stock_available"] == 0:
        asset["status"] = "ALLOCATED"

    return create_response(
        request=request,
        status_code=201,
        message="Allocation created successfully",
        data=new_allocation
    )

@app.get("/allocations")
def get_allocations(request: Request):
    return create_response(
        request=request,
        status_code=200,
        message="Allocation list",
        data=allocations
    )