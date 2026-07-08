from fastapi import FastAPI
from pydantic import BaseModel

class Product(BaseModel):
    id: int
    name: str
    price: float

app = FastAPI()

products = [
    {"id": 1, "name": "Keyboard", "price": 500000},
    {"id": 2, "name": "Mouse", "price": 300000}
]

@app.post("/products")
def create_product(product: Product):
    if product.name.strip() == "":
        return {
            "message": "Name cannot be empty"    
        }
        
    if product.price <= 0:
        return {
            "message": "Price must be greater than 0"
        }
        
    new_product = {
        "id": len(products) + 1,
        "name": product.name,
        "price": product.price
    }
    products.append(new_product)
    return {
        "message": "Enroll successfully",
        "data": new_product
    }
    
@app.get("/products")
def get_product():
    if not products:
        return {
            "detail": "Product not found"
        }
    
    return {
        "message": "All products list",
        "data":products
    }
    
@app.delete("/products/{product_id}")
def delete_products(product_id: int):
    for p in products:
        if p["id"] == product_id:
            products.remove(p)
            return {
                "message": "Xóa thành công",
                "data": p
            }
            
    return {
        "detail": "Product not found"
    }