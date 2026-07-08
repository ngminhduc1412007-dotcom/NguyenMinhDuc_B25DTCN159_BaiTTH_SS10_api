from fastapi import FastAPI
app = FastAPI() 

products = [

    {"id": 1, "name": "Keyboard", "price": 500000},

    {"id": 2, "name": "Mouse", "price": 300000}

]

@app.get("/product")
def get_product():
    return {
        "data": products
    }
    
@app.get("/product/{product_id}")
def get_by_id(product_id):
    for p in products:
        if p["id"] == product_id:
            return {
                "data": products
            }
             
    return {
        "data":None
    }