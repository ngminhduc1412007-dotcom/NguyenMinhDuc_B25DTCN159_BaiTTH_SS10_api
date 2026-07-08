from fastapi import FastAPI

# tao thuc the
app = FastAPI()

# viet api
@app.get("/")
def get_root():
    return {
        "message": "Hello World"
    }