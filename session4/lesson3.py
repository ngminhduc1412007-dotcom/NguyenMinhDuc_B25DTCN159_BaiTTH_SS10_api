from fastapi import FastAPI
app = FastAPI() 

products = [
    {"id": 1, "name": "Laptop", "price": 15000000},
    {"id": 2, "name": "Mouse", "price": 200000},
    {"id": 3, "name": "Keyboard", "price": 500000},
    {"id": 4, "name": "Monitor", "price": 3000000}
]

@app.get("/products")
def get_products(keyword: str = None, max_price: float = None):
    if max_price is not None and max_price < 0:
        return {
            "message": "max_price không được âm"
        }
        
    filter_products = products
    if keyword is not None:
        filter_products = [product for product in filter_products if keyword.lower() in product["name"].lower()]

    if max_price is not None:
        filter_products = [product for product in filter_products if product["price"] <= max_price]

    return filter_products