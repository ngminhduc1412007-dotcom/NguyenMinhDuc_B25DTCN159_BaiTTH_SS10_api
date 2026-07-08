from fastapi import FastAPI
app = FastAPI()
students = ["An", "Binh", "Cuong"]
@app.get("/getstudents")
def get_students():
    return {"Danh sach sinh vien": students}