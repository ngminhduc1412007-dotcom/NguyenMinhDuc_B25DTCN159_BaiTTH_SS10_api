from fastapi import FastAPI, status, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Any

app = FastAPI()

# Dữ liệu nội bộ trong bộ nhớ tạm
promo_codes_db = {
    "SUMMER25": {"code": "SUMMER25", "discount_rate": 0.15, "max_budget": 50000000, "is_active": True},
    "WELCOME50": {"code": "WELCOME50", "discount_rate": 0.50, "max_budget": 10000000, "is_active": False}
}

# Model nội bộ chứa cả trường ngân sách chiến dịch nhạy cảm (Cấm lộ)
class PromoInternal(BaseModel):
    code: str
    discount_rate: float
    max_budget: int # Trường nhạy cảm - Không được lộ ra Client!
    is_active: bool

class PromoPublic(BaseModel):
    code: str
    discount_rate: float

class BaseResponse(BaseModel):
    statusCode: int
    message: str
    data: Optional[Any]
    error: Optional[str]
    timestamp: str
    path: str

def create_response(request: Request, status_code: int, message: str, data=None, error=None):
    return BaseResponse(
        statusCode=status_code,
        message=message,
        data=data,
        error=error,
        timestamp=datetime.now().isoformat(),
        path=request.url.path
    )

@app.get("/promos/{code}", response_model=PromoPublic)
def get_promo(code: str):
    promo = promo_codes_db.get(code)
    if promo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Mã giảm giá không tồn tại"
        )

    if promo["is_active"] == False:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Mã giảm giá đã hết hạn sử dụng"
        )
    return promo

@app.exception_handler(HTTPException)
def http_exception_handler(request: Request, exc: HTTPException):
    response = create_response(
        request=request,
        status_code=exc.status_code,
        message="Failed",
        error=exc.detail
    )

    return JSONResponse(
        status_code=exc.status_code,
        content=response.model_dump()
    )