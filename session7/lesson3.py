from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from typing import List, Optional

app = FastAPI()

products_db = [
    {"id": 101, "name": "Bàn phím cơ", "stock": 5, "price": 1200000.0},
    {"id": 102, "name": "Chuột Gaming", "stock": 2, "price": 600000.0}
]
orders_db = []

class OrderCreateRequest(BaseModel):
    product_id: int
    quantity: int = Field(..., description="Số lượng đặt mua phải lớn hơn 0")

class OrderResponse(BaseModel):
    order_id: int
    product_id: int
    quantity: int
    total_price: float

@app.post("/orders", response_model=OrderResponse, status_code=status.HTTP_201_CREATED, summary="Khởi tạo đơn hàng mới với ràng buộc kho")
def create_order(order_data: OrderCreateRequest):
    if order_data.quantity <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Số lượng mua phải lớn hơn 0"
        )
    
    target_product = None
    for product in products_db:
        if product["id"] == order_data.product_id:
            target_product = product
            break
            
    if not target_product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sản phẩm không tồn tại trong hệ thống"
        )
        
    if order_data.quantity > target_product["stock"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Sản phẩm không đủ số lượng trong kho"
        )
        
    target_product["stock"] -= order_data.quantity
    total_price = order_data.quantity * target_product["price"]
    new_order_id = len(orders_db) + 1
    new_order = {
        "order_id": new_order_id,
        "product_id": order_data.product_id,
        "quantity": order_data.quantity,
        "total_price": total_price
    }
    orders_db.append(new_order)
    return new_order