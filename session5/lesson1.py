from fastapi import FastAPI
from pydantic import BaseModel
app = FastAPI()
products = [
    {
        "id": 1,
        "code": "SP001",
        "name": "Laptop Dell",
        "price": 15000000,
        "stock": 10
    },
    {
        "id": 2,
        "code": "SP002",
        "name": "Mouse Logitech",
        "price": 350000,
        "stock": 50
    }
]
class ProductCreate(BaseModel):
    code: str
    name: str
    price: float
    stock: int
@app.post("/products")
def create_product(product: ProductCreate):
    for p in products:
        if p["code"].strip().upper() == product.code.strip().upper():
            return {
                "message": f"Ma san pham '{product.code}' dax ton tai!",
                "data": None
            }
            
    new_product = {
        "id": len(products) + 1,
        "code": product.code,
        "name": product.name,
        "price": product.price,
        "stock": product.stock
    }
    products.append(new_product)
    return {
        "message": "Create product successfully",
        "data": new_product
    }