from fastapi import FastAPI

app = FastAPI()

students = [
    {"id": 1, "name": "An", "status": "active"},
    {"id": 2, "name": "Binh", "status": "inactive"},
    {"id": 3, "name": "Cuong", "status": "active"},
    {"id": 4, "name": "Dung", "status": "pending"}
]

@app.get("/students/active")
def get_student():
    actived_students = [i for i in students if i["status"] == "active"]
    
    if not actived_students:
        return {
            "message": "Không có sinh viên đang học",
            "data": []
        }
        
    return {
        "message": "Danh sách sinh viên đang học",
        "data": actived_students
    }