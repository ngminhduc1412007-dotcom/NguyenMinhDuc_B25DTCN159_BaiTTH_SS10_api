from fastapi import FastAPI, status, Request, HTTPException
from datetime import datetime
from pydantic import BaseModel
from typing import Optional, Any

app = FastAPI()

class BaseResponse(BaseModel):
    status_code: int
    message: str
    data: Optional[Any]
    errors: Optional[str]
    timestamp: str
    path: str
    
def create_response(request, status_code: int, message: str, data = None, errors = None):
    return BaseResponse(
        status_code= status_code,
        message= message,
        data= data,
        errors= errors,
        timestamp= datetime.now().isoformat(),
        path = request.url.path
    )

products = [
    {"id": 1, "name": "Keyboard", "price": 500000},
    {"id": 2, "name": "Mouse", "price": 300000},
    {"id": 3, "name": "Screen", "price": 400000}
]

@app.get("/products")
def get_all_product(request: Request):
    if not products:
        return create_response(request, status.HTTP_404_NOT_FOUND, "Failed!", errors= "Dữ liệu không tồn tại!")

    # return {
    #     "status_code": status.HTTP_200_OK,
    #     "message": "All products list",
    #     "data":products,
    #     "errors": None,
    #     "timestamp": datetime.now(),
    #     "path": request.url.path
    # }
    
    # return BaseResponse(
    #     status_code = status.HTTP_200_OK,
    #     message = "All products list",
    #     data = products,
    #     errors = None,
    #     timestamp = datetime.now().isoformat(),
    #     path = request.url.path
    # )
    
    return create_response(request, status.HTTP_200_OK, "Success!", products)

@app.get("/products/{product_id}")
def get_products(request: Request, product_id: int):
    for p in products:
        if p["id"] == product_id:
            return create_response(request, status.HTTP_200_OK, "Success!", p)
    
    raise HTTPException(status.HTTP_404_NOT_FOUND, "Not found")

@app.exception_handler(HTTPException)
def http_exception_handler(
    request: Request,
    exc: HTTPException
):
    response = create_response(request, status.HTTP_404_NOT_FOUND, "Failed", errors= exc.detail)
    return response