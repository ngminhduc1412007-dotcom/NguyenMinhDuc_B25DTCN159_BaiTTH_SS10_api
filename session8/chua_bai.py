from fastapi import FastAPI, Request, HTTPException, status
from pydantic import BaseModel
from typing import Optional, Any
from datetime import datetime
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

class CreateCarriers(BaseModel):
    "id" = int
    "code" = str
    "name" = str
    "max_weight_capacity" = int
    "status" = str
    
class BaseResponse(BaseModel):
    status_code: int
    message: str
    data: Optional[Any]
    errors: Optional[str]
    timestamp: str
    path: str

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

def create_response(request: Request, status_code: int, message: str, data = None, errors = None):
    return BaseResponse(
        status_code= status_code,
        message= message,
        data= data,
        errors= errors,
        timestamp= datetime.now().isoformat(),
        path = request.url.path
    )

@app.post("/carriers")
def create_carrier(new_carrier: CreateCarriers, request: Request):
    carrie = new_carrier.model_dump()
    carriers.append(carrie)
    return create_response(request, status.HTTP_200_OK, "Success!", carriers)

@app.get("/carrier")
def get_all_carrier(request: Request):
    return create_response(request, status.HTTP_200_OK, "Success!", carriers)
    
@app.get("/carriers/{id}")
def get_carrier_by_id(id: int, request: Request):
    for c in carriers:
        if c['id'] == id:
            return create_response(request, status.HTTP_200_OK, "Success!", c)
    raise HTTPException(status.HTTP_404_NOT_FOUND, "Not found")

@app.exception_handler(Exception)
def global_exception_handler(
    request: Request,
    exc: Exception  
):
    response = create_response(request, status.HTTP_500_INTERNAL_SERVER_ERROR, "Failed", errors= str(exc))
    return JSONResponse(
        content=response.model_dump(),
        status_code=response.status_code
    )
    
@app.exception_handler(RequestValidationError)
def global_exception_handler(
    request: Request,
    exc: RequestValidationError  
):
    response = create_response(request, status.HTTP_422_UNPROCESSABLE_CONTENT, "Failed", errors=exc.errors())
    return JSONResponse(
        content=response.model_dump(),
        status_code=response.status_code
    )
    
@app.exception_handler(HTTPException)
def global_exception_handler(
    request: Request,
    exc: HTTPException  
):
    response = create_response(request, exc.status_code, "Failed", errors= str(exc))
    return JSONResponse(
        content=response.model_dump(),
        status_code=response.status_code
    )