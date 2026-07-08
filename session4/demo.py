from fastapi import FastAPI

app = FastAPI()

students = [
    {"id": 1, "name": "Nguyen Van A", "age": 19},
    {"id": 2, "name": "Le Thi B", "age": 20}
]

@app.get("/students")
def get_student():
    return {
        "message":"All student in list",
        "data": students
    }
    
@app.get("/students/{student_id}")
def get_student_id(student_id: int):
    for student in students:
        if student["id"] == student_id:
            return {
                "data": student
            } 
            
    return {
        "data":None
    }
    
# viet api co chuc nang lay danh sach sinh vien trong khoang tuoi query parameter
@app.get("/student")
def get_student_by_age(start_age:int, end_age:int):
    filter_student = []
    for student in students:
        if start_age <= student["age"] <= end_age:
            filter_student.append(student)
    
    if filter_student:
        return{
            "data":{
                "start_age": start_age,
                "end_age": end_age
            }
        }
    
    return {
        "data":None
    }
    
